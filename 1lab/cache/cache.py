from .abc import AbstractCache
from cache.redis import RedisCache
from cache.inmemory import InMemoryCache
from cache.none import NoneCache


def get_cache_obj(cfg: dict) -> AbstractCache:
    match cfg.get("cache", None):
        case "redis":
            return RedisCache()
        case "inmemory":
            return InMemoryCache()
        case _:
            return NoneCache()
