# Deployment Notes: Docker & Infrastructure Quick Reference

Practical, concise reference guide for Docker, MongoDB, container management, and image publishing for the **Portfolio Research** platform.

---

## 1. Docker Image Management

### Build Image
Build the application container image using the Dockerfile located in `deployment/docker/Dockerfile`:

```bash
docker build -t portfolio-research:latest -f deployment/docker/Dockerfile .
```

### Tag Image for Docker Hub
Tag the built image with your Docker Hub username and version:

```bash
docker tag portfolio-research:latest <your-dockerhub-username>/portfolio-research:v1.0.0
docker tag portfolio-research:latest <your-dockerhub-username>/portfolio-research:latest
```

---

## 2. Running Application Container

### Run Container Standalone
Run the portfolio research service mapping host port `8000` to container port `8000`:

```bash
docker run -d \
  --name portfolio-app \
  -p 8000:8000 \
  -e MONGO_URI="mongodb://mongo:27017" \
  portfolio-research:latest
```

### Stop and Remove Container
```bash
docker stop portfolio-app
docker rm portfolio-app
```

---

## 3. MongoDB Container & Volume Management

### Create Persistent Volume
Create a named volume to persist database records across container restarts:

```bash
docker volume create mongo_portfolio_data
```

### Run MongoDB Container
Start a MongoDB instance using the persistent named volume:

```bash
docker run -d \
  --name portfolio-mongo \
  -p 27017:27017 \
  -v mongo_portfolio_data:/data/db \
  mongo:7.0
```

### Connect App and Database via Docker Network
Create a shared bridge network so the application container can resolve the MongoDB service name:

```bash
# 1. Create Docker network
docker network create portfolio-net

# 2. Run MongoDB on network
docker run -d \
  --name mongo \
  --network portfolio-net \
  -v mongo_portfolio_data:/data/db \
  mongo:7.0

# 3. Run App on network
docker run -d \
  --name portfolio-app \
  --network portfolio-net \
  -p 8000:8000 \
  -e MONGO_URI="mongodb://mongo:27017" \
  portfolio-research:latest
```

---

## 4. Docker Hub Operations

### Push Image to Docker Hub
Log in to Docker Hub and push the repository image:

```bash
docker login
docker push <your-dockerhub-username>/portfolio-research:v1.0.0
docker push <your-dockerhub-username>/portfolio-research:latest
```

### Pull Image from Docker Hub
Pull the latest published image onto a target server or deployment machine:

```bash
docker pull <your-dockerhub-username>/portfolio-research:latest
```

---

## 5. Cheat Sheet Summary

| Command | Purpose |
| :--- | :--- |
| `docker build -t portfolio-research -f deployment/docker/Dockerfile .` | Build app image |
| `docker run -d -p 8000:8000 portfolio-research` | Run app container |
| `docker volume create mongo_portfolio_data` | Create DB storage volume |
| `docker run -d -v mongo_portfolio_data:/data/db mongo:7.0` | Run persistent Mongo DB |
| `docker push <user>/portfolio-research:latest` | Push to Docker Hub |
| `docker pull <user>/portfolio-research:latest` | Pull from Docker Hub |
