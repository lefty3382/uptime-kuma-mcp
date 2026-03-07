"""Application configuration from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Uptime Kuma MCP server configuration."""

    kuma_url: str
    kuma_username: str
    kuma_password: str
    mcp_port: int

    @classmethod
    def from_env(cls) -> "AppConfig":
        username = os.environ.get("KUMA_USERNAME", "")
        password = os.environ.get("KUMA_PASSWORD", "")
        if not username or not password:
            raise ValueError(
                "KUMA_USERNAME and KUMA_PASSWORD environment variables are required"
            )

        return cls(
            kuma_url=os.environ.get("KUMA_URL", "http://uptime-kuma:3001"),
            kuma_username=username,
            kuma_password=password,
            mcp_port=int(os.environ.get("MCP_PORT", "8487")),
        )
