"""Data management tools — clear events, clear statistics."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_data_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register data management tools."""

    @mcp.tool
    async def clear_events(monitor_id: int, confirm: bool = False) -> dict:
        """Clear all events for a monitor. Set confirm=True to execute.

        Args:
            monitor_id: The monitor ID whose events to clear.
            confirm: Must be True to execute. False returns a preview.
        """
        monitor = await client.call("get_monitor", monitor_id)
        if not confirm:
            return {
                "preview": True,
                "would_clear_events_for": monitor.get("name"),
                "monitor_id": monitor_id,
                "message": "Set confirm=True to clear all events for this monitor",
            }
        await client.call("clear_events", monitor_id)
        return {"cleared": True, "monitor": monitor.get("name"), "monitor_id": monitor_id}

    @mcp.tool
    async def clear_statistics(confirm: bool = False) -> dict:
        """Clear all statistics data. Set confirm=True to execute.

        Args:
            confirm: Must be True to execute. False returns a preview.
        """
        if not confirm:
            return {
                "preview": True,
                "action": "Clear ALL statistics for ALL monitors",
                "message": "Set confirm=True to clear all statistics",
            }
        await client.call("clear_statistics")
        return {"cleared": True, "action": "All statistics cleared"}
