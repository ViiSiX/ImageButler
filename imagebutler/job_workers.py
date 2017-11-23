"""Workers to support Redislite caching."""


def worker_do_cache_redis(caching_object):
    """Just a wrapper function to cache the caching object. It's the way
    RQ act."""
    return caching_object
