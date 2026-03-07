"""Notification tools — list, add, edit, delete, test."""

from fastmcp import FastMCP

from ..client import KumaClient


def register_notification_tools(mcp: FastMCP, client: KumaClient) -> None:
    """Register notification management tools."""

    @mcp.tool
    async def list_notifications() -> dict:
        """List all configured notification channels."""
        notifications = await client.call("get_notifications")
        result = []
        for n in notifications:
            result.append({
                "id": n.get("id"),
                "name": n.get("name"),
                "type": n.get("type"),
                "active": n.get("active"),
                "isDefault": n.get("isDefault"),
            })
        return {"notifications": result, "count": len(result)}

    @mcp.tool
    async def add_notification(
        name: str,
        type: str,
        isDefault: bool = False,
        applyExisting: bool = False,
        discordWebhookUrl: str | None = None,
        telegramBotToken: str | None = None,
        telegramChatID: str | None = None,
        slackWebhookUrl: str | None = None,
        webhookUrl: str | None = None,
    ) -> dict:
        """Create a new notification channel.

        Args:
            name: Display name for the notification.
            type: Notification type — Discord, Telegram, Slack, Webhook, SMTP, etc.
            isDefault: Apply to all new monitors by default.
            applyExisting: Also apply to all existing monitors.
            discordWebhookUrl: Discord webhook URL (for Discord type).
            telegramBotToken: Telegram bot token (for Telegram type).
            telegramChatID: Telegram chat ID (for Telegram type).
            slackWebhookUrl: Slack webhook URL (for Slack type).
            webhookUrl: Generic webhook URL (for Webhook type).
        """
        kwargs = {
            "name": name,
            "type": type,
            "isDefault": isDefault,
            "applyExisting": applyExisting,
        }
        if discordWebhookUrl is not None:
            kwargs["discordWebhookUrl"] = discordWebhookUrl
        if telegramBotToken is not None:
            kwargs["telegramBotToken"] = telegramBotToken
        if telegramChatID is not None:
            kwargs["telegramChatID"] = telegramChatID
        if slackWebhookUrl is not None:
            kwargs["slackWebhookUrl"] = slackWebhookUrl
        if webhookUrl is not None:
            kwargs["webhookUrl"] = webhookUrl
        return await client.call("add_notification", **kwargs)

    @mcp.tool
    async def edit_notification(
        notification_id: int,
        name: str | None = None,
        type: str | None = None,
        isDefault: bool | None = None,
        applyExisting: bool | None = None,
    ) -> dict:
        """Edit an existing notification channel.

        Args:
            notification_id: The notification ID to edit.
            name: New display name.
            type: New notification type.
            isDefault: New default setting.
            applyExisting: Apply changes to existing monitors.
        """
        kwargs = {}
        if name is not None:
            kwargs["name"] = name
        if type is not None:
            kwargs["type"] = type
        if isDefault is not None:
            kwargs["isDefault"] = isDefault
        if applyExisting is not None:
            kwargs["applyExisting"] = applyExisting
        return await client.call("edit_notification", notification_id, **kwargs)

    @mcp.tool
    async def delete_notification(notification_id: int, confirm: bool = False) -> dict:
        """Delete a notification channel. Set confirm=True to execute.

        Args:
            notification_id: The notification ID to delete.
            confirm: Must be True to execute. False returns a preview.
        """
        notifications = await client.call("get_notifications")
        target = None
        for n in notifications:
            if n.get("id") == notification_id:
                target = n
                break
        if not confirm:
            return {
                "preview": True,
                "would_delete": target.get("name") if target else f"ID {notification_id}",
                "id": notification_id,
                "type": target.get("type") if target else "unknown",
                "message": "Set confirm=True to delete this notification",
            }
        await client.call("delete_notification", notification_id)
        return {
            "deleted": True,
            "name": target.get("name") if target else f"ID {notification_id}",
            "id": notification_id,
        }

    @mcp.tool
    async def test_notification(
        name: str,
        type: str,
        discordWebhookUrl: str | None = None,
        telegramBotToken: str | None = None,
        telegramChatID: str | None = None,
        slackWebhookUrl: str | None = None,
        webhookUrl: str | None = None,
    ) -> dict:
        """Send a test notification to verify configuration.

        Args:
            name: Notification name.
            type: Notification type — Discord, Telegram, Slack, etc.
            discordWebhookUrl: Discord webhook URL (for Discord type).
            telegramBotToken: Telegram bot token (for Telegram type).
            telegramChatID: Telegram chat ID (for Telegram type).
            slackWebhookUrl: Slack webhook URL (for Slack type).
            webhookUrl: Generic webhook URL (for Webhook type).
        """
        kwargs = {"name": name, "type": type}
        if discordWebhookUrl is not None:
            kwargs["discordWebhookUrl"] = discordWebhookUrl
        if telegramBotToken is not None:
            kwargs["telegramBotToken"] = telegramBotToken
        if telegramChatID is not None:
            kwargs["telegramChatID"] = telegramChatID
        if slackWebhookUrl is not None:
            kwargs["slackWebhookUrl"] = slackWebhookUrl
        if webhookUrl is not None:
            kwargs["webhookUrl"] = webhookUrl
        return await client.call("test_notification", **kwargs)
