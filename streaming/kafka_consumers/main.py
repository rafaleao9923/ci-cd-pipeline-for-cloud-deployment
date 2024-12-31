from kafka import KafkaConsumer
import json
import logging
from typing import Dict, Any

class KafkaDataConsumer:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: list):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=True,
            auto_offset_reset='earliest'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Kafka consumer initialized")

    def consume_messages(self, process_message: callable):
        try:
            for message in self.consumer:
                try:
                    process_message(message.value)
                    self.logger.debug(f"Processed message: {message.value}")
                except Exception as e:
                    self.logger.error(f"Error processing message: {e}")
        except KeyboardInterrupt:
            self.logger.info("Consumer interrupted")
        finally:
            self.close()

    def close(self):
        self.consumer.close()
        self.logger.info("Kafka consumer closed")

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    def process_message(message: Dict[str, Any]):
        print(f"Processing message: {message}")
    
    consumer = KafkaDataConsumer(
        bootstrap_servers='kafka:9092',
        group_id='data-processor',
        topics=['raw_data']
    )
    
    try:
        consumer.consume_messages(process_message)
    except KeyboardInterrupt:
        pass