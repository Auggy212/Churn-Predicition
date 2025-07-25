#!/usr/bin/env python3
"""
Test script to verify frontend-API connection
"""

import requests
import json

def test_api_endpoints():
    """Test all API endpoints that the frontend needs"""
    print("🔍 Testing API Endpoints...")
    
    endpoints = [
        ("Health Check", "http://localhost:8000/health"),
        ("Model Info", "http://localhost:8000/model-info"),
        ("Root", "http://localhost:8000/"),
    ]
    
    all_working = True
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: Working")
                if name == "Health Check":
                    data = response.json()
                    print(f"   Model loaded: {data.get('model_loaded', False)}")
                    print(f"   Status: {data.get('status', 'Unknown')}")
                elif name == "Model Info":
                    data = response.json()
                    print(f"   Model type: {data.get('model_type', 'Unknown')}")
                    print(f"   Version: {data.get('model_version', 'Unknown')}")
            else:
                print(f"❌ {name}: Failed (Status {response.status_code})")
                all_working = False
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            all_working = False
    
    return all_working

def test_prediction():
    """Test the prediction endpoint"""
    print("\n🎯 Testing Prediction Endpoint...")
    
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
            print("✅ Prediction API: Working")
            print(f"   Churn prediction: {result.get('churn_prediction', 'Unknown')}")
            print(f"   Probability: {result.get('churn_probability', 0):.2f}")
            return True
        else:
            print(f"❌ Prediction API: Failed (Status {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction API: Error - {e}")
        return False

def test_frontend_proxy():
    """Test if frontend proxy is working"""
    print("\n🌐 Testing Frontend Proxy...")
    
    try:
        # Test if frontend is accessible
        response = requests.get("http://localhost:3000", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend: Accessible")
            return True
        else:
            print(f"❌ Frontend: Not accessible (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Frontend: Error - {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Frontend-API Connection")
    print("=" * 50)
    
    # Test API endpoints
    api_ok = test_api_endpoints()
    
    # Test prediction
    prediction_ok = test_prediction()
    
    # Test frontend
    frontend_ok = test_frontend_proxy()
    
    print("\n" + "=" * 50)
    print("📋 Test Results:")
    print(f"  API Endpoints: {'✅' if api_ok else '❌'}")
    print(f"  Prediction API: {'✅' if prediction_ok else '❌'}")
    print(f"  Frontend: {'✅' if frontend_ok else '❌'}")
    
    if all([api_ok, prediction_ok, frontend_ok]):
        print("\n🎉 All tests passed! Your API is working correctly.")
        print("\n📋 Next steps:")
        print("1. Refresh your frontend browser page")
        print("2. Check the browser console for the API configuration log")
        print("3. The frontend should now connect to localhost:8000")
        print("4. No more 'ERR_NAME_NOT_RESOLVED' errors")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the API is running: docker-compose up -d")
        print("2. Check if port 8000 is accessible")
        print("3. Verify the frontend is running on port 3000")

if __name__ == "__main__":
    main() 