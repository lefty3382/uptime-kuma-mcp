"""Tag tools — list, add, delete."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_tag_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register tag management tools."""

    @mcp.tool
    async def list_tags() -> dict:
        """List all tags."""
        tags = await client.call("get_tags")
        result = []
        for t in tags:
            result.append({
                "id": t.get("id"),
                "name": t.get("name"),
                "color": t.get("color"),
            })
        return {"tags": result, "count": len(result)}

    @mcp.tool
    async def add_tag(name: str, color: str = "#2196F3") -> dict:
        """Create a new tag.

        Args:
            name: Tag name.
            color: Tag color as hex code (default: #2196F3 / blue).
        """
        return await client.call("add_tag", name=name, color=color)

    @mcp.tool
    async def delete_tag(tag_id: int, confirm: bool = False) -> dict:
        """Delete a tag. Set confirm=True to execute.

        Args:
            tag_id: The tag ID to delete.
            confirm: Must be True to execute. False returns a preview.
        """
        tags = await client.call("get_tags")
        target = None
        for t in tags:
            if t.get("id") == tag_id:
                target = t
                break
        if not confirm:
            return {
                "preview": True,
                "would_delete": target.get("name") if target else f"ID {tag_id}",
                "id": tag_id,
                "message": "Set confirm=True to delete this tag",
            }
        await client.call("delete_tag", tag_id)
        return {
            "deleted": True,
            "name": target.get("name") if target else f"ID {tag_id}",
            "id": tag_id,
        }
