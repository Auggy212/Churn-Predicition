# CI/CD Pipeline for Churn Prediction MLOps

This document describes the complete CI/CD pipeline setup for the Churn Prediction MLOps project using GitHub Actions.

## 🚀 Pipeline Overview

The CI/CD pipeline consists of multiple workflows that handle different aspects of the development and deployment process:

### **1. Main CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
- **Code Quality**: Linting, formatting, and testing
- **Model Training**: Automated model training and evaluation
- **Docker Builds**: Building and pushing container images
- **Security Scanning**: Vulnerability assessment
- **Deployment**: Staging and production deployments

### **2. Model Retraining** (`.github/workflows/model-retraining.yml`)
- **Scheduled Retraining**: Weekly model retraining
- **Manual Trigger**: On-demand retraining
- **Performance Evaluation**: Model performance assessment

### **3. Security Scanning** (`.github/workflows/security-scan.yml`)
- **Daily Scans**: Automated security assessments
- **Dependency Scanning**: Vulnerability checks
- **Code Security**: Static analysis

## 📋 Prerequisites

### **GitHub Repository Setup**
1. **Enable GitHub Actions**: Go to Settings → Actions → General
2. **Set up Environments**: Create `staging` and `production` environments
3. **Configure Secrets**: Add necessary secrets for deployment

### **Required Secrets**
```bash
# GitHub Container Registry
GITHUB_TOKEN (automatically available)

# Kubernetes (if using K8s deployment)
KUBE_CONFIG_DATA
KUBE_CONTEXT

# Cloud Provider (if using cloud deployment)
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AZURE_CREDENTIALS
GCP_SA_KEY
```

## 🔧 Pipeline Stages

### **Stage 1: Code Quality & Testing**
```yaml
- Linting with flake8
- Code formatting with black
- Unit tests with pytest
- Coverage reporting
- Frontend testing and build
```

### **Stage 2: Model Training**
```yaml
- Install dependencies
- Train ML model
- Evaluate performance
- Upload model artifacts
```

### **Stage 3: Container Builds**
```yaml
- Build backend Docker image
- Build frontend Docker image
- Push to GitHub Container Registry
- Cache layers for faster builds
```

### **Stage 4: Security Scanning**
```yaml
- Trivy vulnerability scanning
- Bandit security analysis
- Safety dependency check
- Upload results to GitHub Security
```

### **Stage 5: Deployment**
```yaml
- Deploy to staging (develop branch)
- Deploy to production (main branch)
- Health checks and monitoring
```

## 🎯 Usage

### **Automatic Triggers**
- **Push to main**: Full pipeline with production deployment
- **Push to develop**: Full pipeline with staging deployment
- **Pull Request**: Testing and security scanning only

### **Manual Triggers**
```bash
# Trigger full pipeline
gh workflow run ci-cd.yml

# Trigger model retraining
gh workflow run model-retraining.yml

# Trigger security scan
gh workflow run security-scan.yml
```

### **Scheduled Jobs**
- **Model Retraining**: Every Sunday at 2 AM UTC
- **Security Scanning**: Daily at 6 AM UTC

## 🐳 Container Images

### **Image Tags**
- **Latest**: `ghcr.io/username/repo/backend:latest`
- **Versioned**: `ghcr.io/username/repo/backend:v1.0.0`
- **Commit-based**: `ghcr.io/username/repo/backend:sha-abc123`

### **Image Security**
- Multi-stage builds for smaller images
- Non-root user execution
- Security scanning with Trivy
- Base image vulnerability checks

## ☸️ Kubernetes Deployment

### **Deployment Files**
- `k8s/namespace.yml`: Project namespace
- `k8s/backend-deployment.yml`: API deployment
- `k8s/frontend-deployment.yml`: Frontend deployment
- `k8s/monitoring.yml`: Prometheus & Grafana

### **Deployment Commands**
```bash
# Deploy to staging
kubectl apply -f k8s/ --namespace=churn-prediction-staging

# Deploy to production
kubectl apply -f k8s/ --namespace=churn-prediction-production

# Check deployment status
kubectl get pods -n churn-prediction
```

## 📊 Monitoring & Observability

### **Prometheus Metrics**
- HTTP request rates
- Response times
- Error rates
- Model performance metrics

### **Grafana Dashboards**
- Real-time system monitoring
- Model performance tracking
- API usage analytics
- Error rate alerts

### **Health Checks**
- Liveness probes for container health
- Readiness probes for service availability
- Custom health endpoints

## 🔒 Security Features

### **Code Security**
- Static analysis with Bandit
- Dependency vulnerability scanning
- Container image security scanning
- Secret scanning

### **Infrastructure Security**
- Non-root container execution
- Resource limits and requests
- Network policies
- RBAC configuration

## 🚨 Alerts & Notifications

### **Pipeline Notifications**
- Success/failure notifications
- Deployment status updates
- Security scan results
- Model performance alerts

### **Monitoring Alerts**
- High error rates
- Slow response times
- Resource usage thresholds
- Model performance degradation

## 🔧 Customization

### **Environment Variables**
```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
  PYTHON_VERSION: 3.9
  NODE_VERSION: 18
```

### **Resource Limits**
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### **Deployment Strategies**
- **Rolling Update**: Zero-downtime deployments
- **Blue-Green**: Traffic switching
- **Canary**: Gradual rollout

## 📈 Performance Optimization

### **Build Optimization**
- Docker layer caching
- Multi-stage builds
- Parallel job execution
- Dependency caching

### **Deployment Optimization**
- Health check optimization
- Resource allocation
- Auto-scaling configuration
- Load balancing

## 🛠️ Troubleshooting

### **Common Issues**
1. **Build Failures**: Check dependency versions
2. **Test Failures**: Verify test environment
3. **Deployment Issues**: Check Kubernetes configuration
4. **Security Failures**: Review vulnerability reports

### **Debug Commands**
```bash
# Check workflow status
gh run list

# View workflow logs
gh run view --log

# Check pod status
kubectl describe pod <pod-name> -n churn-prediction

# Check service endpoints
kubectl get endpoints -n churn-prediction
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure all tests pass
5. Submit a pull request

The CI/CD pipeline will automatically test your changes and provide feedback. 