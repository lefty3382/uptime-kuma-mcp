"""Maintenance tools — list, add, delete, toggle."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_maintenance_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register maintenance window management tools."""

    @mcp.tool
    async def list_maintenances() -> dict:
        """List all maintenance windows."""
        maintenances = await client.call("get_maintenances")
        result = []
        for m in maintenances:
            result.append({
                "id": m.get("id"),
                "title": m.get("title"),
                "strategy": m.get("strategy"),
                "active": m.get("active"),
                "description": m.get("description"),
            })
        return {"maintenances": result, "count": len(result)}

    @mcp.tool
    async def add_maintenance(
        title: str,
        strategy: str = "manual",
        description: str = "",
        dateRange: list[str] | None = None,
        intervalDay: int = 1,
        cron: str | None = None,
        durationMinutes: int = 60,
        timezoneOption: str | None = None,
    ) -> dict:
        """Create a new maintenance window.

        Args:
            title: Maintenance window title.
            strategy: Schedule strategy — manual, single, recurring-interval, recurring-weekday, recurring-day-of-month, cron.
            description: Optional description.
            dateRange: Date range for single strategy ["YYYY-MM-DD HH:MM", "YYYY-MM-DD HH:MM"].
            intervalDay: Interval in days for recurring-interval strategy.
            cron: Cron expression for cron strategy.
            durationMinutes: Duration in minutes (default: 60).
            timezoneOption: Timezone (e.g., "America/Los_Angeles").
        """
        kwargs = {"title": title, "strategy": strategy, "description": description}
        if dateRange is not None:
            kwargs["dateRange"] = dateRange
        if intervalDay != 1:
            kwargs["intervalDay"] = intervalDay
        if cron is not None:
            kwargs["cron"] = cron
        if durationMinutes != 60:
            kwargs["durationMinutes"] = durationMinutes
        if timezoneOption is not None:
            kwargs["timezoneOption"] = timezoneOption
        return await client.call("add_maintenance", **kwargs)

    @mcp.tool
    async def delete_maintenance(maintenance_id: int, confirm: bool = False) -> dict:
        """Delete a maintenance window. Set confirm=True to execute.

        Args:
            maintenance_id: The maintenance window ID to delete.
            confirm: Must be True to execute. False returns a preview.
        """
        maintenances = await client.call("get_maintenances")
        target = None
        for m in maintenances:
            if m.get("id") == maintenance_id:
                target = m
                break
        if not confirm:
            return {
                "preview": True,
                "would_delete": target.get("title") if target else f"ID {maintenance_id}",
                "id": maintenance_id,
                "message": "Set confirm=True to delete this maintenance window",
            }
        await client.call("delete_maintenance", maintenance_id)
        return {
            "deleted": True,
            "title": target.get("title") if target else f"ID {maintenance_id}",
            "id": maintenance_id,
        }

    @mcp.tool
    async def toggle_maintenance(maintenance_id: int, active: bool) -> dict:
        """Pause or resume a maintenance window.

        Args:
            maintenance_id: The maintenance window ID.
            active: True to resume (activate), False to pause.
        """
        if active:
            return await client.call("resume_maintenance", maintenance_id)
        else:
            return await client.call("pause_maintenance", maintenance_id)
