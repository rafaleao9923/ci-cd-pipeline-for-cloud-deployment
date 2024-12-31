from kafka import KafkaProducer
import json
import logging

class KafkaPipeline:
    def __init__(self):
        self.producer = None
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.settings = crawler.settings
        return pipeline

    def open_spider(self, spider):
        self.producer = KafkaProducer(
            bootstrap_servers=self.settings.get('KAFKA_PRODUCER_CONFIG')['bootstrap.servers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            client_id=self.settings.get('KAFKA_PRODUCER_CONFIG')['client.id']
        )
        self.logger.info("Kafka producer initialized")

    def close_spider(self, spider):
        if self.producer:
            self.producer.close()
            self.logger.info("Kafka producer closed")

    def process_item(self, item, spider):
        try:
            self.producer.send(
                topic='raw_data',
                value=dict(item)
            )
            self.logger.debug(f"Sent item to Kafka: {dict(item)}")
        except Exception as e:
            self.logger.error(f"Error sending item to Kafka: {e}")
            raise
        return item