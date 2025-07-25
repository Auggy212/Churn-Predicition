#!/usr/bin/env python3
"""
Test script to check frontend-model connection
"""

import requests
import json
import time

def test_api_health():
    """Test if the API is healthy and model is loaded"""
    print("🔍 Testing API Health...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            print(f"   Model type: {data.get('model_type', 'Unknown')}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False

def test_prediction_api():
    """Test the prediction API endpoint"""
    print("\n🎯 Testing Prediction API...")
    
    test_data = {
        "tenure": 12,
        "monthly_charges": 50.0,
        "total_charges": 600.0,
        "contract_type": "Month-to-month",
        "payment_method": "Electronic check",
        "internet_service": "DSL",
        "customer_service_calls": 2
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction API working")
            print(f"   Churn prediction: {result.get('churn_prediction', 'Unknown')}")
            print(f"   Churn probability: {result.get('churn_probability', 0):.2f}")
            print(f"   Confidence: {result.get('confidence', 0):.2f}")
            return True
        else:
            print(f"❌ Prediction API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction API error: {e}")
        return False

def test_frontend_proxy():
    """Test if frontend proxy is working"""
    print("\n🌐 Testing Frontend Proxy...")
    
    try:
        # Test if frontend is accessible
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend proxy error: {e}")
        return False

def test_frontend_to_api_connection():
    """Test if frontend can connect to API through proxy"""
    print("\n🔗 Testing Frontend-to-API Connection...")
    
    # This simulates what the frontend would do
    test_data = {
        "tenure": 24,
        "monthly_charges": 80.0,
        "total_charges": 1920.0,
        "contract_type": "One year",
        "payment_method": "Credit card",
        "internet_service": "Fiber optic",
        "customer_service_calls": 1
    }
    
    try:
        # Test through the proxy (like frontend would)
        response = requests.post(
            "http://localhost:3000/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Frontend-to-API connection working")
            print(f"   Churn prediction: {result.get('churn_prediction', 'Unknown')}")
            print(f"   Churn probability: {result.get('churn_probability', 0):.2f}")
            return True
        else:
            print(f"❌ Frontend-to-API connection failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Frontend-to-API connection error: {e}")
        return False

def check_services_status():
    """Check if all required services are running"""
    print("🔧 Checking Services Status...")
    
    services = [
        ("API (FastAPI)", "http://localhost:8000/health"),
        ("Frontend (React)", "http://localhost:3000"),
        ("Prometheus", "http://localhost:9090"),
        ("Grafana", "http://localhost:3001"),
        ("MLflow", "http://localhost:5000")
    ]
    
    all_running = True
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 302]:  # 302 for redirects
                print(f"✅ {service_name}: Running")
            else:
                print(f"⚠️  {service_name}: Status {response.status_code}")
                all_running = False
        except Exception as e:
            print(f"❌ {service_name}: Not accessible ({e})")
            all_running = False
    
    return all_running

def main():
    """Main test function"""
    print("🚀 Testing Frontend-Model Connection")
    print("=" * 50)
    
    # Check services status
    services_ok = check_services_status()
    
    if not services_ok:
        print("\n⚠️  Some services are not running. Please start them first:")
        print("   docker-compose up -d")
        return
    
    # Test API health
    api_health_ok = test_api_health()
    
    # Test prediction API
    prediction_ok = test_prediction_api()
    
    # Test frontend proxy
    frontend_ok = test_frontend_proxy()
    
    # Test frontend-to-api connection
    connection_ok = test_frontend_to_api_connection()
    
    print("\n" + "=" * 50)
    print("📋 Connection Test Results:")
    print(f"  Services Running: {'✅' if services_ok else '❌'}")
    print(f"  API Health: {'✅' if api_health_ok else '❌'}")
    print(f"  Prediction API: {'✅' if prediction_ok else '❌'}")
    print(f"  Frontend Proxy: {'✅' if frontend_ok else '❌'}")
    print(f"  Frontend-to-API: {'✅' if connection_ok else '❌'}")
    
    if all([services_ok, api_health_ok, prediction_ok, frontend_ok, connection_ok]):
        print("\n🎉 All tests passed! Your frontend is properly connected to your model.")
        print("\n📋 Access Points:")
        print("  Frontend: http://localhost:3000")
        print("  API: http://localhost:8000")
        print("  API Docs: http://localhost:8000/docs")
        print("  Prometheus: http://localhost:9090")
        print("  Grafana: http://localhost:3001")
        print("  MLflow: http://localhost:5000")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all services are running: docker-compose up -d")
        print("2. Check if the model file exists: models/churn_model.pkl")
        print("3. Verify the API is responding: curl http://localhost:8000/health")
        print("4. Check frontend proxy configuration in package.json")

if __name__ == "__main__":
    main() 