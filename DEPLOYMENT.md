# Investment Simulation System - Deployment Guide

This guide covers deploying the Investment Simulation System with both Python backend and React frontend.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │  Python Engine  │
│   (Port 80)     │◄──►│   (Port 8000)   │◄──►│   (core.py)     │
│   Nginx + SPA   │    │   REST API      │    │   Simulations   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git
- 4GB+ RAM
- 2GB+ disk space

### 1. Clone and Deploy

```bash
# Clone the repository
git clone <your-repo-url>
cd investment-simulation-system

# Deploy with one command
./deploy.sh    # Linux/Mac
# or
deploy.bat     # Windows
```

### 2. Access the Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Deployment Options

### Option 1: Docker Compose (Recommended)

**Development:**
```bash
docker-compose up -d
```

**Production:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Manual Deployment

**Backend:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API server
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Serve with nginx or any static server
npx serve -s dist -l 80
```

### Option 3: Cloud Deployment

#### AWS Deployment

1. **Backend (AWS Lambda + API Gateway)**
```bash
# Install serverless framework
npm install -g serverless

# Deploy backend
serverless deploy
```

2. **Frontend (AWS S3 + CloudFront)**
```bash
# Build frontend
cd frontend && npm run build

# Deploy to S3
aws s3 sync dist/ s3://your-bucket-name --delete
```

#### Heroku Deployment

**Backend:**
```bash
# Create Heroku app
heroku create investment-sim-api

# Deploy
git subtree push --prefix=backend heroku main
```

**Frontend:**
```bash
# Create Heroku app for frontend
heroku create investment-sim-frontend

# Add buildpack
heroku buildpacks:set heroku/nodejs

# Deploy
git subtree push --prefix=frontend heroku main
```

#### Vercel Deployment (Frontend)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel --prod
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application Settings
ENVIRONMENT=production
DEBUG=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Investment Simulation System

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost,https://yourdomain.com
```

### Frontend Environment

Create `frontend/.env.production`:

```bash
VITE_API_URL=https://your-api-domain.com
VITE_APP_TITLE=Investment Simulation System
VITE_APP_VERSION=1.0.0
```

## 🔧 Production Optimizations

### Backend Optimizations

1. **Use Gunicorn with multiple workers:**
```bash
gunicorn backend.api:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Add Redis for caching:**
```python
# In backend/api.py
import redis
redis_client = redis.Redis(host='redis', port=6379, db=0)
```

3. **Enable compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Frontend Optimizations

1. **Enable gzip in nginx:**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

2. **Add caching headers:**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Bundle optimization:**
```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          charts: ['recharts']
        }
      }
    }
  }
})
```

## 🔒 Security Considerations

### Backend Security

1. **CORS Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

2. **Rate Limiting:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/simulate/cdi")
@limiter.limit("10/minute")
async def simulate_cdi(request: Request, params: CDIParams):
    # ... implementation
```

3. **Input Validation:**
```python
class SimulationParams(BaseModel):
    aporte_inicial: float = Field(..., gt=0, le=10_000_000)
    anos: int = Field(..., gt=0, le=100)
```

### Frontend Security

1. **Content Security Policy:**
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self' 'unsafe-inline';">
```

2. **Environment Variable Validation:**
```typescript
const API_URL = import.meta.env.VITE_API_URL;
if (!API_URL) {
  throw new Error('VITE_API_URL environment variable is required');
}
```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Health Checks:**
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

2. **Metrics Collection:**
```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
```

3. **Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        "request_completed",
        method=request.method,
        url=str(request.url),
        status_code=response.status_code,
        duration=duration
    )
    return response
```

### Infrastructure Monitoring

Use the included monitoring stack:

```bash
# Start with monitoring
docker-compose -f docker-compose.prod.yml up -d

# Access monitoring dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts:**
```bash
# Check what's using port 80/8000
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# Use different ports
docker-compose up -d --scale frontend=0
docker run -p 8080:80 investment-simulation_frontend
```

2. **Memory issues:**
```bash
# Increase Docker memory limit
# Docker Desktop > Settings > Resources > Memory > 4GB+

# Monitor container memory usage
docker stats
```

3. **Build failures:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

4. **API connection issues:**
```bash
# Check backend logs
docker-compose logs backend

# Test API directly
curl http://localhost:8000/

# Check network connectivity
docker-compose exec frontend ping backend
```

### Performance Issues

1. **Slow simulations:**
```python
# Enable NumPy optimizations
import os
os.environ['OPENBLAS_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'
```

2. **Frontend loading slowly:**
```bash
# Enable production build
npm run build
npm run preview

# Check bundle size
npm run build -- --analyze
```

### Debugging

1. **Enable debug mode:**
```bash
# Backend debug
export DEBUG=true
uvicorn backend.api:app --reload --log-level debug

# Frontend debug
npm run dev
```

2. **Container debugging:**
```bash
# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# View container logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📈 Scaling

### Horizontal Scaling

1. **Multiple backend instances:**
```yaml
# docker-compose.yml
services:
  backend:
    # ... configuration
    deploy:
      replicas: 3
  
  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
```

2. **Load balancer configuration:**
```nginx
# nginx-lb.conf
upstream backend {
    server backend_1:8000;
    server backend_2:8000;
    server backend_3:8000;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### Vertical Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Investment Simulation System

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and Deploy
        run: |
          docker-compose build
          docker-compose up -d
          
      - name: Run Tests
        run: |
          docker-compose exec -T backend python -m pytest
          docker-compose exec -T frontend npm test
```

### Automated Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec -T backend python -c "
import shutil
shutil.make_archive('backup_$DATE', 'zip', 'outputs')
"
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)

## 🆘 Support

For deployment issues:

1. Check the logs: `docker-compose logs -f`
2. Verify configuration: `docker-compose config`
3. Test connectivity: `curl http://localhost:8000/health`
4. Review this guide's troubleshooting section
5. Open an issue in the repository

---

**Happy Deploying! 🚀**