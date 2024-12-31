BOT_NAME = 'data-pipeline'

SPIDER_MODULES = ['scraping.spiders']
NEWSPIDER_MODULE = 'scraping.spiders'

# Scrapy settings
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 1.0
ROBOTSTXT_OBEY = True

# Item pipelines
ITEM_PIPELINES = {
    'scraping.pipelines.KafkaPipeline': 100,
    'scraping.pipelines.MongoDBPipeline': 200,
}

# Kafka configuration
KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'scrapy-producer'
}

# MongoDB configuration
MONGODB_URI = 'mongodb://mongodb:27017'
MONGODB_DATABASE = 'raw_data'
MONGODB_COLLECTION = 'scraped_data'

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0