# Future Market

A sophisticated market analysis and prediction system that combines real-time market data, sentiment analysis, and machine learning to provide insights into market trends and predictions.

## Overview

This project is a comprehensive market analysis platform that includes:
- Real-time market data collection
- Sentiment analysis from news sources
- Feature engineering pipeline
- Machine learning models for market prediction
- Vector database for semantic search
- Message queue for data processing

## Architecture

The system consists of several microservices:

1. **Data Pipeline**: Collects market data and news sentiment
2. **Data CDC (Change Data Capture)**: Handles data synchronization
3. **Feature Pipeline**: Processes and engineers features for ML models
4. **Core Services**:
   - MongoDB (Replica Set) for data storage
   - RabbitMQ for message queuing
   - Qdrant for vector storage and semantic search

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Poetry for Python dependency management

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd future-market
   ```

2. Create and activate a virtual environment:
   ```bash
   make init
   make install
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required environment variables

4. Start the infrastructure:
   ```bash
   make local-start
   ```

## Available Commands

- `make init`: Setup Poetry virtual environment
- `make install`: Install dependencies
- `make local-start`: Start Docker infrastructure
- `make local-stop`: Stop Docker infrastructure
- `make local-restart`: Restart Docker infrastructure
- `make local-fetch`: Fetch stock data and sentiment news
- `make local-run`: Run the pipelines

## Project Structure

```
future-market/
├── src/
│   ├── data_cdc/        # Change Data Capture service
│   ├── data_pipeline/   # Data collection and processing
│   ├── feature_pipeline/# Feature engineering
│   ├── core/           # Core business logic
│   └── utils/          # Utility functions
├── notebooks/          # Jupyter notebooks for analysis
├── rabbitmq/          # RabbitMQ configuration
├── .docker/           # Docker configuration files
├── docker-compose.yml # Service orchestration
├── pyproject.toml     # Python dependencies
└── Makefile          # Build and run commands
```

## Dependencies

Key dependencies include:
- structlog: Structured logging
- pydantic: Data validation
- pandas: Data manipulation
- langchain: LLM integration
- bytewax: Data processing
- torch: Deep learning
- sentence-transformers: Text embeddings
- statsmodels: Statistical analysis
- seaborn & matplotlib: Data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT]