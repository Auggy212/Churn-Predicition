#!/usr/bin/env python3
"""
Setup script for the Churn Prediction MLOps System
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    required_tools = {
        "python": "python --version",
        "pip": "pip --version",
        "docker": "docker --version",
        "docker-compose": "docker-compose --version"
    }
    
    missing_tools = []
    
    for tool, command in required_tools.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            print(f"✅ {tool} is installed")
        except subprocess.CalledProcessError:
            print(f"❌ {tool} is not installed")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n⚠️  Missing tools: {', '.join(missing_tools)}")
        print("Please install the missing tools before continuing.")
        return False
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def train_model():
    """Train the model using the Python script"""
    print("🎯 Training the model...")
    
    # Check if model already exists
    model_path = Path("models/churn_model.pkl")
    if model_path.exists():
        print("✅ Model already exists, skipping training")
        return True
    
    print("📝 Running model training script...")
    return run_command("python scripts/train_model.py", "Training model")

def build_docker_image():
    """Build the Docker image"""
    return run_command("docker build -t churn-prediction-api .", "Building Docker image")

def start_services():
    """Start all services using Docker Compose"""
    print("🚀 Starting all services...")
    
    # Stop any existing services
    subprocess.run("docker-compose down", shell=True, capture_output=True)
    
    # Start services
    if run_command("docker-compose up -d", "Starting services"):
        print("⏳ Waiting for services to be ready...")
        time.sleep(30)
        
        # Check service status
        result = subprocess.run("docker-compose ps", shell=True, capture_output=True, text=True)
        print("📊 Service Status:")
        print(result.stdout)
        
        return True
    
    return False

def test_api():
    """Test the API"""
    print("🧪 Testing the API...")
    return run_command("python scripts/test_api.py", "Testing API functionality")

def show_access_info():
    """Show access information for all services"""
    print("\n" + "="*60)
    print("🎉 Setup Complete! Access Information:")
    print("="*60)
    print("📊 FastAPI Application: http://localhost:8000")
    print("📚 API Documentation:   http://localhost:8000/docs")
    print("🏥 Health Check:        http://localhost:8000/health")
    print("📈 Grafana Dashboard:   http://localhost:3000 (admin/admin)")
    print("📊 Prometheus Metrics:  http://localhost:9090")
    print("🔬 MLflow Tracking:     http://localhost:5000")
    print("="*60)
    print("\n💡 Next steps:")
    print("1. Train the model: python scripts/train_model.py")
    print("2. Test the API: python scripts/test_api.py")
    print("3. View metrics in Grafana dashboard")
    print("4. Check MLflow for experiment tracking")

def main():
    """Main setup function"""
    print("🚀 Churn Prediction MLOps System Setup")
    print("="*50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Train model (or provide instructions)
    if not train_model():
        print("❌ Failed to train model")
        sys.exit(1)
    
    # Build Docker image
    if not build_docker_image():
        print("❌ Failed to build Docker image")
        sys.exit(1)
    
    # Start services
    if not start_services():
        print("❌ Failed to start services")
        sys.exit(1)
    
    # Test API
    if not test_api():
        print("⚠️  API tests failed, but services are running")
    
    # Show access information
    show_access_info()

if __name__ == "__main__":
    main() 