import logging
from typing import Dict, Any
from pymongo import MongoClient
from psycopg2 import connect
from psycopg2.extras import Json

class StreamProcessor:
    def __init__(self, mongo_uri: str, postgres_uri: str):
        self.mongo_client = MongoClient(mongo_uri)
        self.postgres_conn = connect(postgres_uri)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Stream processor initialized")

    def process_message(self, message: Dict[str, Any]):
        try:
            # Store raw data in MongoDB
            mongo_db = self.mongo_client['raw_data']
            mongo_collection = mongo_db['scraped_data']
            mongo_collection.insert_one(message)
            self.logger.debug(f"Stored raw data in MongoDB: {message}")

            # Process and store in PostgreSQL
            processed_data = self._transform_data(message)
            self._store_processed_data(processed_data)
            self.logger.debug(f"Stored processed data in PostgreSQL: {processed_data}")
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            raise

    def _transform_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw data into processed format"""
        return {
            'source_id': raw_data.get('id'),
            'data': raw_data.get('content'),
            'metadata': {
                'source': raw_data.get('source'),
                'timestamp': raw_data.get('timestamp')
            }
        }

    def _store_processed_data(self, processed_data: Dict[str, Any]):
        """Store processed data in PostgreSQL"""
        with self.postgres_conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO processed_data (source_id, data, metadata)
                VALUES (%s, %s, %s)
                ON CONFLICT (source_id) DO UPDATE SET
                    data = EXCLUDED.data,
                    metadata = EXCLUDED.metadata,
                    processed_at = NOW()
            """, (
                processed_data['source_id'],
                Json(processed_data['data']),
                Json(processed_data['metadata'])
            ))
            self.postgres_conn.commit()

    def close(self):
        self.mongo_client.close()
        self.postgres_conn.close()
        self.logger.info("Stream processor closed")

if __name__ == "__main__":
    import sys
    from streaming.kafka_consumers.main import KafkaDataConsumer
    logging.basicConfig(level=logging.INFO)
    
    processor = StreamProcessor(
        mongo_uri='mongodb://mongodb:27017',
        postgres_uri='postgresql://postgres:password@postgres:5432/processed_data'
    )
    
    def process_message(message: Dict[str, Any]):
        processor.process_message(message)
    
    consumer = KafkaDataConsumer(
        bootstrap_servers='kafka:9092',
        group_id='stream-processor',
        topics=['raw_data']
    )
    
    try:
        consumer.consume_messages(process_message)
    except KeyboardInterrupt:
        pass
    finally:
        processor.close()