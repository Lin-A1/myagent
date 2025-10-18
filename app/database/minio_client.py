"""
MinIO client for object storage with enhanced reliability
"""
import logging
from minio import Minio
from minio.error import S3Error
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.database.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class MinIOClient:
    """
    MinIO client wrapper for object storage with enhanced reliability
    """
    
    def __init__(self):
        self.client = None
        self.is_connected = False
        self._connect()
    
    def _connect(self):
        """
        Establish MinIO connection
        """
        try:
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False,  # Set to True if using HTTPS
                region="us-east-1"  # Default region
            )
            # Test connection by listing buckets
            self.client.list_buckets()
            self.is_connected = True
            logger.info("MinIO connection established successfully")
        except Exception as e:
            logger.error(f"Failed to establish MinIO connection: {e}")
            self.is_connected = False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((S3Error, ConnectionError)),
        reraise=True
    )
    def _ensure_connection(self):
        """
        Ensure MinIO connection is active, reconnect if needed
        """
        if not self.is_connected:
            self._connect()
            
        if not self.is_connected:
            raise ConnectionError("MinIO connection is not available")
            
        try:
            self.client.list_buckets()
        except (S3Error, ConnectionError):
            logger.warning("MinIO connection lost, attempting to reconnect")
            self._connect()
            if not self.is_connected:
                raise ConnectionError("Failed to reconnect to MinIO")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((S3Error, ConnectionError)),
        reraise=True
    )
    def create_bucket(self, bucket_name: str) -> bool:
        """
        Create a bucket if it doesn't exist
        
        Args:
            bucket_name: Name of the bucket to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            return True
        except S3Error as e:
            logger.error(f"Error creating bucket {bucket_name} in MinIO: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating bucket {bucket_name} in MinIO: {e}")
            return False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((S3Error, ConnectionError)),
        reraise=True
    )
    def upload_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        Upload a file to MinIO
        
        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object in MinIO
            file_path: Path to the local file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            self.client.fput_object(bucket_name, object_name, file_path)
            return True
        except S3Error as e:
            logger.error(f"Error uploading file {file_path} to MinIO bucket {bucket_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error uploading file {file_path} to MinIO bucket {bucket_name}: {e}")
            return False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((S3Error, ConnectionError)),
        reraise=True
    )
    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        Download a file from MinIO
        
        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object in MinIO
            file_path: Path to save the downloaded file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            self.client.fget_object(bucket_name, object_name, file_path)
            return True
        except S3Error as e:
            logger.error(f"Error downloading file {object_name} from MinIO bucket {bucket_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error downloading file {object_name} from MinIO bucket {bucket_name}: {e}")
            return False
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((S3Error, ConnectionError)),
        reraise=True
    )
    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        Delete a file from MinIO
        
        Args:
            bucket_name: Name of the bucket
            object_name: Name of the object in MinIO
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_connection()
            self.client.remove_object(bucket_name, object_name)
            return True
        except S3Error as e:
            logger.error(f"Error deleting file {object_name} from MinIO bucket {bucket_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting file {object_name} from MinIO bucket {bucket_name}: {e}")
            return False

# Global instance
minio_client = MinIOClient()