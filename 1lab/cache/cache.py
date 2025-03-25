from .abc import AbstractCache
from redis import RedisCache
from inmemory import InMemoryCache
from none import NoneCache


def get_cache_obj(cfg: dict) -> AbstractCache:
    match cfg.get("cache", None):
        case "redis":
            return RedisCache()
        case "inmemory":
            return InMemoryCache()
        case _:
            return NoneCache()
