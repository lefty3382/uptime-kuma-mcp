"""Uptime Kuma Socket.IO client with persistent connection and auto-reconnect."""

import asyncio
import logging

from uptime_kuma_api import UptimeKumaApi

from .config import AppConfig

logger = logging.getLogger(__name__)


class KumaClient:
    """Persistent Socket.IO client with auto-reconnect on failure."""

    def __init__(self, config: AppConfig) -> None:
        self._url = config.kuma_url
        self._username = config.kuma_username
        self._password = config.kuma_password
        self._api: UptimeKumaApi | None = None

    def _connect(self) -> None:
        """Establish Socket.IO connection and login."""
        if self._api is not None:
            try:
                self._api.disconnect()
            except Exception:
                pass
        logger.info("Connecting to Uptime Kuma at %s", self._url)
        self._api = UptimeKumaApi(self._url)
        self._api.login(self._username, self._password)
        logger.info("Connected and authenticated")

    def _call_sync(self, method: str, *args, **kwargs):
        """Call an API method with auto-reconnect on failure."""
        if self._api is None:
            self._connect()
        try:
            return getattr(self._api, method)(*args, **kwargs)
        except Exception as e:
            logger.warning("Call to %s failed (%s), reconnecting...", method, e)
            self._api = None
            self._connect()
            return getattr(self._api, method)(*args, **kwargs)

    async def call(self, method: str, *args, **kwargs):
        """Async wrapper — runs sync Socket.IO call in a thread."""
        return await asyncio.to_thread(self._call_sync, method, *args, **kwargs)
