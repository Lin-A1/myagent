"""
Database clients for PostgreSQL, Redis, MinIO, and Milvus
"""
import redis
import json
from typing import Any, Optional
from minio import Minio
from minio.error import S3Error
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

from app.database.config import settings

class RedisClient:
    """
    Redis client wrapper for caching and session storage
    """
    
    def __init__(self):
        self.client = redis.from_url(settings.REDIS_URL)
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """
        Set a key-value pair in Redis
        """
        try:
            serialized_value = json.dumps(value)
            return bool(self.client.setex(key, expire, serialized_value))
        except Exception:
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis by key
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except Exception:
            return None
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from Redis
        """
        try:
            return bool(self.client.delete(key))
        except Exception:
            return False

class MinIOClient:
    """
    MinIO client wrapper for object storage
    """
    
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
    
    def create_bucket(self, bucket_name: str) -> bool:
        """
        Create a bucket if it doesn't exist
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            return True
        except S3Error:
            return False

class MilvusClient:
    """
    Milvus client wrapper for vector storage and similarity search
    """
    
    def __init__(self):
        # Connect to Milvus
        connections.connect(
            alias="default", 
            host=settings.MILVUS_HOST, 
            port=settings.MILVUS_PORT
        )
    
    def create_collection(self, collection_name: str, fields: list) -> bool:
        """
        Create a collection in Milvus
        """
        try:
            if utility.has_collection(collection_name):
                return True
                
            schema = CollectionSchema(fields, f"Schema for {collection_name}")
            collection = Collection(collection_name, schema)
            return True
        except Exception:
            return False

# Global instances
redis_client = RedisClient()
minio_client = MinIOClient()
milvus_client = MilvusClient()