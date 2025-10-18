#!/bin/bash

# Start script for LLM Agent Platform

echo "Starting LLM Agent Platform..."

# Build and start all services
docker-compose up -d

echo "LLM Agent Platform started!"
echo "Services:"
echo "  - Nginx (Load Balancer): http://localhost"
echo "  - App Instances: http://localhost:8001, http://localhost:8002, http://localhost:8003"
echo "  - PostgreSQL: localhost:5432"
echo "  - Redis: localhost:6379"
echo "  - MinIO: http://localhost:9000"
echo "  - Milvus: localhost:19530"