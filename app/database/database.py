"""
Database connection and session management with enhanced reliability and performance optimization
"""
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.database.config import settings
from app.core.performance import CONNECTION_POOL_CONFIG

# Configure logging
logger = logging.getLogger(__name__)

# Create database engine with connection pooling and retry configuration
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=CONNECTION_POOL_CONFIG["database"]["pool_pre_ping"],
    pool_recycle=CONNECTION_POOL_CONFIG["database"]["pool_recycle"],
    pool_size=CONNECTION_POOL_CONFIG["database"]["pool_size"],
    max_overflow=CONNECTION_POOL_CONFIG["database"]["max_overflow"],
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

class DatabaseManager:
    """
    Manager for database operations with enhanced reliability and fault recovery
    """
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        self.is_connected = False
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((SQLAlchemyError, OSError)),
        reraise=True
    )
    def connect(self):
        """
        Establish database connection with retry mechanism
        """
        try:
            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute("SELECT 1")
                result.fetchone()
            self.is_connected = True
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Failed to establish database connection: {e}")
            raise
            
    def disconnect(self):
        """
        Close database connection
        """
        try:
            self.engine.dispose()
            self.is_connected = False
            logger.info("Database connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((SQLAlchemyError, OSError)),
        reraise=True
    )
    def get_db(self):
        """
        Dependency to get a database session with retry mechanism
        """
        db = self.SessionLocal()
        try:
            yield db
        except SQLAlchemyError as e:
            logger.error(f"Database session error: {e}")
            db.rollback()
            raise
        finally:
            try:
                db.close()
            except Exception as e:
                logger.warning(f"Error closing database session: {e}")

# Global database manager instance
db_manager = DatabaseManager()