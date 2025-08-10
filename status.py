#!/usr/bin/env python3
"""
Status dashboard for Investment Simulation System
Shows real-time status of all components
"""

import requests
import time
import os
import subprocess
from datetime import datetime
from typing import Dict, Any

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_docker_status() -> Dict[str, Any]:
    """Get Docker container status"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return {"status": "running", "containers": result.stdout}
        else:
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_service_status(url: str, name: str) -> Dict[str, Any]:
    """Get status of a service"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = time.time() - start_time
        
        return {
            "status": "healthy" if response.status_code == 200 else "unhealthy",
            "status_code": response.status_code,
            "response_time": response_time,
            "url": url
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "url": url
        }

def format_status_indicator(status: str) -> str:
    """Format status with colored indicators"""
    indicators = {
        "healthy": "🟢",
        "unhealthy": "🔴",
        "running": "🟢",
        "error": "🔴",
        "unknown": "🟡"
    }
    return indicators.get(status, "🟡")

def display_dashboard():
    """Display the status dashboard"""
    clear_screen()
    
    print("📊 Investment Simulation System - Status Dashboard")
    print("=" * 60)
    print(f"🕐 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Docker Status
    print("🐳 Docker Containers:")
    docker_status = get_docker_status()
    print(f"   {format_status_indicator(docker_status['status'])} Docker Compose: {docker_status['status']}")
    
    # Service Status
    services = [
        ("Backend API", "http://localhost:8000/"),
        ("Frontend", "http://localhost/"),
        ("API Docs", "http://localhost:8000/docs"),
    ]
    
    print("\n🌐 Services:")
    for name, url in services:
        status = get_service_status(url, name)
        indicator = format_status_indicator(status["status"])
        
        if status["status"] == "healthy":
            response_time = status.get("response_time", 0)
            print(f"   {indicator} {name}: {status['status']} ({response_time:.3f}s)")
        else:
            error = status.get("error", f"HTTP {status.get('status_code', 'Unknown')}")
            print(f"   {indicator} {name}: {status['status']} - {error}")
    
    # System Resources (if available)
    try:
        import psutil
        print(f"\n💻 System Resources:")
        print(f"   🖥️  CPU Usage: {psutil.cpu_percent()}%")
        print(f"   🧠 Memory Usage: {psutil.virtual_memory().percent}%")
        print(f"   💾 Disk Usage: {psutil.disk_usage('/').percent}%")
    except ImportError:
        pass
    
    # Quick Commands
    print(f"\n🔧 Quick Commands:")
    print(f"   View Logs: docker-compose logs -f")
    print(f"   Restart: docker-compose restart")
    print(f"   Stop: docker-compose down")
    print(f"   Health Check: python health-check.py")
    
    print(f"\n📱 Access URLs:")
    print(f"   Frontend: http://localhost")
    print(f"   Backend API: http://localhost:8000")
    print(f"   API Documentation: http://localhost:8000/docs")
    
    print(f"\nPress Ctrl+C to exit...")

def main():
    """Main function for continuous status monitoring"""
    try:
        while True:
            display_dashboard()
            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print(f"\n\n👋 Status monitoring stopped.")
        print(f"Thank you for using Investment Simulation System!")

if __name__ == "__main__":
    main()