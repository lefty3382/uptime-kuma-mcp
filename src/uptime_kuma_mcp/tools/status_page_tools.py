"""Status page tools — list, get, save, post/unpin incident."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_status_page_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register status page management tools."""

    @mcp.tool
    async def list_status_pages() -> dict:
        """List all status pages."""
        pages = await client.call("get_status_pages")
        result = []
        for p in pages:
            result.append({
                "id": p.get("id"),
                "slug": p.get("slug"),
                "title": p.get("title"),
                "published": p.get("published"),
            })
        return {"status_pages": result, "count": len(result)}

    @mcp.tool
    async def get_status_page(slug: str) -> dict:
        """Get detailed information for a status page including monitor groups.

        Args:
            slug: The status page slug (URL identifier).
        """
        return await client.call("get_status_page", slug)

    @mcp.tool
    async def save_status_page(
        slug: str,
        title: str | None = None,
        description: str | None = None,
        published: bool | None = None,
        showTags: bool | None = None,
        showPoweredBy: bool | None = None,
        publicGroupList: list | None = None,
    ) -> dict:
        """Update a status page configuration and monitor groups.

        Args:
            slug: The status page slug to update.
            title: Page title.
            description: Page description.
            published: Whether the page is publicly visible.
            showTags: Show tags on the page.
            showPoweredBy: Show "Powered by Uptime Kuma" footer.
            publicGroupList: List of monitor group objects for the page layout.
        """
        kwargs = {}
        if title is not None:
            kwargs["title"] = title
        if description is not None:
            kwargs["description"] = description
        if published is not None:
            kwargs["published"] = published
        if showTags is not None:
            kwargs["showTags"] = showTags
        if showPoweredBy is not None:
            kwargs["showPoweredBy"] = showPoweredBy
        if publicGroupList is not None:
            kwargs["publicGroupList"] = publicGroupList
        return await client.call("save_status_page", slug, **kwargs)

    @mcp.tool
    async def post_incident(
        slug: str,
        title: str,
        content: str,
        style: str = "warning",
    ) -> dict:
        """Post an incident to a status page.

        Args:
            slug: The status page slug.
            title: Incident title.
            content: Incident description/content.
            style: Incident style — info, warning, danger, primary, light, dark (default: warning).
        """
        return await client.call("post_incident", slug, title, content, style)

    @mcp.tool
    async def unpin_incident(slug: str) -> dict:
        """Remove the pinned incident from a status page.

        Args:
            slug: The status page slug.
        """
        return await client.call("unpin_incident", slug)
