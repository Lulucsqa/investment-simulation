#!/usr/bin/env python3
"""
Health check script for Investment Simulation System
Verifies that both backend and frontend are running correctly
"""

import requests
import sys
import time
from typing import Dict, Any

def check_backend() -> Dict[str, Any]:
    """Check if backend API is responding"""
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            return {"status": "healthy", "response_time": response.elapsed.total_seconds()}
        else:
            return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "unhealthy", "error": str(e)}

def check_frontend() -> Dict[str, Any]:
    """Check if frontend is responding"""
    try:
        response = requests.get("http://localhost/", timeout=10)
        if response.status_code == 200:
            return {"status": "healthy", "response_time": response.elapsed.total_seconds()}
        else:
            return {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "unhealthy", "error": str(e)}

def check_api_endpoints() -> Dict[str, Any]:
    """Check specific API endpoints"""
    endpoints = [
        "/docs",
        "/openapi.json"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            results[endpoint] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code
            }
        except requests.exceptions.RequestException as e:
            results[endpoint] = {"status": "unhealthy", "error": str(e)}
    
    return results

def main():
    """Main health check function"""
    print("🏥 Investment Simulation System Health Check")
    print("=" * 50)
    
    # Check backend
    print("🔧 Checking Backend API...")
    backend_status = check_backend()
    if backend_status["status"] == "healthy":
        print(f"✅ Backend is healthy (response time: {backend_status['response_time']:.3f}s)")
    else:
        print(f"❌ Backend is unhealthy: {backend_status['error']}")
    
    # Check frontend
    print("\n🎨 Checking Frontend...")
    frontend_status = check_frontend()
    if frontend_status["status"] == "healthy":
        print(f"✅ Frontend is healthy (response time: {frontend_status['response_time']:.3f}s)")
    else:
        print(f"❌ Frontend is unhealthy: {frontend_status['error']}")
    
    # Check API endpoints
    print("\n🔍 Checking API Endpoints...")
    api_endpoints = check_api_endpoints()
    for endpoint, status in api_endpoints.items():
        if status["status"] == "healthy":
            print(f"✅ {endpoint} is healthy")
        else:
            print(f"❌ {endpoint} is unhealthy: {status.get('error', f'HTTP {status.get('status_code')}')}")
    
    # Overall status
    print("\n📊 Overall Status:")
    all_healthy = (
        backend_status["status"] == "healthy" and 
        frontend_status["status"] == "healthy" and
        all(status["status"] == "healthy" for status in api_endpoints.values())
    )
    
    if all_healthy:
        print("🎉 All systems are healthy!")
        print("\n🌐 Access URLs:")
        print("   Frontend: http://localhost")
        print("   Backend API: http://localhost:8000")
        print("   API Documentation: http://localhost:8000/docs")
        sys.exit(0)
    else:
        print("⚠️  Some systems are unhealthy. Check the logs above.")
        print("\n🔧 Troubleshooting commands:")
        print("   docker-compose logs -f")
        print("   docker-compose ps")
        print("   docker-compose restart")
        sys.exit(1)

if __name__ == "__main__":
    main()