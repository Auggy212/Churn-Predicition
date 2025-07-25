#!/usr/bin/env python3
"""
Script to run the integrated FastAPI + Prometheus setup
"""

import subprocess
import sys
import time
import requests
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    try:
        import fastapi
        import prometheus_client
        import prometheus_fastapi_instrumentator
        print("✓ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_model():
    """Check if the model file exists"""
    print("Checking model file...")
    
    model_paths = [
        "models/churn_model.pkl",
        "apps/churn_model.pkl"
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            print(f"✓ Model found at: {path}")
            return True
    
    print("✗ Model file not found")
    print("Please train the model first with: python scripts/train_model.py")
    return False

def start_fastapi():
    """Start the FastAPI application"""
    print("Starting FastAPI application with integrated Prometheus monitoring...")
    
    try:
        # Start the FastAPI app
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "apps.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
        
        print("✓ FastAPI application started")
        print("  - API: http://localhost:8000")
        print("  - Docs: http://localhost:8000/docs")
        print("  - Metrics: http://localhost:8000/metrics")
        print("  - Prometheus: http://localhost:8000/prometheus")
        print("  - Health: http://localhost:8000/health")
        
        return process
    except Exception as e:
        print(f"✗ Failed to start FastAPI: {e}")
        return None

def test_endpoints():
    """Test the API endpoints"""
    print("\nTesting API endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/model-info", "Model info"),
        ("/metrics", "Metrics"),
        ("/prometheus", "Prometheus metrics")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {description}: {response.status_code}")
            else:
                print(f"✗ {description}: {response.status_code}")
        except Exception as e:
            print(f"✗ {description}: Error - {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("FastAPI + Prometheus Integrated Setup")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model
    if not check_model():
        sys.exit(1)
    
    # Start FastAPI
    process = start_fastapi()
    if not process:
        sys.exit(1)
    
    try:
        # Wait for the app to start
        print("\nWaiting for application to start...")
        time.sleep(3)
        
        # Test endpoints
        test_endpoints()
        
        print("\n" + "=" * 60)
        print("Setup complete! The application is running.")
        print("=" * 60)
        print("\nPress Ctrl+C to stop the application")
        
        # Keep the process running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\nStopping application...")
        process.terminate()
        process.wait()
        print("✓ Application stopped")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        process.terminate()
        process.wait()
        sys.exit(1)

if __name__ == "__main__":
    main() 