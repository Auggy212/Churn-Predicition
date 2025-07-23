# Churn Prediction MLOps System

A comprehensive end-to-end machine learning system for customer churn prediction with full MLOps pipeline implementation.

## 🎯 Project Overview

This project demonstrates a complete MLOps workflow including:
- **Data Preparation & Model Training** (Jupyter + scikit-learn)
- **Experiment Tracking** (MLflow)
- **API Deployment** (FastAPI)
- **Containerization** (Docker)
- **CI/CD Pipeline** (GitHub Actions)
- **Monitoring** (Prometheus + Grafana)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Jupyter       │    │   FastAPI       │    │   Prometheus    │
│   Notebook      │───▶│   Application   │───▶│   Metrics       │
│   (Training)    │    │   (Prediction)  │    │   Collection    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MLflow        │    │   Docker        │    │   Grafana       │
│   Tracking      │    │   Container     │    │   Dashboard     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
project-root/
├── apps/
│   ├── main.py              # FastAPI application
│   └── __init__.py
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── App.js          # Main app component
│   │   └── index.js        # React entry point
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container
│   └── nginx.conf          # Nginx configuration
├── scripts/
│   ├── train_model.py       # Model training script
│   ├── test_api.py          # API testing script
│   └── setup.py             # Setup script
├── models/                  # Trained models
├── tests/
│   └── test_api.py         # Unit tests
├── grafana/
│   ├── dashboards/         # Grafana dashboards
│   └── datasources/        # Data source configs
├── Dockerfile              # Backend container configuration
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Python dependencies
├── prometheus.yml          # Prometheus configuration
├── .github/workflows/      # CI/CD pipeline
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- Docker & Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd churn-prediction-mlops
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Train the model
python scripts/train_model.py
```

### 3. Frontend Setup

```bash
# Install frontend dependencies
cd frontend
npm install

# Start frontend development server
npm start
```

### 4. Run with Docker Compose (Full Stack)

```bash
# Start all services including frontend
docker-compose up -d

# Check services
docker-compose ps
```

### 5. Access Services

- **Frontend App**: http://localhost:3000
- **FastAPI App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MLflow**: http://localhost:5000

## 📊 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Make Predictions

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "tenure": 12,
       "monthly_charges": 50.0,
       "total_charges": 600.0,
       "contract_type": "Month-to-month",
       "payment_method": "Electronic check",
       "internet_service": "DSL",
       "customer_service_calls": 2
     }'
```

### Response Format

```json
{
  "churn_prediction": false,
  "churn_probability": 0.23,
  "confidence": 0.77,
  "model_version": "1.0.0"
}
```

## 🔧 Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Linting
flake8 apps/

# Formatting
black apps/
```

### Local Development

```bash
# Run FastAPI locally
uvicorn apps.main:app --reload --host 0.0.0.0 --port 8000
```

## 📈 Monitoring

### Grafana Dashboard

The system includes a pre-configured Grafana dashboard with:
- Request rate monitoring
- Response time tracking
- Error rate alerts
- Prediction endpoint usage

### Prometheus Metrics

Key metrics collected:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration
- `http_requests_in_progress` - Active requests

## 🔄 CI/CD Pipeline

The GitHub Actions workflow includes:
1. **Code Quality**: Linting with flake8 and black
2. **Testing**: Unit tests with pytest
3. **Docker Build**: Container image creation
4. **Deployment**: Automated deployment (configurable)

## 📋 Model Information

### Features Used

- **Numerical**: tenure, monthly_charges, total_charges, customer_service_calls
- **Categorical**: contract_type, payment_method, internet_service
- **Derived**: tenure_monthly_ratio, total_monthly_ratio
- **Binary**: is_month_to_month, is_electronic_check, has_internet

### Model Performance

- **Accuracy**: ~85%
- **Precision**: ~80%
- **Recall**: ~75%
- **ROC-AUC**: ~0.85

## 🛠️ Configuration

### Environment Variables

```bash
# API Configuration
PORT=8000
PYTHONPATH=/app

# MLflow Configuration
MLFLOW_TRACKING_URI=sqlite:///mlruns.db

# Grafana Configuration
GF_SECURITY_ADMIN_PASSWORD=admin
```

### Docker Configuration

The system uses multi-stage Docker builds for optimization:
- Base image: Python 3.9-slim
- Health checks included
- Non-root user for security

## 🔍 Troubleshooting

### Common Issues

1. **Model not loading**: Ensure the model file exists in `models/` directory
2. **Port conflicts**: Check if ports 8000, 3000, 9090, 5000 are available
3. **Docker issues**: Ensure Docker and Docker Compose are running

### Logs

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs churn-api
docker-compose logs grafana
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

This project was developed as part of an MLOps assignment demonstrating:
- Version control with Git
- Experiment tracking with MLflow
- API development with FastAPI
- Containerization with Docker
- CI/CD with GitHub Actions
- Monitoring with Prometheus and Grafana 