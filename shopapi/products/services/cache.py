import asyncio
import time
from typing import Any, Optional


class InMemoryTTLCache:
    """Simple async-safe in-memory TTL cache using per-key locks.
    Not production-grade (use Redis/Memcached in production), but good for demo.
    """

    def __init__(self, default_ttl: int = 300):
        self._store: dict[str, tuple[float, Any]] = {}
        self._locks: dict[str, asyncio.Lock] = {}
        self._default_ttl = default_ttl
        self._global_lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        expires_at, value = item
        if expires_at < time.time():
            # expired
            self._store.pop(key, None)
            return None
        return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires_at = time.time() + (ttl or self._default_ttl)
        self._store[key] = (expires_at, value)

    async def lock(self, key: str) -> asyncio.Lock:
        # Ensure one lock per key
        async with self._global_lock:
            if key not in self._locks:
                self._locks[key] = asyncio.Lock()
            return self._locks[key]


cache = InMemoryTTLCache(default_ttl=300)