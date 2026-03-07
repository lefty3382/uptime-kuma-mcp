"""Server & admin tools — server info, settings, database."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_server_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register server administration tools."""

    @mcp.tool
    async def get_server_info() -> dict:
        """Get Uptime Kuma server information including version and uptime."""
        try:
            info = await client.call("info")
            return {
                "version": info.get("version"),
                "latestVersion": info.get("latestVersion"),
                "primaryBaseURL": info.get("primaryBaseURL"),
                "serverTimezone": info.get("serverTimezone"),
                "serverTimezoneOffset": info.get("serverTimezoneOffset"),
            }
        except Exception as e:
            return {"error": str(e), "status": "unreachable"}

    @mcp.tool
    async def get_server_settings() -> dict:
        """Get Uptime Kuma server settings."""
        try:
            return await client.call("get_settings")
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool
    async def get_database_size() -> dict:
        """Get the current Uptime Kuma database size."""
        try:
            return await client.call("get_database_size")
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool
    async def shrink_database(confirm: bool = False) -> dict:
        """Shrink the Uptime Kuma database to reclaim space.

        Args:
            confirm: Must be True to execute. False returns a preview.
        """
        if not confirm:
            try:
                size = await client.call("get_database_size")
                return {
                    "preview": True,
                    "current_size": size,
                    "message": "Set confirm=True to shrink the database",
                }
            except Exception as e:
                return {"error": str(e)}
        result = await client.call("shrink_database")
        return {"shrunk": True, "result": result}
