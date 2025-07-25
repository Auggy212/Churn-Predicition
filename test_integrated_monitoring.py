#!/usr/bin/env python3
"""
Test script for integrated Prometheus monitoring in FastAPI
"""

import requests
import time
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("Testing API endpoints...")
    
    # Test root endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✓ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Message: {data.get('message')}")
            print(f"  Monitoring: {data.get('monitoring', {}).get('prometheus_integrated')}")
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"✓ Health endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: {data.get('status')}")
            print(f"  Model loaded: {data.get('model_loaded')}")
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
    
    # Test model info endpoint
    try:
        response = requests.get(f"{API_BASE_URL}/model-info")
        print(f"✓ Model info endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Model type: {data.get('model_type')}")
            print(f"  Model version: {data.get('model_version')}")
    except Exception as e:
        print(f"✗ Model info endpoint error: {e}")

def test_metrics_endpoints():
    """Test metrics endpoints"""
    print("\nTesting metrics endpoints...")
    
    # Test /metrics endpoint (from prometheus-fastapi-instrumentator)
    try:
        response = requests.get(f"{API_BASE_URL}/metrics")
        print(f"✓ /metrics endpoint: {response.status_code}")
        if response.status_code == 200:
            metrics_content = response.text
            print(f"  Content length: {len(metrics_content)} characters")
            print(f"  Contains 'http_requests_total': {'http_requests_total' in metrics_content}")
    except Exception as e:
        print(f"✗ /metrics endpoint error: {e}")
    
    # Test /prometheus endpoint (custom)
    try:
        response = requests.get(f"{API_BASE_URL}/prometheus")
        print(f"✓ /prometheus endpoint: {response.status_code}")
        if response.status_code == 200:
            metrics_content = response.text
            print(f"  Content length: {len(metrics_content)} characters")
            print(f"  Contains custom metrics: {'prediction_requests_total' in metrics_content}")
    except Exception as e:
        print(f"✗ /prometheus endpoint error: {e}")

def test_prediction_and_metrics():
    """Test prediction and verify metrics are updated"""
    print("\nTesting prediction and metrics...")
    
    # Sample customer data
    customer_data = {
        "tenure": 12,
        "monthly_charges": 65.0,
        "total_charges": 780.0,
        "contract_type": "Month-to-month",
        "payment_method": "Electronic check",
        "internet_service": "DSL",
        "online_security": "No",
        "tech_support": "No",
        "streaming_tv": "No",
        "customer_service_calls": 2
    }
    
    # Make prediction
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=customer_data)
        print(f"✓ Prediction request: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  Churn prediction: {result.get('churn_prediction')}")
            print(f"  Churn probability: {result.get('churn_probability'):.3f}")
            print(f"  Confidence: {result.get('confidence'):.3f}")
    except Exception as e:
        print(f"✗ Prediction error: {e}")
    
    # Wait a moment for metrics to update
    time.sleep(1)
    
    # Check if metrics were updated
    try:
        response = requests.get(f"{API_BASE_URL}/prometheus")
        if response.status_code == 200:
            metrics_content = response.text
            print(f"  Metrics after prediction:")
            print(f"    Contains prediction_requests_total: {'prediction_requests_total' in metrics_content}")
            print(f"    Contains prediction_duration_seconds: {'prediction_duration_seconds' in metrics_content}")
            print(f"    Contains churn_predictions_total: {'churn_predictions_total' in metrics_content}")
    except Exception as e:
        print(f"✗ Metrics check error: {e}")

def main():
    """Main test function"""
    print("=" * 60)
    print("Testing Integrated Prometheus Monitoring in FastAPI")
    print("=" * 60)
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test metrics endpoints
    test_metrics_endpoints()
    
    # Test prediction and metrics
    test_prediction_and_metrics()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    print("\nTo view metrics in Grafana:")
    print("1. Open http://localhost:3001 (Grafana)")
    print("2. Login with admin/admin")
    print("3. The Prometheus datasource should be configured automatically")
    print("4. Create dashboards using the custom metrics:")
    print("   - prediction_requests_total")
    print("   - prediction_duration_seconds")
    print("   - churn_predictions_total")
    print("   - model_load_status")

if __name__ == "__main__":
    main() 