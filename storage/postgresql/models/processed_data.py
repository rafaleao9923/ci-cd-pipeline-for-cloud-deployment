from psycopg2 import connect
from psycopg2.extras import Json
from typing import Dict, Any
import logging

class ProcessedDataModel:
    def __init__(self, postgres_uri: str):
        self.conn = connect(postgres_uri)
        self.logger = logging.getLogger(__name__)
        self._create_schema()

    def _create_schema(self):
        """Create processed data table schema and indexes"""
        with self.conn.cursor() as cursor:
            # Create processed_data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_data (
                    id SERIAL PRIMARY KEY,
                    source_id VARCHAR(255) NOT NULL,
                    processed_at TIMESTAMPTZ DEFAULT NOW(),
                    data JSONB NOT NULL,
                    metadata JSONB,
                    CONSTRAINT unique_source UNIQUE (source_id)
                )
            """)
            
            # Create GIN index on metadata
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_data_metadata
                ON processed_data USING GIN (metadata)
            """)
            
            self.conn.commit()
            self.logger.info("Processed data schema created")

    def insert_processed_data(self, data: Dict[str, Any]):
        """Insert processed data into PostgreSQL"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO processed_data (source_id, data, metadata)
                VALUES (%s, %s, %s)
                ON CONFLICT (source_id) DO UPDATE SET
                    data = EXCLUDED.data,
                    metadata = EXCLUDED.metadata,
                    processed_at = NOW()
            """, (
                data['source_id'],
                Json(data['data']),
                Json(data['metadata'])
            ))
            self.conn.commit()
            self.logger.debug(f"Inserted processed data: {data}")

    def close(self):
        self.conn.close()
        self.logger.info("PostgreSQL connection closed")

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    model = ProcessedDataModel(
        postgres_uri='postgresql://postgres:password@postgres:5432/processed_data'
    )
    
    try:
        # Example usage
        model.insert_processed_data({
            'source_id': 'example-id',
            'data': {'key': 'value'},
            'metadata': {'source': 'example'}
        })
    finally:
        model.close()