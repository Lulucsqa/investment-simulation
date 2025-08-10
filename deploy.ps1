# Investment Simulation System PowerShell Deployment Script
# Advanced deployment with better error handling and features

param(
    [switch]$Production,
    [switch]$Monitor,
    [switch]$SkipBrowser,
    [string]$Environment = "development"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Cyan = "Cyan"

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Write-Header {
    param([string]$Message)
    Write-Host $Message -ForegroundColor $Cyan
    Write-Host ("=" * $Message.Length) -ForegroundColor $Cyan
}

# Main deployment function
function Deploy-InvestmentSystem {
    Write-Header "🚀 Investment Simulation System - PowerShell Deployment"
    
    # Check prerequisites
    Write-Status "Checking prerequisites..."
    
    # Check Docker
    try {
        $dockerVersion = docker --version
        Write-Status "✅ Docker found: $dockerVersion"
    }
    catch {
        Write-Error "Docker is not installed or not in PATH"
        Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop"
        exit 1
    }
    
    # Check Docker Compose
    try {
        $composeVersion = docker-compose --version
        Write-Status "✅ Docker Compose found: $composeVersion"
    }
    catch {
        Write-Error "Docker Compose is not installed or not in PATH"
        exit 1
    }
    
    # Check if Docker is running
    try {
        docker info | Out-Null
        Write-Status "✅ Docker daemon is running"
    }
    catch {
        Write-Error "Docker daemon is not running. Please start Docker Desktop."
        exit 1
    }
    
    # Create necessary directories
    Write-Status "Creating necessary directories..."
    @("outputs", "backend", "logs") | ForEach-Object {
        if (!(Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ -Force | Out-Null
            Write-Status "Created directory: $_"
        }
    }
    
    # Set environment variables
    $env:COMPOSE_PROJECT_NAME = "investment-simulation"
    
    # Choose compose file based on environment
    $composeFile = if ($Production) { "docker-compose.prod.yml" } else { "docker-compose.yml" }
    Write-Status "Using compose file: $composeFile"
    
    # Stop existing containers
    Write-Status "Stopping existing containers..."
    docker-compose -f $composeFile down --remove-orphans 2>$null
    
    # Build and start services
    Write-Status "Building and starting services..."
    docker-compose -f $composeFile build --no-cache
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to build containers"
        exit 1
    }
    
    docker-compose -f $composeFile up -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to start containers"
        exit 1
    }
    
    # Wait for services
    Write-Status "Waiting for services to start..."
    Start-Sleep -Seconds 15
    
    # Health checks
    Write-Status "Performing health checks..."
    
    $backendHealthy = $false
    $frontendHealthy = $false
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Status "✅ Backend API is healthy"
            $backendHealthy = $true
        }
    }
    catch {
        Write-Warning "⚠️ Backend API might not be ready yet"
    }
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost/" -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Status "✅ Frontend is healthy"
            $frontendHealthy = $true
        }
    }
    catch {
        Write-Warning "⚠️ Frontend might not be ready yet"
    }
    
    # Display results
    Write-Host ""
    Write-Header "🎉 Deployment Complete!"
    Write-Host ""
    Write-Host "📊 Investment Simulation System is running:" -ForegroundColor $Cyan
    Write-Host "   Frontend: http://localhost" -ForegroundColor White
    Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
    Write-Host "   API Documentation: http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Management Commands:" -ForegroundColor $Cyan
    Write-Host "   Status Dashboard: python status.py" -ForegroundColor White
    Write-Host "   Health Check: python health-check.py" -ForegroundColor White
    Write-Host "   View Logs: docker-compose logs -f" -ForegroundColor White
    Write-Host "   Stop System: docker-compose down" -ForegroundColor White
    Write-Host "   Restart: docker-compose restart" -ForegroundColor White
    Write-Host ""
    
    # Start monitoring if requested
    if ($Monitor) {
        Write-Status "Starting status monitor..."
        python status.py
    }
    
    # Open browser if not skipped
    if (!$SkipBrowser -and $frontendHealthy) {
        Write-Status "Opening application in browser..."
        Start-Process "http://localhost"
    }
    
    # Show container status
    Write-Host "🐳 Container Status:" -ForegroundColor $Cyan
    docker-compose -f $composeFile ps
}

# Error handling
try {
    Deploy-InvestmentSystem
}
catch {
    Write-Error "Deployment failed: $($_.Exception.Message)"
    Write-Host ""
    Write-Host "🔧 Troubleshooting:" -ForegroundColor $Yellow
    Write-Host "1. Check Docker Desktop is running"
    Write-Host "2. Ensure ports 80 and 8000 are available"
    Write-Host "3. Run: docker-compose logs -f"
    Write-Host "4. Try: docker system prune -a"
    exit 1
}