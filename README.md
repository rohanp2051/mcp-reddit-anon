# MCP Reddit Server (Anonymous Fork)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that provides tools for fetching and analyzing Reddit content.

> **This is a fork of [adhikasp/mcp-reddit](https://github.com/adhikasp/mcp-reddit)** that uses anonymous OAuth authentication, requiring **no API credentials**.

## Differences from Original

This fork uses Reddit's anonymous OAuth flow (the same method Reddit's mobile apps use for logged-out users) instead of requiring user credentials.

| Aspect          | [Original](https://github.com/adhikasp/mcp-reddit) | This Fork           |
| --------------- | -------------------------------------------------- | ------------------- |
| **Setup**       | Requires client ID, client secret, refresh token   | None                |
| **Rate Limits** | Higher (authenticated)                             | Lower (anonymous)   |
| **Access**      | Private subreddits, user actions                   | Public content only |

**Use this fork** for quick setup and read-only public access.  
**Use the original** for higher rate limits, private subreddits, or user actions.

## Features

- Fetch hot threads from any subreddit
- Get detailed post content including comments
- Support for different post types (text, link, gallery)

## Installation

### Manual Installation

```json
{
  "reddit": {
    "command": "uvx",
    "args": [
      "--from",
      "git+https://github.com/rohanp2051/mcp-reddit-anon.git",
      "mcp-reddit"
    ],
    "env": {}
  }
}
```

### With Nix

```bash
git clone https://github.com/rohanp2051/mcp-reddit-anon.git
cd mcp-reddit-anon
nix develop  # Enters shell with all dependencies
```

## Usage

Using [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli):

```
$ llm what are latest hot thread in r/victoria3

I'll fetch the latest hot threads from the Victoria 3 subreddit for you.

Tool Calls:
  fetch_hot_threads
  Args:
    subreddit: victoria3


Based on the hot threads, here are the key highlights from the Victoria 3 subreddit:

1. Dev Diary #126 - Update 1.8 Overview
   - Major updates planned for the game, including:
     - Political Movement Rework (Ideological Forces)
     - Discrimination Rework
     - Food Availability, Famines, and Harvest Incidents
     - Additional features like Companies owning buildings and Bulk Nationalization

2. Dev Diary #138 - Pivot of Empire Update
   - Update 1.8 "Masala Chai" has been released
   - Focuses on India with new Journal Entries, Events, and Immersion Pack
   - 10 new achievements added
   - Save games from 1.7.7 are not compatible with 1.8

3. Interesting Community Discussions:
   - A player shared a detailed experience of retaking Constantinople as Greece, highlighting the complex population dynamics
   - Humorous posts about game mechanics, such as investment rights and political movements
   - Various memes and gameplay screenshots showcasing unique game situations

The most upvoted thread is the Dev Diary #126, which provides an in-depth look at the upcoming game mechanics improvements, particularly the reworks to political movements and discrimination systems.

Would you like me to elaborate on any of these points or provide more details about the Victoria 3 update?
```

## Acknowledgments

This project was developed with assistance from [Claude](https://claude.ai), an AI assistant by Anthropic.
