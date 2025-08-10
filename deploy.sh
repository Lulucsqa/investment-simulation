#!/bin/bash

# Investment Simulation System Deployment Script
# This script handles the complete deployment of both backend and frontend

set -e

echo "🚀 Starting Investment Simulation System Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p outputs
mkdir -p backend

# Set environment variables
export COMPOSE_PROJECT_NAME=investment-simulation

# Build and start services
print_status "Building and starting services..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check if backend is running
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    print_status "✅ Backend API is running at http://localhost:8000"
else
    print_warning "⚠️  Backend API might not be ready yet. Check logs with: docker-compose logs backend"
fi

# Check if frontend is running
if curl -f http://localhost/ > /dev/null 2>&1; then
    print_status "✅ Frontend is running at http://localhost"
else
    print_warning "⚠️  Frontend might not be ready yet. Check logs with: docker-compose logs frontend"
fi

print_status "🎉 Deployment completed!"
print_status ""
print_status "📊 Investment Simulation System is now running:"
print_status "   Frontend: http://localhost"
print_status "   Backend API: http://localhost:8000"
print_status "   API Documentation: http://localhost:8000/docs"
print_status ""
print_status "📝 Useful commands:"
print_status "   View logs: docker-compose logs -f"
print_status "   Stop services: docker-compose down"
print_status "   Restart services: docker-compose restart"
print_status "   View running containers: docker-compose ps"