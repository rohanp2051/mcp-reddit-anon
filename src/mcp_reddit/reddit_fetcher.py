import logging
from typing import Any
from fastmcp import FastMCP
from .reddit_auth import fetch_reddit_json

mcp = FastMCP("Reddit MCP")
logging.getLogger().setLevel(logging.WARNING)


@mcp.tool()
async def fetch_reddit_hot_threads(subreddit: str, limit: int = 10) -> str:
    """
    Fetch hot threads from a subreddit

    Args:
        subreddit: Name of the subreddit
        limit: Number of posts to fetch (default: 10)

    Returns:
        Human readable string containing list of post information
    """
    try:
        endpoint = f"/r/{subreddit}/hot?limit={limit}"
        response = fetch_reddit_json(endpoint)

        posts = []
        children = response.get("data", {}).get("children", [])

        for child in children:
            data = child.get("data", {})
            post_type = _get_post_type(data)
            content = _get_content(data)

            post_info = (
                f"Title: {data.get('title', '')}\n"
                f"Score: {data.get('score', 0)}\n"
                f"Comments: {data.get('num_comments', 0)}\n"
                f"Author: {data.get('author', '[deleted]')}\n"
                f"ID: {data.get('id', '')}\n"
                f"Type: {post_type}\n"
                f"Content: {content}\n"
                f"Link: https://reddit.com{data.get('permalink', '')}\n"
                f"---"
            )
            posts.append(post_info)

        return "\n\n".join(posts)

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"


def _format_comment(comment_data: dict, depth: int = 0) -> str:
    """Helper method to format a comment with proper indentation"""
    data = comment_data.get("data", {})
    indent = "-- " * depth

    author = data.get("author", "[deleted]")
    score = data.get("score", 0)
    body = data.get("body", "[removed]")

    content = (
        f"{indent}* Author: {author}\n"
        f"{indent}  Score: {score}\n"
        f"{indent}  {body}\n"
    )

    # Process nested replies
    replies = data.get("replies")
    if replies and isinstance(replies, dict):
        replies_children = replies.get("data", {}).get("children", [])
        for reply in replies_children:
            if reply.get("kind") == "t1":  # t1 = comment
                content += "\n" + _format_comment(reply, depth + 1)

    return content


@mcp.tool()
async def fetch_reddit_post_content(post_id: str, comment_limit: int = 20, comment_depth: int = 3) -> str:
    """
    Fetch detailed content of a specific post

    Args:
        post_id: Reddit post ID
        comment_limit: Number of top level comments to fetch
        comment_depth: Maximum depth of comment tree to traverse

    Returns:
        Human readable string containing post content and comments tree
    """
    try:
        # Fetch post and comments
        endpoint = f"/comments/{post_id}?limit={comment_limit}&depth={comment_depth}&sort=top"
        response = fetch_reddit_json(endpoint)

        if not isinstance(response, list) or len(response) < 2:
            return "Error: Unexpected response format from Reddit"

        # Reddit returns [submission_listing, comments_listing]
        submission_listing = response[0]
        comments_listing = response[1]

        # Extract submission data
        submission_children = submission_listing.get("data", {}).get("children", [])
        if not submission_children:
            return "Error: No submission data found"

        data = submission_children[0].get("data", {})
        post_type = _get_post_type(data)
        post_content = _get_content(data)

        content = (
            f"Title: {data.get('title', '')}\n"
            f"Score: {data.get('score', 0)}\n"
            f"Author: {data.get('author', '[deleted]')}\n"
            f"Type: {post_type}\n"
            f"Content: {post_content}\n"
        )

        # Process comments
        comments_children = comments_listing.get("data", {}).get("children", [])
        if comments_children:
            content += "\nComments:\n"
            for comment in comments_children:
                if comment.get("kind") == "t1":  # t1 = comment
                    content += "\n" + _format_comment(comment, depth=0)
        else:
            content += "\nNo comments found."

        return content

    except Exception as e:
        return f"An error occurred: {str(e)}"


def _get_post_type(data: dict) -> str:
    """Helper method to determine post type from submission data"""
    if data.get("is_self"):
        return "text"
    elif data.get("is_gallery"):
        return "gallery"
    elif data.get("is_video"):
        return "video"
    else:
        return "link"


def _get_content(data: dict) -> str:
    """Helper method to extract post content based on type"""
    if data.get("is_self"):
        return data.get("selftext", "") or "(no text)"
    elif data.get("is_gallery"):
        return data.get("url", "")
    else:
        return data.get("url", "")
