"""Monitor tools — list, get, create, edit, delete, pause, resume."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_monitor_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register monitor management tools."""

    @mcp.tool
    async def list_monitors() -> dict:
        """List all monitors with their current status."""
        monitors = await client.call("get_monitors")
        result = []
        for m in monitors:
            result.append({
                "id": m.get("id"),
                "name": m.get("name"),
                "type": m.get("type"),
                "url": m.get("url"),
                "hostname": m.get("hostname"),
                "port": m.get("port"),
                "active": m.get("active"),
                "parent": m.get("parent"),
                "interval": m.get("interval"),
            })
        return {"monitors": result, "count": len(result)}

    @mcp.tool
    async def get_monitor(monitor_id: int) -> dict:
        """Get detailed information for a specific monitor.

        Args:
            monitor_id: The monitor ID.
        """
        return await client.call("get_monitor", monitor_id)

    @mcp.tool
    async def get_monitor_beats(monitor_id: int, hours: int = 24) -> dict:
        """Get heartbeat history for a monitor.

        Args:
            monitor_id: The monitor ID.
            hours: Number of hours of history to retrieve (default: 24).
        """
        beats = await client.call("get_monitor_beats", monitor_id, hours)
        return {"monitor_id": monitor_id, "hours": hours, "beats": beats, "count": len(beats)}

    @mcp.tool
    async def get_monitor_status() -> dict:
        """Get aggregated status for all monitors — uptime percentages, average ping, and certificate info."""
        uptime = await client.call("uptime")
        avg_ping = await client.call("avg_ping")
        cert_info = await client.call("cert_info")
        return {
            "uptime": uptime,
            "avg_ping": avg_ping,
            "cert_info": cert_info,
        }

    @mcp.tool
    async def add_monitor(
        type: str,
        name: str,
        url: str | None = None,
        hostname: str | None = None,
        port: int | None = None,
        interval: int = 60,
        maxretries: int = 1,
        parent: int | None = None,
        description: str | None = None,
        accepted_statuscodes: list[str] | None = None,
        ignoreTls: bool = False,
        keyword: str | None = None,
        docker_container: str | None = None,
        docker_host: int | None = None,
        notificationIDList: list[int] | None = None,
    ) -> dict:
        """Create a new monitor.

        Args:
            type: Monitor type — HTTP, PORT, PING, KEYWORD, DNS, DOCKER, GROUP, TCP, etc.
            name: Display name for the monitor.
            url: Target URL (for HTTP/KEYWORD monitors).
            hostname: Target hostname or IP (for PING/PORT/DNS monitors).
            port: Target port (for PORT/TCP monitors).
            interval: Check interval in seconds (default: 60).
            maxretries: Max retries before marking down (default: 1).
            parent: Parent group monitor ID (to nest under a group).
            description: Optional description.
            accepted_statuscodes: List of accepted HTTP status codes (default: ["200-299"]).
            ignoreTls: Ignore TLS certificate errors (default: False).
            keyword: Keyword to search for in response (KEYWORD type).
            docker_container: Container name (DOCKER type).
            docker_host: Docker host ID (DOCKER type).
            notificationIDList: List of notification IDs to attach.
        """
        kwargs = {"type": type, "name": name, "interval": interval, "maxretries": maxretries}
        if url is not None:
            kwargs["url"] = url
        if hostname is not None:
            kwargs["hostname"] = hostname
        if port is not None:
            kwargs["port"] = port
        if parent is not None:
            kwargs["parent"] = parent
        if description is not None:
            kwargs["description"] = description
        if accepted_statuscodes is not None:
            kwargs["accepted_statuscodes"] = accepted_statuscodes
        if ignoreTls:
            kwargs["ignoreTls"] = True
        if keyword is not None:
            kwargs["keyword"] = keyword
        if docker_container is not None:
            kwargs["docker_container"] = docker_container
        if docker_host is not None:
            kwargs["docker_host"] = docker_host
        if notificationIDList is not None:
            kwargs["notificationIDList"] = notificationIDList
        return await client.call("add_monitor", **kwargs)

    @mcp.tool
    async def edit_monitor(
        monitor_id: int,
        name: str | None = None,
        url: str | None = None,
        hostname: str | None = None,
        port: int | None = None,
        interval: int | None = None,
        maxretries: int | None = None,
        parent: int | None = None,
        accepted_statuscodes: list[str] | None = None,
        ignoreTls: bool | None = None,
        notificationIDList: list[int] | None = None,
    ) -> dict:
        """Edit an existing monitor's configuration.

        Args:
            monitor_id: The monitor ID to edit.
            name: New display name.
            url: New target URL.
            hostname: New hostname/IP.
            port: New port.
            interval: New check interval in seconds.
            maxretries: New max retries.
            parent: New parent group ID.
            accepted_statuscodes: New accepted status codes.
            ignoreTls: New TLS ignore setting.
            notificationIDList: New notification ID list.
        """
        kwargs = {}
        if name is not None:
            kwargs["name"] = name
        if url is not None:
            kwargs["url"] = url
        if hostname is not None:
            kwargs["hostname"] = hostname
        if port is not None:
            kwargs["port"] = port
        if interval is not None:
            kwargs["interval"] = interval
        if maxretries is not None:
            kwargs["maxretries"] = maxretries
        if parent is not None:
            kwargs["parent"] = parent
        if accepted_statuscodes is not None:
            kwargs["accepted_statuscodes"] = accepted_statuscodes
        if ignoreTls is not None:
            kwargs["ignoreTls"] = ignoreTls
        if notificationIDList is not None:
            kwargs["notificationIDList"] = notificationIDList
        return await client.call("edit_monitor", monitor_id, **kwargs)

    @mcp.tool
    async def delete_monitor(monitor_id: int, confirm: bool = False) -> dict:
        """Delete a monitor. Set confirm=True to execute.

        Args:
            monitor_id: The monitor ID to delete.
            confirm: Must be True to execute. False returns a preview.
        """
        monitor = await client.call("get_monitor", monitor_id)
        if not confirm:
            return {
                "preview": True,
                "would_delete": monitor.get("name"),
                "id": monitor_id,
                "type": monitor.get("type"),
                "message": "Set confirm=True to delete this monitor",
            }
        await client.call("delete_monitor", monitor_id)
        return {"deleted": True, "name": monitor.get("name"), "id": monitor_id}

    @mcp.tool
    async def pause_monitor(monitor_id: int) -> dict:
        """Pause a monitor (stop checking).

        Args:
            monitor_id: The monitor ID to pause.
        """
        return await client.call("pause_monitor", monitor_id)

    @mcp.tool
    async def resume_monitor(monitor_id: int) -> dict:
        """Resume a paused monitor (start checking again).

        Args:
            monitor_id: The monitor ID to resume.
        """
        return await client.call("resume_monitor", monitor_id)
