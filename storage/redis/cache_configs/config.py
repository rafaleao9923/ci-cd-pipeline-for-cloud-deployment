import redis
import json
import logging
from typing import Optional, Dict, Any

class RedisCacheManager:
    def __init__(self, redis_uri: str):
        self.redis = redis.Redis.from_url(redis_uri)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Redis cache manager initialized")

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data by key"""
        try:
            data = self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            self.logger.error(f"Error getting cache for key {key}: {e}")
            raise

    def set(self, key: str, value: Dict[str, Any], ttl: int = 3600) -> bool:
        """Set cached data with optional TTL"""
        try:
            serialized = json.dumps(value)
            return bool(self.redis.set(key, serialized, ex=ttl))
        except Exception as e:
            self.logger.error(f"Error setting cache for key {key}: {e}")
            raise

    def delete(self, key: str) -> bool:
        """Delete cached data by key"""
        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            self.logger.error(f"Error deleting cache for key {key}: {e}")
            raise

    def enqueue(self, queue_name: str, message: Dict[str, Any]) -> bool:
        """Add message to job queue"""
        try:
            serialized = json.dumps(message)
            return bool(self.redis.rpush(queue_name, serialized))
        except Exception as e:
            self.logger.error(f"Error enqueuing message to {queue_name}: {e}")
            raise

    def dequeue(self, queue_name: str) -> Optional[Dict[str, Any]]:
        """Get message from job queue"""
        try:
            message = self.redis.lpop(queue_name)
            if message:
                return json.loads(message)
            return None
        except Exception as e:
            self.logger.error(f"Error dequeuing message from {queue_name}: {e}")
            raise

    def close(self):
        self.redis.close()
        self.logger.info("Redis connection closed")

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    cache = RedisCacheManager('redis://redis:6379/0')
    
    try:
        # Example usage
        cache.set('test_key', {'key': 'value'})
        print(cache.get('test_key'))
        cache.enqueue('test_queue', {'job': 'data'})
        print(cache.dequeue('test_queue'))
    finally:
        cache.close()