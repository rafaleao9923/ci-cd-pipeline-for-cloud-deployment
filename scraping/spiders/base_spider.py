import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from kafka import KafkaProducer
import json

class BaseSpider(scrapy.Spider):
    name = 'base_spider'
    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 1.0,
        'ROBOTSTXT_OBEY': True
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kafka_producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def parse(self, response):
        """Override this method to implement custom parsing logic"""
        raise NotImplementedError("parse method must be implemented in child class")

    def send_to_kafka(self, topic, data):
        """Send scraped data to Kafka topic"""
        self.kafka_producer.send(topic, value=data)

    def closed(self, reason):
        """Clean up resources when spider is closed"""
        self.kafka_producer.close()
        super().closed(reason)

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(BaseSpider)
    process.start()