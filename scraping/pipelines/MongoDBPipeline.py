from pymongo import MongoClient
import logging

class MongoDBPipeline:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.settings = crawler.settings
        return pipeline

    def open_spider(self, spider):
        self.client = MongoClient(self.settings.get('MONGODB_URI'))
        self.db = self.client[self.settings.get('MONGODB_DATABASE')]
        self.collection = self.db[self.settings.get('MONGODB_COLLECTION')]
        self.logger.info("MongoDB connection established")

    def close_spider(self, spider):
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")

    def process_item(self, item, spider):
        try:
            self.collection.insert_one(dict(item))
            self.logger.debug(f"Inserted item into MongoDB: {dict(item)}")
        except Exception as e:
            self.logger.error(f"Error inserting item into MongoDB: {e}")
            raise
        return item