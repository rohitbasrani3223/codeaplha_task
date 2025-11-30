@echo off
REM Docker Web Server Startup Script for Windows

echo 🐳 Starting Docker Web Server...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker is not running. Please start Docker first.
    exit /b 1
)

REM Check if docker-compose is available
where docker-compose >nul 2>&1
if %errorlevel% equ 0 (
    echo 📦 Using Docker Compose...
    docker-compose up -d --build
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Web server started successfully!
        echo 🌐 Access the server at: http://localhost:8080
        echo 💚 Health check: http://localhost:8080/health
        echo.
        echo 📋 Useful commands:
        echo    View logs: docker-compose logs -f
        echo    Stop server: docker-compose down
    ) else (
        echo ❌ Failed to start web server
        exit /b 1
    )
) else (
    echo 📦 Using Docker commands...
    docker build -t my-webserver .
    docker run -d -p 8080:80 --name webserver my-webserver
    
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Web server started successfully!
        echo 🌐 Access the server at: http://localhost:8080
        echo 💚 Health check: http://localhost:8080/health
        echo.
        echo 📋 Useful commands:
        echo    View logs: docker logs webserver
        echo    Stop server: docker stop webserver
    ) else (
        echo ❌ Failed to start web server
        exit /b 1
    )
)

pause

