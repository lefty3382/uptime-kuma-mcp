"""FastMCP server factory."""

from fastmcp import FastMCP

from .client import KumaClient


def create_server(client: KumaClient) -> FastMCP:
    """Create and configure the FastMCP server with all tools."""
    mcp = FastMCP(
        "Uptime Kuma MCP Server",
        instructions=(
            "Provides complete Uptime Kuma management: monitor CRUD, "
            "notifications, status pages, Docker hosts, maintenance windows, "
            "tags, and server administration."
        ),
    )

    try:
        from .tools.server_tools import register_server_tools
        register_server_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.monitor_tools import register_monitor_tools
        register_monitor_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.notification_tools import register_notification_tools
        register_notification_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.status_page_tools import register_status_page_tools
        register_status_page_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.docker_host_tools import register_docker_host_tools
        register_docker_host_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.maintenance_tools import register_maintenance_tools
        register_maintenance_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.tag_tools import register_tag_tools
        register_tag_tools(mcp, client)
    except ImportError:
        pass

    try:
        from .tools.data_tools import register_data_tools
        register_data_tools(mcp, client)
    except ImportError:
        pass

    return mcp
