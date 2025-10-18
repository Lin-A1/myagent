"""
Milvus client for vector storage and similarity search with enhanced reliability
"""
import logging
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.database.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class MilvusClient:
    """
    Milvus client wrapper for vector storage and similarity search with enhanced reliability
    """
    
    def __init__(self):
        self.is_connected = False
        self._connect()
    
    def _connect(self):
        """
        Connect to Milvus
        """
        try:
            connections.connect(
                alias="default", 
                host=settings.MILVUS_HOST, 
                port=settings.MILVUS_PORT,
                timeout=10
            )
            self.is_connected = True
            logger.info("Milvus connection established successfully")
        except Exception as e:
            logger.error(f"Failed to establish Milvus connection: {e}")
            self.is_connected = False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        reraise=True
    )
    def _ensure_connection(self):
        """
        Ensure Milvus connection is active, reconnect if needed
        """
        if not self.is_connected:
            self._connect()
            
        if not self.is_connected:
            raise ConnectionError("Milvus connection is not available")
            
        try:
            utility.list_collections()
        except Exception:
            logger.warning("Milvus connection lost, attempting to reconnect")
            self._connect()
            if not self.is_connected:
                raise ConnectionError("Failed to reconnect to Milvus")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        reraise=True
    )
    def create_collection(self, collection_name: str, fields: list) -> bool:
        """
        Create a collection in Milvus
        
        Args:
            collection_name: Name of the collection
            fields: List of field schemas
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            if utility.has_collection(collection_name):
                return True
                
            schema = CollectionSchema(fields, f"Schema for {collection_name}")
            Collection(collection_name, schema)
            return True
        except Exception as e:
            logger.error(f"Error creating collection {collection_name} in Milvus: {e}")
            return False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        reraise=True
    )
    def insert_vectors(self, collection_name: str, data: list) -> bool:
        """
        Insert vectors into a collection
        
        Args:
            collection_name: Name of the collection
            data: List of vectors to insert
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            collection = Collection(collection_name)
            collection.insert(data)
            collection.flush()
            return True
        except Exception as e:
            logger.error(f"Error inserting vectors into collection {collection_name} in Milvus: {e}")
            return False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        reraise=True
    )
    def search_vectors(self, collection_name: str, query_vectors: list, limit: int = 10) -> list:
        """
        Search for similar vectors
        
        Args:
            collection_name: Name of the collection
            query_vectors: List of query vectors
            limit: Maximum number of results to return
            
        Returns:
            List of search results
        """
        try:
            self._ensure_connection()
            collection = Collection(collection_name)
            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10},
            }
            results = collection.search(
                data=query_vectors,
                anns_field="embedding",
                param=search_params,
                limit=limit,
                expr=None,
                consistency_level="Strong"
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vectors in collection {collection_name} in Milvus: {e}")
            return []
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception)),
        reraise=True
    )
    def drop_collection(self, collection_name: str) -> bool:
        """
        Drop a collection from Milvus
        
        Args:
            collection_name: Name of the collection to drop
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            if utility.has_collection(collection_name):
                utility.drop_collection(collection_name)
            return True
        except Exception as e:
            logger.error(f"Error dropping collection {collection_name} in Milvus: {e}")
            return False

# Global instance
milvus_client = MilvusClient()