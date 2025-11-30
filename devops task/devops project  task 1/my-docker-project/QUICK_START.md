# 🚀 Quick Start Guide

## Step 1: Install Docker Desktop

1. Download Docker Desktop for Windows: https://www.docker.com/products/docker-desktop
2. Install and restart your computer if needed
3. Start Docker Desktop application
4. Wait for Docker to start (whale icon in system tray)

## Step 2: Verify Installation

Open PowerShell or Command Prompt and run:
```bash
docker --version
docker-compose --version
```

You should see version numbers if Docker is installed correctly.

## Step 3: Run the Project

Navigate to project folder:
```bash
cd C:\Users\PC\Desktop\my-docker-project
```

Run the container:
```bash
docker-compose up -d --build
```

## Step 4: Access Web Server

Open your browser and go to:
- **Main Page**: http://localhost:8080
- **Health Check**: http://localhost:8080/health

## Step 5: Check Status

```bash
# Check if container is running
docker ps

# View logs
docker-compose logs -f

# Check health status
docker inspect --format='{{.State.Health.Status}}' my-webserver
```

## Step 6: Stop the Server

```bash
docker-compose down
```

---

## Alternative: Using Docker Commands Directly

If docker-compose doesn't work, use these commands:

```bash
# Build the image
docker build -t my-webserver .

# Run the container
docker run -d -p 8080:80 --name webserver my-webserver

# Check status
docker ps

# View logs
docker logs webserver

# Stop and remove
docker stop webserver
docker rm webserver
```

---

## Troubleshooting

### Docker not starting?
- Make sure Docker Desktop is running
- Check Windows WSL 2 is enabled (Docker Desktop will guide you)

### Port 8080 already in use?
- Change port in `docker-compose.yml`: `"3000:80"` instead of `"8080:80"`
- Or stop the service using port 8080

### Permission errors?
- Run PowerShell as Administrator
- Make sure Docker Desktop is running

---

**Need Help?** Check `README.md` for detailed documentation.

