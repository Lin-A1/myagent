#!/bin/bash

# Stop script for LLM Agent Platform

echo "Stopping LLM Agent Platform..."

# Stop all services
docker-compose down

echo "LLM Agent Platform stopped!"