from django.core.cache import cache

LOCK_EXPIRE = 60 * 5  # 5 min


def acquire_lock(lock_id):
    """Attempts to acquire the lock, returning True upon success"""
    return cache.add(lock_id, "true", LOCK_EXPIRE)


def release_lock(lock_id):
    """Release lock"""
    cache.delete(lock_id)
