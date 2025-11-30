#!/bin/bash

# Docker Web Server Startup Script

echo "🐳 Starting Docker Web Server..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "📦 Using Docker Compose..."
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Web server started successfully!"
        echo "🌐 Access the server at: http://localhost:8080"
        echo "💚 Health check: http://localhost:8080/health"
        echo ""
        echo "📋 Useful commands:"
        echo "   View logs: docker-compose logs -f"
        echo "   Stop server: docker-compose down"
    else
        echo "❌ Failed to start web server"
        exit 1
    fi
else
    echo "📦 Using Docker commands..."
    docker build -t my-webserver .
    docker run -d -p 8080:80 --name webserver my-webserver
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Web server started successfully!"
        echo "🌐 Access the server at: http://localhost:8080"
        echo "💚 Health check: http://localhost:8080/health"
        echo ""
        echo "📋 Useful commands:"
        echo "   View logs: docker logs webserver"
        echo "   Stop server: docker stop webserver"
    else
        echo "❌ Failed to start web server"
        exit 1
    fi
fi

