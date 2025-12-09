# cache_service.py
"""
Redis Caching Service for AI Responses
Reduces Claude API calls by 30-40%
"""

import redis
import json
import hashlib
import os
from typing import Optional, Any, Callable
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Redis caching for expensive AI operations"""

    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        try:
            self.client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.client.ping()
            logger.info(f"✅ Cache service connected: {redis_url}")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.client = None

    def _generate_key(self, prefix: str, data: Any) -> str:
        """Generate cache key from data"""
        content = json.dumps(data, sort_keys=True)
        hash_obj = hashlib.md5(content.encode())
        return f"gv:{prefix}:{hash_obj.hexdigest()}"

    def get(self, key: str) -> Optional[dict]:
        """Get cached data"""
        if not self.client:
            return None

        try:
            data = self.client.get(key)
            if data:
                logger.info(f"💾 Cache HIT: {key[:50]}...")
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: dict, ttl: int = 3600):
        """Set cached data with TTL"""
        if not self.client:
            return False

        try:
            self.client.setex(key, ttl, json.dumps(value))
            logger.info(f"💾 Cache SET: {key[:50]}... (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def cache_ai_response(self, ttl: int = 7200):
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key (exclude conversation_history AND self to reduce key size)
                cache_data = {
                    "func": func.__name__,
                    "args": args[1:] if args else [],  # Skip self (args[0])
                    "kwargs": {
                        k: v
                        for k, v in kwargs.items()
                        if k not in ["conversation_history"]
                    },
                }
                cache_key = self._generate_key("ai", cache_data)

                # Check cache
                cached = self.get(cache_key)
                if cached:
                    return cached

                # Call function
                logger.info(f"🔄 Cache MISS: {cache_key[:50]}... - calling AI")
                result = await func(*args, **kwargs)

                # Store in cache
                self.set(cache_key, result, ttl)

                return result

            return wrapper

        return decorator

    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.client:
            return {"error": "Redis not connected"}

        try:
            info = self.client.info("stats")
            return {
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "keys": self.client.dbsize(),
            }
        except Exception as e:
            return {"error": str(e)}


# Initialize global cache service
cache = CacheService()
