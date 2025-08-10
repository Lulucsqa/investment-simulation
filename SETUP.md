# Investment Simulation System - Setup Guide

This guide will help you set up the complete Investment Simulation System on your machine.

## 📋 Prerequisites Installation

### 1. Install Docker Desktop (Required)

**Windows:**
1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop
2. Run the installer and follow the setup wizard
3. Restart your computer when prompted
4. Launch Docker Desktop and wait for it to start
5. Verify installation: Open PowerShell and run `docker --version`

**Alternative for Windows (if Docker Desktop doesn't work):**
- Install Docker using WSL2: https://docs.docker.com/desktop/windows/wsl/

**Mac:**
1. Download Docker Desktop for Mac from: https://www.docker.com/products/docker-desktop
2. Drag Docker.app to Applications folder
3. Launch Docker Desktop
4. Verify installation: Open Terminal and run `docker --version`

**Linux (Ubuntu/Debian):**
```bash
# Update package index
sudo apt update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Restart to apply group changes
sudo reboot
```

### 2. Install Python (Optional - for standalone mode)

**Windows:**
1. Download Python 3.11+ from: https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Verify: Open Command Prompt and run `python --version`

**Mac:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# CentOS/RHEL
sudo yum install python311 python311-pip
```

### 3. Install Node.js (Optional - for frontend development)

**All Platforms:**
1. Download Node.js 18+ from: https://nodejs.org/
2. Run the installer
3. Verify: `node --version` and `npm --version`

## 🚀 Quick Start Options

### Option 1: Docker Deployment (Recommended)

This is the easiest way to get everything running:

**Windows:**
```cmd
# Simple start (recommended for beginners)
start.cmd

# Or with batch script
deploy.bat

# Or with PowerShell (advanced features)
.\deploy.ps1
```

**Linux/Mac:**
```bash
# Make script executable
chmod +x deploy.sh

# Deploy
./deploy.sh
```

### Option 2: Manual Installation

If you prefer to run components separately:

**Backend Setup:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the API server
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

**Frontend Setup:**
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Or build for production
npm run build
npm run preview
```

**Python Simulation (Standalone):**
```bash
# Run the original Python simulation
python main.py
```

## 🔧 Configuration

### Environment Setup

1. **Copy environment template:**
```bash
copy .env.example .env          # Windows
cp .env.example .env            # Linux/Mac
```

2. **Edit `.env` file:**
```bash
# Application Settings
ENVIRONMENT=development
DEBUG=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

### Frontend Configuration

Create `frontend/.env.local`:
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Investment Simulation System
```

## 🏥 Health Checks

After deployment, verify everything is working:

**Automated Health Check:**
```bash
python health-check.py
```

**Manual Verification:**
1. Frontend: Open http://localhost in your browser
2. Backend API: Open http://localhost:8000 in your browser
3. API Documentation: Open http://localhost:8000/docs

**Real-time Monitoring:**
```bash
python status.py
```

## 🐳 Docker Commands Reference

**Basic Operations:**
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# View running containers
docker-compose ps

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh
```

**Troubleshooting:**
```bash
# Rebuild containers
docker-compose build --no-cache

# Clean up Docker system
docker system prune -a

# Remove all containers and volumes
docker-compose down -v --remove-orphans
```

## 🔍 Troubleshooting

### Common Issues

**1. Docker not found:**
```
Error: 'docker' is not recognized as an internal or external command
```
**Solution:** Install Docker Desktop and restart your terminal/PowerShell.

**2. Port already in use:**
```
Error: Port 80 is already in use
```
**Solution:** 
- Stop other web servers (IIS, Apache, Nginx)
- Or change ports in `docker-compose.yml`:
```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Use port 8080 instead
```

**3. Docker daemon not running:**
```
Error: Cannot connect to the Docker daemon
```
**Solution:** Start Docker Desktop and wait for it to fully load.

**4. Permission denied (Linux):**
```
Error: Permission denied while trying to connect to Docker daemon
```
**Solution:**
```bash
sudo usermod -aG docker $USER
# Then logout and login again
```

**5. Build failures:**
```
Error: Failed to build containers
```
**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
```

### Performance Issues

**Slow startup:**
- Increase Docker Desktop memory allocation (Settings > Resources > Memory > 4GB+)
- Close other applications to free up resources

**Slow simulations:**
- The Python backend uses NumPy optimizations
- For large simulations, consider increasing container resources

### Network Issues

**Can't access frontend:**
1. Check if port 80 is available: `netstat -an | findstr :80`
2. Try accessing via IP: http://127.0.0.1
3. Check Windows Firewall settings

**API connection errors:**
1. Verify backend is running: `curl http://localhost:8000/`
2. Check CORS settings in `backend/api.py`
3. Verify network connectivity between containers

## 📱 Access URLs

After successful deployment:

- **Frontend Application:** http://localhost
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API OpenAPI Spec:** http://localhost:8000/openapi.json

## 🔒 Security Notes

**Development Environment:**
- CORS is configured for localhost access
- Debug mode may be enabled
- No authentication required

**Production Deployment:**
- Update CORS origins in `backend/api.py`
- Set `DEBUG=false` in environment variables
- Configure proper authentication
- Use HTTPS with SSL certificates
- Set up proper firewall rules

## 📊 System Requirements

**Minimum:**
- 4GB RAM
- 2GB free disk space
- Windows 10/11, macOS 10.15+, or Linux
- Docker Desktop 4.0+

**Recommended:**
- 8GB RAM
- 5GB free disk space
- SSD storage
- Multi-core processor

## 🆘 Getting Help

**If you encounter issues:**

1. **Check the logs:**
```bash
docker-compose logs -f
```

2. **Run health check:**
```bash
python health-check.py
```

3. **Verify Docker status:**
```bash
docker-compose ps
docker system info
```

4. **Common solutions:**
- Restart Docker Desktop
- Clear Docker cache: `docker system prune -a`
- Check port availability
- Verify firewall settings

5. **Still having issues?**
- Check the DEPLOYMENT.md file for advanced troubleshooting
- Review Docker Desktop documentation
- Ensure all prerequisites are properly installed

## 🎉 Next Steps

Once everything is running:

1. **Explore the Web Interface:** http://localhost
2. **Try the API:** http://localhost:8000/docs
3. **Run Python simulations:** `python main.py`
4. **Monitor system status:** `python status.py`
5. **Customize parameters** in the web interface or `main.py`

**Happy Investing! 📈**