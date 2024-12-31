from kafka import KafkaProducer
import json
import logging
from typing import Dict, Any

class KafkaDataProducer:
    def __init__(self, bootstrap_servers: str, client_id: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            client_id=client_id
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Kafka producer initialized")

    def send_message(self, topic: str, message: Dict[str, Any]):
        try:
            future = self.producer.send(topic, value=message)
            future.get(timeout=10)
            self.logger.debug(f"Message sent to topic {topic}: {message}")
        except Exception as e:
            self.logger.error(f"Error sending message to Kafka: {e}")
            raise

    def close(self):
        self.producer.close()
        self.logger.info("Kafka producer closed")

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    producer = KafkaDataProducer(
        bootstrap_servers='kafka:9092',
        client_id='data-producer'
    )
    
    try:
        # Example usage
        producer.send_message('raw_data', {'key': 'value'})
    finally:
        producer.close()