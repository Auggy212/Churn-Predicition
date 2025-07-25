#!/usr/bin/env python3
"""
Test script to verify CORS headers
"""

import requests

def test_cors_headers():
    """Test if CORS headers are present"""
    print("🔍 Testing CORS Headers...")
    
    try:
        # Test with Origin header
        headers = {
            'Origin': 'http://localhost:3000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get("http://localhost:8000/health", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Check for CORS headers
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials'
        ]
        
        print("\nCORS Headers Found:")
        for header in cors_headers:
            value = response.headers.get(header)
            if value:
                print(f"✅ {header}: {value}")
            else:
                print(f"❌ {header}: Not found")
        
        # Check if the specific origin is allowed
        allow_origin = response.headers.get('Access-Control-Allow-Origin')
        if allow_origin == 'http://localhost:3000' or allow_origin == '*':
            print("\n🎉 CORS is properly configured!")
            return True
        else:
            print(f"\n⚠️  CORS origin mismatch. Expected 'http://localhost:3000', got '{allow_origin}'")
            return False
            
    except Exception as e:
        print(f"❌ Error testing CORS: {e}")
        return False

def test_preflight_request():
    """Test OPTIONS preflight request"""
    print("\n🛫 Testing Preflight Request...")
    
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options("http://localhost:8000/health", headers=headers)
        
        print(f"Preflight Status Code: {response.status_code}")
        
        # Check preflight headers
        allow_origin = response.headers.get('Access-Control-Allow-Origin')
        allow_methods = response.headers.get('Access-Control-Allow-Methods')
        
        if allow_origin and allow_methods:
            print(f"✅ Preflight CORS headers: {allow_origin}, {allow_methods}")
            return True
        else:
            print("❌ Preflight CORS headers missing")
            return False
            
    except Exception as e:
        print(f"❌ Error testing preflight: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing CORS Configuration")
    print("=" * 40)
    
    cors_ok = test_cors_headers()
    preflight_ok = test_preflight_request()
    
    print("\n" + "=" * 40)
    print("📋 CORS Test Results:")
    print(f"  CORS Headers: {'✅' if cors_ok else '❌'}")
    print(f"  Preflight Request: {'✅' if preflight_ok else '❌'}")
    
    if cors_ok and preflight_ok:
        print("\n🎉 CORS is properly configured!")
        print("The frontend should now be able to connect to the API.")
    else:
        print("\n⚠️  CORS configuration issues detected.")
        print("The API may need to be restarted or the CORS middleware may not be loaded.")

if __name__ == "__main__":
    main() 