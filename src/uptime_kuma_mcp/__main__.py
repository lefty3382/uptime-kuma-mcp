"""Entry point for the Uptime Kuma MCP server."""

import sys

from .config import AppConfig
from .client import KumaClient
from .server import create_server


def main() -> None:
    """Main entry point."""
    try:
        config = AppConfig.from_env()
        client = KumaClient(config)

        print(f"Uptime Kuma target: {config.kuma_url}")
        print(f"MCP port: {config.mcp_port}")

        mcp = create_server(client)

        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=config.mcp_port,
        )
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
