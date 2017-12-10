"""Workers to support Redislite caching."""


def worker_do_cache_redis(caching_object):
    """Just a wrapper function to cache the caching object. It's the way
    RQ act."""
    return caching_object


def worker_undo_cached_redis(caching_object):
    """Just a wrapper function to clean RQ's jobs' results."""
    return caching_object.delete()
