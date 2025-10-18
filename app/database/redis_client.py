"""
Redis client for caching and session storage with enhanced reliability and performance optimization
"""
import redis
import json
import logging
import time
from typing import Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.database.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Define connection pool config directly in this file
CONNECTION_POOL_CONFIG = {
    "redis": {
        "connection_pool_size": 20,
        "retry_on_timeout": True,
        "socket_keepalive": True,
        "health_check_interval": 30
    }
}

class TTLCache:
    """
    Simple TTL (Time To Live) cache implementation
    """
    
    def __init__(self, maxsize=128, ttl=300):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Simple cache key generation
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check if cached result exists and is still valid
            if key in self.cache:
                result, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    return result
                    
            # Call function and cache result
            result = func(*args, **kwargs)
            self.cache[key] = (result, time.time())
            
            # Clean up cache if it's too large
            if len(self.cache) > self.maxsize:
                # Remove oldest entries
                keys_to_remove = list(self.cache.keys())[:len(self.cache) - self.maxsize]
                for k in keys_to_remove:
                    del self.cache[k]
                    
            return result
        return wrapper

def ttl_cache(maxsize=128, ttl=300):
    """
    Create a TTL cache decorator
    """
    return TTLCache(maxsize, ttl)

class RedisClient:
    """
    Redis client wrapper for caching and session storage with enhanced reliability
    """
    
    def __init__(self):
        self.client = None
        self.is_connected = False
        self._connect()
        
    def _connect(self):
        """
        Establish Redis connection
        """
        try:
            redis_config = CONNECTION_POOL_CONFIG["redis"]
            self.client = redis.from_url(
                settings.REDIS_URL,
                retry_on_timeout=redis_config["retry_on_timeout"],
                socket_keepalive=redis_config["socket_keepalive"],
                socket_connect_timeout=5,
                socket_timeout=5,
                health_check_interval=redis_config["health_check_interval"],
                max_connections=redis_config["connection_pool_size"]
            )
            # Test connection
            self.client.ping()
            self.is_connected = True
            logger.info("Redis connection established successfully")
        except Exception as e:
            logger.error(f"Failed to establish Redis connection: {e}")
            self.is_connected = False
            
    def _ensure_connection(self):
        """
        Ensure Redis connection is active, reconnect if needed
        """
        if not self.is_connected:
            self._connect()
            
        if not self.is_connected:
            raise redis.ConnectionError("Redis connection is not available")
            
        try:
            self.client.ping()
        except (redis.ConnectionError, redis.TimeoutError):
            logger.warning("Redis connection lost, attempting to reconnect")
            self._connect()
            if not self.is_connected:
                raise redis.ConnectionError("Failed to reconnect to Redis")
                
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        Set a key-value pair in Redis
        
        Args:
            key: The key to set
            value: The value to set (will be JSON serialized)
            expire: Expiration time in seconds (default: 1 hour)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            if self.client is None:
                return False
            serialized_value = json.dumps(value)
            return bool(self.client.setex(key, expire, serialized_value))
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis by key
        
        Args:
            key: The key to retrieve
            
        Returns:
            The deserialized value or None if not found
        """
        try:
            self._ensure_connection()
            if self.client is None:
                return None
            value = self.client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis
        
        Args:
            key: The key to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            if self.client is None:
                return False
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting key {key} from Redis: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis
        
        Args:
            key: The key to check
            
        Returns:
            True if key exists, False otherwise
        """
        try:
            self._ensure_connection()
            if self.client is None:
                return False
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking key {key} existence in Redis: {e}")
            return False
            
    def flush_all(self) -> bool:
        """
        Flush all keys from Redis (use with caution)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            if self.client is None:
                return False
            self.client.flushall()
            return True
        except Exception as e:
            logger.error(f"Error flushing Redis: {e}")
            return False
            
    @ttl_cache(maxsize=1000, ttl=300)
    def get_with_ttl_cache(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis with TTL cache decorator
        
        Args:
            key: The key to retrieve
            
        Returns:
            The deserialized value or None if not found
        """
        return self.get(key)

# Global instance
redis_client = RedisClient()