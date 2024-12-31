import logging
from typing import Dict, Any
from storage.redis.cache_configs.config import RedisCacheManager
from storage.postgresql.models.processed_data import ProcessedDataModel
from pymongo import MongoClient

class DataService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.redis_cache = RedisCacheManager('redis://redis:6379/0')
        self.mongo_client = MongoClient('mongodb://mongodb:27017')
        self.postgres_model = ProcessedDataModel(
            'postgresql://postgres:password@postgres:5432/processed_data'
        )
        self.logger.info("Data service initialized")

    def get_raw_data(self, item_id: str) -> Dict[str, Any]:
        """Get raw data from MongoDB"""
        try:
            db = self.mongo_client['raw_data']
            collection = db['scraped_data']
            data = collection.find_one({'_id': item_id})
            if data:
                return data
            raise ValueError("Item not found")
        except Exception as e:
            self.logger.error(f"Error getting raw data: {e}")
            raise

    def get_processed_data(self, source_id: str) -> Dict[str, Any]:
        """Get processed data from PostgreSQL"""
        try:
            return self.postgres_model.get_processed_data(source_id)
        except Exception as e:
            self.logger.error(f"Error getting processed data: {e}")
            raise

    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw data and store in PostgreSQL"""
        try:
            # Transform data
            processed_data = {
                'source_id': raw_data.get('id'),
                'data': raw_data.get('content'),
                'metadata': {
                    'source': raw_data.get('source'),
                    'timestamp': raw_data.get('timestamp')
                }
            }
            
            # Store processed data
            self.postgres_model.insert_processed_data(processed_data)
            
            # Cache processed data
            self.redis_cache.set(
                f"processed:{processed_data['source_id']}",
                processed_data
            )
            
            return processed_data
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            raise

    def close(self):
        self.redis_cache.close()
        self.mongo_client.close()
        self.postgres_model.close()
        self.logger.info("Data service connections closed")

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    service = DataService()
    
    try:
        # Example usage
        processed_data = service.process_data({
            'id': 'example-id',
            'content': {'key': 'value'},
            'source': 'example',
            'timestamp': '2024-01-01T00:00:00Z'
        })
        print(processed_data)
    finally:
        service.close()