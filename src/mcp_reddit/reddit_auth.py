"""
Anonymous OAuth authentication for Reddit API.

Uses Reddit's Android app client ID with device-based anonymous authentication.
No API credentials required - works like Reddit's official app anonymous mode.
"""

import base64
import json
import random
import string
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# Reddit's Android app OAuth client ID (public, used for anonymous auth)
OAUTH_CLIENT_ID = "ohXpoqrZYub1kg"

# Spoofed Android app user agent
ANDROID_USER_AGENT = "Reddit/Version 2024.17.0/Build 1700000/Android 14"

# OAuth API base URL
OAUTH_API_BASE = "https://oauth.reddit.com"


class RedditAuth:
    """Handles anonymous OAuth authentication with Reddit."""

    def __init__(self):
        self.access_token: str | None = None
        self.token_expiry: float = 0
        self.device_id = self._generate_device_id()

    def _generate_device_id(self) -> str:
        """Generate a random device ID."""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=24))

    def _get_auth_header(self) -> str:
        """Get HTTP Basic Auth header for token request."""
        credentials = f"{OAUTH_CLIENT_ID}:"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    def get_token(self) -> str:
        """
        Get a valid OAuth access token, refreshing if necessary.

        Returns:
            Valid access token string
        """
        if self.access_token and time.time() < self.token_expiry - 60:
            return self.access_token

        self._refresh_token()
        return self.access_token

    def _refresh_token(self) -> None:
        """Fetch a new anonymous OAuth token from Reddit."""
        url = "https://www.reddit.com/api/v1/access_token"

        data = urllib.parse.urlencode(
            {
                "grant_type": "https://oauth.reddit.com/grants/installed_client",
                "device_id": self.device_id,
            }
        ).encode()

        headers = {
            "Authorization": self._get_auth_header(),
            "User-Agent": ANDROID_USER_AGENT,
            "Content-Type": "application/x-www-form-urlencoded",
        }

        request = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode())
            self.access_token = result["access_token"]
            self.token_expiry = time.time() + result.get("expires_in", 3600)


# Global auth instance
_auth = RedditAuth()


def fetch_reddit_json(endpoint: str) -> Any:
    """
    Fetch JSON data from Reddit's OAuth API.

    Args:
        endpoint: API endpoint path (e.g., "/r/Python/hot")

    Returns:
        Parsed JSON data
    """
    token = _auth.get_token()

    # Ensure endpoint starts with /
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    url = f"{OAUTH_API_BASE}{endpoint}"

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": ANDROID_USER_AGENT,
    }

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Rate limited - wait and retry
            time.sleep(5)
            return fetch_reddit_json(endpoint)
        raise
