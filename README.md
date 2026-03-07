# Uptime Kuma MCP Server

MCP server for complete Uptime Kuma v2 management — monitors, notifications, status pages, Docker hosts, maintenance, and tags via Socket.IO API.

## Overview

35 tools across 8 categories:
- **Server & System** (4) — server info, settings, database size, shrink database
- **Monitors** (9) — list, get, beats, status, add, edit, delete, pause, resume
- **Notifications** (5) — list, add, edit, delete, test
- **Status Pages** (5) — list, get, save, post incident, unpin incident
- **Docker Hosts** (3) — list, add, delete
- **Maintenance** (4) — list, add, delete, toggle
- **Tags** (3) — list, add, delete
- **Data Management** (2) — clear events, clear statistics

## Deployment

Co-located on VM 102 alongside Uptime Kuma for Docker DNS access.

### Quick Start

1. Copy `.env.example` to `.env` and set your Kuma credentials:
   ```
   KUMA_URL=http://uptime-kuma:3001
   KUMA_USERNAME=your-username
   KUMA_PASSWORD=your-password
   MCP_PORT=8487
   ```

2. Build and start:
   ```bash
   docker build -t ghcr.io/lefty3382/uptime-kuma-mcp:latest .
   docker run -d --name uptime-kuma-mcp \
     --env-file .env \
     -p 8487:8487 \
     ghcr.io/lefty3382/uptime-kuma-mcp:latest
   ```

   Or add to your Docker Compose stack:
   ```yaml
   uptime-kuma-mcp:
     image: ghcr.io/lefty3382/uptime-kuma-mcp:latest
     container_name: uptime-kuma-mcp
     restart: unless-stopped
     ports:
       - "8487:8487"
     environment:
       - KUMA_URL=http://uptime-kuma:3001
       - KUMA_USERNAME=${KUMA_USERNAME}
       - KUMA_PASSWORD=${KUMA_PASSWORD}
       - MCP_PORT=8487
   ```

3. Configure Claude Code:
   ```bash
   claude mcp add uptime-kuma --transport http http://YOUR_HOST:8487/mcp --scope user
   ```

## Architecture

- **KumaClient** — wraps the synchronous `uptime-kuma-api-v2` Socket.IO library with persistent connection and auto-reconnect. Uses `asyncio.to_thread()` to bridge sync Socket.IO calls into FastMCP's async tool handlers.
- **FastMCP 3.1.0** — Streamable HTTP transport with `stateless_http=True` to prevent session expiry between Claude Code tool calls.
- **Confirm gates** — 9 destructive operations (deletes, clears, shrink) require `confirm=True`. Default behavior is preview mode showing what would be affected.

## Tech Stack

- Python 3.12
- FastMCP 3.1.0 (Streamable HTTP)
- uptime-kuma-api-v2 (Socket.IO wrapper for Kuma v2 API)

## License

MIT
