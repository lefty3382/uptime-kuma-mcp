"""Docker host tools — list, add, delete."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_docker_host_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register Docker host management tools."""

    @mcp.tool
    async def list_docker_hosts() -> dict:
        """List all configured Docker hosts."""
        hosts = await client.call("get_docker_hosts")
        result = []
        for h in hosts:
            result.append({
                "id": h.get("id"),
                "name": h.get("name"),
                "dockerType": h.get("dockerType"),
                "dockerDaemon": h.get("dockerDaemon"),
            })
        return {"docker_hosts": result, "count": len(result)}

    @mcp.tool
    async def add_docker_host(
        name: str,
        dockerType: str,
        dockerDaemon: str,
    ) -> dict:
        """Add a new Docker host for container monitoring.

        Args:
            name: Display name for the Docker host.
            dockerType: Connection type — socket or tcp.
            dockerDaemon: Connection string (e.g., /var/run/docker.sock or tcp://10.0.40.30:2375).
        """
        return await client.call(
            "add_docker_host",
            name=name,
            dockerType=dockerType,
            dockerDaemon=dockerDaemon,
        )

    @mcp.tool
    async def delete_docker_host(docker_host_id: int, confirm: bool = False) -> dict:
        """Delete a Docker host. Set confirm=True to execute.

        Args:
            docker_host_id: The Docker host ID to delete.
            confirm: Must be True to execute. False returns a preview.
        """
        hosts = await client.call("get_docker_hosts")
        target = None
        for h in hosts:
            if h.get("id") == docker_host_id:
                target = h
                break
        if not confirm:
            return {
                "preview": True,
                "would_delete": target.get("name") if target else f"ID {docker_host_id}",
                "id": docker_host_id,
                "message": "Set confirm=True to delete this Docker host",
            }
        await client.call("delete_docker_host", docker_host_id)
        return {
            "deleted": True,
            "name": target.get("name") if target else f"ID {docker_host_id}",
            "id": docker_host_id,
        }
