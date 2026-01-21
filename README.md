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

### With Nix Flakes

Add the flake input to your configuration:

```nix
# flake.nix
{
  inputs.mcp-reddit-anon.url = "github:rohanp2051/mcp-reddit-anon";
}
```

Then use the package in your MCP server config:

```nix
# In your MCP server config
{ pkgs, inputs, ... }:

let
  mcp-reddit = inputs.mcp-reddit-anon.packages.${pkgs.system}.default;
in
{
  mcp.servers.reddit = {
    command = "${mcp-reddit}/bin/mcp-reddit";
    args = [ ];
  };
}
```

For development:

```bash
git clone https://github.com/rohanp2051/mcp-reddit-anon.git
cd mcp-reddit-anon
nix develop  # Enters shell with all dependencies
```

### With uvx

```json
{
  "reddit": {
    "command": "uvx",
    "args": [
      "--from",
      "git+https://github.com/rohanp2051/mcp-reddit-anon.git",
      "mcp-reddit"
    ]
  }
}
```

Note: The uvx approach may be slow on first run as it fetches and builds the package.

## Usage

Using [mcp-client-cli](https://github.com/adhikasp/mcp-client-cli):

```
$ llm what are latest hot thread in r/victoria3

I'll fetch the latest hot threads from the Victoria 3 subreddit for you.

Tool Calls:
  fetch_hot_threads
  Args:
    subreddit: victoria3
```

## Acknowledgments

This project was developed with assistance from [Claude](https://claude.ai), an AI assistant by Anthropic.
