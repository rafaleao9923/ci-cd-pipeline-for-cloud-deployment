from pymongo import MongoClient
from datetime import datetime

class RawDataSchema:
    def __init__(self, mongo_uri: str, database: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[database]
        self._create_schema()

    def _create_schema(self):
        """Create schema and indexes for raw data collection"""
        collection = self.db['scraped_data']
        
        # Create schema validation
        validator = {
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['url', 'content', 'timestamp'],
                'properties': {
                    'url': {
                        'bsonType': 'string',
                        'description': 'must be a string and is required'
                    },
                    'content': {
                        'bsonType': 'object',
                        'description': 'must be an object and is required'
                    },
                    'timestamp': {
                        'bsonType': 'date',
                        'description': 'must be a date and is required'
                    },
                    'metadata': {
                        'bsonType': 'object',
                        'properties': {
                            'source': {'bsonType': 'string'},
                            'tags': {
                                'bsonType': 'array',
                                'items': {'bsonType': 'string'}
                            }
                        }
                    }
                }
            }
        }
        
        # Apply schema validation
        self.db.command('collMod', 'scraped_data', validator=validator)
        
        # Create indexes
        collection.create_index([('timestamp', -1)])
        collection.create_index([('url', 1)], unique=True)

    def close(self):
        self.client.close()

if __name__ == "__main__":
    schema = RawDataSchema(
        mongo_uri='mongodb://mongodb:27017',
        database='raw_data'
    )
    schema.close()