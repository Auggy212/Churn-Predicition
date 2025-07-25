#!/usr/bin/env python3
"""
Simple test to verify frontend-API connection
"""

import requests

def test_api_connection():
    """Test if the API is accessible"""
    print("🔍 Testing API Connection...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API is accessible")
            print(f"   Status: {data.get('status')}")
            print(f"   Model loaded: {data.get('model_loaded')}")
            print(f"   Model type: {data.get('model_type')}")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n📊 Testing Model Info...")
    
    try:
        response = requests.get("http://localhost:8000/model-info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Model info accessible")
            print(f"   Model type: {data.get('model_type')}")
            print(f"   Version: {data.get('model_version')}")
            return True
        else:
            print(f"❌ Model info returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot get model info: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Frontend-API Connection")
    print("=" * 40)
    
    api_ok = test_api_connection()
    model_ok = test_model_info()
    
    print("\n" + "=" * 40)
    print("📋 Results:")
    print(f"  API Connection: {'✅' if api_ok else '❌'}")
    print(f"  Model Info: {'✅' if model_ok else '❌'}")
    
    if api_ok and model_ok:
        print("\n🎉 API is working correctly!")
        print("\n📋 Next steps:")
        print("1. Restart your frontend (if it's running)")
        print("2. Refresh the browser page")
        print("3. Check browser console for API configuration")
        print("4. The frontend should now connect properly")
    else:
        print("\n⚠️  API connection issues detected.")
        print("Please check if the API container is running.")

if __name__ == "__main__":
    main() 