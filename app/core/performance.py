"""
Performance optimization utilities for the LLM Agent Platform
"""
import time
import functools
import logging
import asyncio
from typing import Any, Dict, Callable
from collections import OrderedDict

# Configure logging
logger = logging.getLogger(__name__)

# Connection pool configurations
CONNECTION_POOL_CONFIG = {
    "redis": {
        "connection_pool_size": 20,
        "retry_on_timeout": True,
        "socket_keepalive": True,
        "health_check_interval": 30
    },
    "database": {
        "pool_size": 20,
        "max_overflow": 10,
        "pool_recycle": 3600,
        "pool_pre_ping": True
    },
    "http": {
        "max_keepalive_connections": 20,
        "max_connections": 100,
        "keepalive_expiry": 5.0
    }
}

class PerformanceOptimizer:
    """
    Performance optimization utilities
    """
    
    def __init__(self):
        self.request_count = 0
        self.cache_hit_count = 0
        self.response_times = []
        
    def record_request(self):
        """Record a request"""
        self.request_count += 1
        
    def record_cache_hit(self):
        """Record a cache hit"""
        self.cache_hit_count += 1
        
    def record_response_time(self, response_time: float):
        """Record response time"""
        self.response_times.append(response_time)
        # Keep only the last 1000 response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
            
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
        else:
            avg_response_time = 0
            min_response_time = 0
            max_response_time = 0
            
        cache_hit_rate = (
            self.cache_hit_count / self.request_count 
            if self.request_count > 0 else 0
        )
        
        return {
            "request_count": self.request_count,
            "cache_hit_count": self.cache_hit_count,
            "cache_hit_rate": cache_hit_rate,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time
        }

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

def measure_time(func: Callable) -> Callable:
    """
    Decorator to measure execution time of a function
    """
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            performance_optimizer.record_response_time(execution_time)
            logger.debug(f"{func.__name__} executed in {execution_time:.4f} seconds")
            
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            performance_optimizer.record_response_time(execution_time)
            logger.debug(f"{func.__name__} executed in {execution_time:.4f} seconds")
            
    # Check if the function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

class TTLCache:
    """
    Simple TTL (Time To Live) cache implementation
    """
    
    def __init__(self, maxsize: int = 128, ttl: int = 300):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()
        
    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a key from the function arguments
            key = str(args) + str(sorted(kwargs.items()))
            
            # Check if we have a cached result
            if key in self.cache:
                result, timestamp = self.cache[key]
                # Check if the cached result is still valid
                if time.time() - timestamp < self.ttl:
                    # Move to end to mark as recently used
                    self.cache.move_to_end(key)
                    return result
                else:
                    # Remove expired entry
                    del self.cache[key]
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            self.cache[key] = (result, time.time())
            
            # Remove oldest entries if cache is full
            while len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
                
            return result
        return wrapper

# Convenience function for TTL cache
def ttl_cache(maxsize: int = 128, ttl: int = 300):
    """
    Create a TTL cache decorator
    
    Args:
        maxsize: Maximum number of entries in the cache
        ttl: Time to live in seconds
    """
    return TTLCache(maxsize, ttl)