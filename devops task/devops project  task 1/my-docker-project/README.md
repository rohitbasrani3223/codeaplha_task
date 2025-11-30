# 🐳 Docker Web Server Project

## Task 4: Web Server using Docker

This project demonstrates Docker containerization basics by deploying and managing a web server inside Docker containers.

## 📋 Project Objectives

- ✅ Learn Docker containerization basics
- ✅ Deploy and manage a web server inside Docker containers
- ✅ Understand container lifecycle and commands
- ✅ Monitor container health and troubleshoot issues
- ✅ Explore container-based app deployment best practices

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system
- Docker Compose (optional, for easier management)

### Method 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Method 2: Using Docker Commands

```bash
# Build the Docker image
docker build -t my-webserver .

# Run the container
docker run -d -p 8080:80 --name webserver my-webserver

# Check if container is running
docker ps

# View container logs
docker logs webserver

# Stop the container
docker stop webserver

# Remove the container
docker rm webserver
```

## 🌐 Access the Web Server

Once the container is running, open your browser and navigate to:
- **Main Page**: http://localhost:8080
- **Health Check**: http://localhost:8080/health

## 📦 Container Lifecycle Management

### Build Commands
```bash
# Build image
docker build -t my-webserver .

# Build with no cache
docker build --no-cache -t my-webserver .
```

### Run Commands
```bash
# Run in detached mode
docker run -d -p 8080:80 --name webserver my-webserver

# Run with custom port
docker run -d -p 3000:80 --name webserver my-webserver

# Run with volume mount
docker run -d -p 8080:80 -v $(pwd)/logs:/var/log/nginx --name webserver my-webserver
```

### Container Management
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# View container logs
docker logs webserver
docker logs -f webserver  # Follow logs in real-time

# Execute command inside container
docker exec -it webserver sh

# Inspect container
docker inspect webserver

# View container stats
docker stats webserver
```

### Stop and Remove
```bash
# Stop container
docker stop webserver

# Start stopped container
docker start webserver

# Restart container
docker restart webserver

# Remove stopped container
docker rm webserver

# Force remove running container
docker rm -f webserver

# Remove image
docker rmi my-webserver
```

## 🔍 Monitoring and Health Checks

### Health Check Status
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' webserver

# View health check logs
docker inspect --format='{{json .State.Health}}' webserver | python -m json.tool
```

### Container Stats
```bash
# Real-time container statistics
docker stats webserver

# One-time stats
docker stats --no-stream webserver
```

### Logs Monitoring
```bash
# View all logs
docker logs webserver

# View last 100 lines
docker logs --tail 100 webserver

# Follow logs
docker logs -f webserver

# View logs with timestamps
docker logs -t webserver
```

## 🛠️ Troubleshooting

### Container won't start
```bash
# Check container logs
docker logs webserver

# Check if port is already in use
netstat -an | grep 8080  # Linux/Mac
netstat -an | findstr 8080  # Windows
```

### Container keeps restarting
```bash
# Check exit code
docker inspect webserver | grep -i exitcode

# View last 50 log lines
docker logs --tail 50 webserver
```

### Permission issues
```bash
# Check file permissions
ls -la html/

# Fix permissions if needed
chmod -R 755 html/
```

### Network issues
```bash
# Test connectivity from inside container
docker exec webserver wget -O- http://localhost/health

# Check network configuration
docker network inspect bridge
```

## 📁 Project Structure

```
my-docker-project/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── nginx.conf             # Nginx server configuration
├── .dockerignore          # Files to ignore in Docker build
├── README.md              # This file
├── html/
│   └── index.html         # Web page content
└── logs/                  # Nginx logs (created at runtime)
```

## 🎯 Best Practices Implemented

1. **Multi-stage builds ready**: Using lightweight Alpine Linux base image
2. **Health checks**: Built-in health monitoring
3. **Security**: Security headers in Nginx configuration
4. **Optimization**: Gzip compression enabled
5. **Logging**: Proper log management
6. **Restart policy**: Automatic restart on failure
7. **Resource limits**: Can be added via docker-compose
8. **.dockerignore**: Excludes unnecessary files from build context

## 🔧 Customization

### Change Port
Edit `docker-compose.yml`:
```yaml
ports:
  - "3000:80"  # Change 8080 to your desired port
```

### Modify HTML Content
Edit `html/index.html` and rebuild:
```bash
docker-compose up -d --build
```

### Update Nginx Configuration
Edit `nginx.conf` and rebuild the container.

## 📚 Learning Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## 📝 Notes

- The container uses Alpine Linux for a smaller image size
- Health checks run every 30 seconds
- Logs are stored in the `logs/` directory when using docker-compose
- The web server automatically restarts unless manually stopped

## ✅ Verification Checklist

- [x] Docker image builds successfully
- [x] Container runs without errors
- [x] Web server accessible on http://localhost:8080
- [x] Health check endpoint responds
- [x] Container logs are accessible
- [x] Container can be stopped and restarted
- [x] Health monitoring works correctly

## 👤 Author

DevOps Task 4 Submission

---

**Status**: ✅ Project Complete and Ready for Submission

