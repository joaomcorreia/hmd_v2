#!/usr/bin/env python3
"""
Test script to verify AI assistant login instructions
"""
import requests
import json

# Test the login question flow
def test_login_questions():
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing AI Assistant Login Instructions")
    print("=" * 50)
    
    # Test 1: Admin context login question
    print("\n📋 Test 1: Admin Context - Login Help")
    admin_data = {
        'question': 'How do I log into the admin panel? I forgot my password.',
        'current_page': 'admin',
        'page_context': {}
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/contextual/", 
            json=admin_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Response: {data.get('response')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Test 2: Frontend context login question (Dutch)
    print("\n📋 Test 2: Frontend Context - Login Help (Dutch)")
    frontend_data = {
        'question': 'Hoe kan ik inloggen op de website admin? Ik ben de eigenaar.',
        'current_page': 'frontend',
        'page_context': 'customer'
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/contextual/", 
            json=frontend_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Response: {data.get('response')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Test 3: Follow-up question about credentials
    print("\n📋 Test 3: Follow-up - No Credentials")
    followup_data = {
        'question': 'No, I do not have my login credentials.',
        'current_page': 'admin',
        'page_context': {}
    }
    
    try:
        response = requests.post(
            f"{base_url}/ai/contextual/", 
            json=followup_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Response: {data.get('response')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_login_questions()
    print("\n✅ Login instruction tests completed!")