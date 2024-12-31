# Project File Structure

## Project File Structure
```
data-pipeline-deployment/
├── scraping/                # Scrapy spiders and related components
│   ├── spiders/             # Spider implementations
│   ├── middlewares/         # Scrapy middlewares
│   ├── pipelines/           # Data processing pipelines
│   └── settings/            # Scrapy configuration
├── streaming/               # Kafka streaming components
│   ├── kafka_producers/     # Kafka producers
│   ├── kafka_consumers/     # Kafka consumers
│   └── stream_processors/   # Stream processing logic
├── storage/                 # Data storage components
│   ├── mongodb/             # MongoDB configurations
│   ├── postgresql/          # PostgreSQL configurations
│   └── redis/               # Redis configurations
├── api/                     # API layer components
│   ├── endpoints/           # API endpoints
│   ├── models/              # Data models
│   └── services/            # Business logic
├── pipeline/                # CI/CD pipeline configurations
│   ├── github_actions/      # GitHub Actions workflows
│   └── scripts/             # Deployment and maintenance scripts
├── kubernetes/              # Kubernetes deployment configurations
│   ├── scrapy/              # Scrapy deployment
│   ├── kafka/               # Kafka deployment
│   ├── mongodb/             # MongoDB deployment
│   ├── postgresql/          # PostgreSQL deployment
│   └── redis/               # Redis deployment
├── monitoring/              # Monitoring configurations
│   ├── prometheus/          # Prometheus configurations
│   ├── grafana/             # Grafana dashboards
│   └── alerts/              # Alert configurations
├── docker/                  # Docker configurations
│   ├── scrapy/              # Scrapy Dockerfiles
│   ├── stream_processor/    # Stream processor Dockerfiles
│   └── api/                 # API Dockerfiles
└── tests/                   # Test suites
    ├── spiders/             # Spider tests
    ├── processors/          # Stream processor tests
    └── integration/         # Integration tests
```

## Key Files and Their Roles

### Data Collection
- `scraping/spiders/base_spider.py`: Base spider implementation
- `scraping/settings/settings.py`: Scrapy configuration
- `scraping/pipelines/KafkaPipeline.py`: Pipeline for sending data to Kafka

### Stream Processing
- `streaming/kafka_producers/main.py`: Kafka producer implementation
- `streaming/stream_processors/processor.py`: Stream processing logic

### Data Storage
- `storage/mongodb/schemas/raw_data_schema.py`: MongoDB schema definitions
- `storage/postgresql/models/processed_data.py`: PostgreSQL data models
- `storage/redis/cache_configs/config.py`: Redis cache configuration

### API Layer
- `api/endpoints/data_endpoints.py`: API endpoints for data access
- `api/services/data_service.py`: Business logic for data processing

### Infrastructure
- `kubernetes/scrapy/deployment.yaml`: Scrapy deployment configuration
- `kubernetes/kafka/statefulset.yaml`: Kafka deployment configuration
- `docker/scrapy/Dockerfile`: Scrapy Dockerfile

### Monitoring
- `monitoring/prometheus/pipeline-metrics.yaml`: Prometheus metrics configuration
- `monitoring/grafana/dashboards/pipeline_health.json`: Grafana dashboard

### CI/CD
- `pipeline/github_actions/deploy_pipeline.yml`: Deployment pipeline
- `pipeline/scripts/rollback.sh`: Rollback script

## File Connections
1. **Data Flow**
   - Scrapy spiders (`scraping/spiders/`) send data to Kafka via `KafkaPipeline.py`
   - Kafka consumers (`streaming/kafka_consumers/`) process data and store in MongoDB/PostgreSQL
   - API layer (`api/`) accesses data from storage and serves to clients

2. **Infrastructure**
   - Dockerfiles (`docker/`) define container images
   - Kubernetes configurations (`kubernetes/`) manage deployments
   - Monitoring configurations (`monitoring/`) track system health

3. **Development Process**
   - CI/CD configurations (`pipeline/`) automate testing and deployment
   - Test suites (`tests/`) ensure code quality and system reliability