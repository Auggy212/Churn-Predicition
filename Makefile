.PHONY: help install train test build run stop clean logs api-test setup

# Default target
help:
	@echo "Churn Prediction MLOps System - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  setup      - Complete system setup (install, train, build, run)"
	@echo "  install    - Install Python dependencies"
	@echo "  train      - Train the model (opens Jupyter notebook)"
	@echo ""
	@echo "Development:"
	@echo "  test       - Run unit tests"
	@echo "  lint       - Run code linting"
	@echo "  format     - Format code with black"
	@echo ""
	@echo "Docker Operations:"
	@echo "  build      - Build Docker image"
	@echo "  run        - Start all services with Docker Compose"
	@echo "  stop       - Stop all services"
	@echo "  logs       - View service logs"
	@echo "  clean      - Clean up Docker resources"
	@echo ""
	@echo "API Testing:"
	@echo "  api-test   - Test the API functionality"
	@echo ""
	@echo "Individual Services:"
	@echo "  api        - Run FastAPI locally (development)"
	@echo "  mlflow     - Start MLflow tracking server"
	@echo "  grafana    - Start Grafana (requires Docker)"

# Setup and installation
setup:
	@echo "🚀 Setting up Churn Prediction MLOps System..."
	python scripts/setup.py

install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

train:
	@echo "🎯 Running model training script..."
	python scripts/train_model.py

# Development
test:
	@echo "🧪 Running unit tests..."
	pytest tests/ -v

lint:
	@echo "🔍 Running code linting..."
	flake8 apps/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 apps/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "🎨 Formatting code..."
	black apps/

# Docker operations
build:
	@echo "🐳 Building Docker image..."
	docker build -t churn-prediction-api .

run:
	@echo "🚀 Starting all services..."
	docker-compose up -d

stop:
	@echo "🛑 Stopping all services..."
	docker-compose down

logs:
	@echo "📋 Viewing service logs..."
	docker-compose logs -f

clean:
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v --remove-orphans
	docker system prune -f

# API testing
api-test:
	@echo "🧪 Testing API functionality..."
	python scripts/test_api.py

# Individual services (development)
api:
	@echo "🚀 Running FastAPI locally..."
	uvicorn apps.main:app --reload --host 0.0.0.0 --port 8000

mlflow:
	@echo "🔬 Starting MLflow tracking server..."
	mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri sqlite:///mlruns.db

grafana:
	@echo "📈 Starting Grafana..."
	docker run -d --name grafana -p 3000:3000 grafana/grafana:latest 