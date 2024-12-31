from fastapi import FastAPI, HTTPException
from typing import Optional, Dict, Any
import logging
from storage.redis.cache_configs.config import RedisCacheManager
from storage.postgresql.models.processed_data import ProcessedDataModel
from storage.mongodb.schemas.raw_data_schema import RawDataSchema
from pymongo import MongoClient
from psycopg2 import connect

app = FastAPI()
logger = logging.getLogger(__name__)

# Initialize connections
redis_cache = RedisCacheManager('redis://redis:6379/0')
mongo_client = MongoClient('mongodb://mongodb:27017')
postgres_conn = connect('postgresql://postgres:password@postgres:5432/processed_data')

@app.on_event("shutdown")
def shutdown_event():
    redis_cache.close()
    mongo_client.close()
    postgres_conn.close()
    logger.info("API connections closed")

@app.get("/data/raw/{item_id}")
async def get_raw_data(item_id: str):
    """Get raw data from MongoDB"""
    try:
        db = mongo_client['raw_data']
        collection = db['scraped_data']
        data = collection.find_one({'_id': item_id})
        if data:
            return data
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error getting raw data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/data/processed/{source_id}")
async def get_processed_data(source_id: str):
    """Get processed data from PostgreSQL"""
    try:
        with postgres_conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM processed_data WHERE source_id = %s
            """, (source_id,))
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'source_id': result[1],
                    'processed_at': result[2],
                    'data': result[3],
                    'metadata': result[4]
                }
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        logger.error(f"Error getting processed data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/cache/{key}")
async def get_cache(key: str):
    """Get cached data"""
    try:
        data = redis_cache.get(key)
        if data:
            return data
        raise HTTPException(status_code=404, detail="Cache not found")
    except Exception as e:
        logger.error(f"Error getting cache: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/cache/{key}")
async def set_cache(key: str, value: Dict[str, Any], ttl: int = 3600):
    """Set cached data"""
    try:
        success = redis_cache.set(key, value, ttl)
        if success:
            return {"message": "Cache set successfully"}
        raise HTTPException(status_code=500, detail="Failed to set cache")
    except Exception as e:
        logger.error(f"Error setting cache: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check MongoDB connection
        mongo_client.admin.command('ping')
        
        # Check PostgreSQL connection
        with postgres_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Check Redis connection
        redis_cache.get('health_check')
        
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Service unavailable")