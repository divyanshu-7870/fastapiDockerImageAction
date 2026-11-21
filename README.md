# FastAPI Notes Application — PBL Assignment (Unit 4)

A production-grade, containerized **Notes Management REST API** built with **FastAPI**, featuring structured request logging, liveness monitoring, automated route testing with `automationTesting.py`, Docker containerization, Docker Compose orchestration, and an automated **GitHub Actions CI/CD pipeline** pushing images to **Docker Hub**.

---

## 📋 Features

- **Full CRUD Notes Management**: Create, Read, Update, Delete, and Tag-filter notes.
- **Structured Request Logging**: HTTP middleware capturing method, path, HTTP status, and duration in ms (`duration_ms=...`).
- **Health Checks & Observability**: `/health` endpoint for orchestrator and load balancer probes.
- **Automated Route Testing (`automationTesting.py`)**: Tests 100% of routes, status codes, input validations, and error conditions.
- **Docker Containerization**: Lightweight `python:3.12-slim` image.
- **Docker Compose Orchestration**: Single-command container deployment with automated health checks.
- **CI/CD with GitHub Actions**: Automatically runs tests on push; on success, builds and pushes multi-tagged images (`v0.1`, `latest`) to Docker Hub.

---

## 🗂 Project Structure

```bash
.
├── .github/
│   └── workflows/
│       └── ActionsYaml.yaml   # GitHub Actions CI/CD workflow
├── .env.example               # Template for Docker Hub credentials
├── .gitignore                 # Prevents secrets and cache from being committed
├── automationTesting.py       # Automated testing suite for all API routes
├── docker-compose.yml         # Compose configuration for the service
├── Dockerfile                 # Multi-layer Docker build definition
├── main.py                    # FastAPI application with CRUD & logging middleware
├── README.md                  # Documentation and submission guide
└── requirements.txt           # Python application & test dependencies
```

---

## 🚀 Quick Start (Local Setup)

### 1. Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API Docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 Running Automated Tests

Run the dedicated test suite:

```bash
python automationTesting.py
```

Or via `pytest`:

```bash
pytest automationTesting.py -v
```

All tests must pass (exit code `0`) before the GitHub Actions CI/CD workflow will proceed to build and push the Docker image.

---

## 🐳 Docker Deployment

### Build the Image
```bash
docker build -t notes-fastapi-app:v0.1 .
```

### Run the Container
```bash
docker run --rm -d -p 8000:8000 --name notes-container notes-fastapi-app:v0.1
```

### Verify Endpoints
```bash
curl http://localhost:8000/health
curl http://localhost:8000/notes
```

### Check Structured Logs
```bash
docker logs -f notes-container
```

---

## 🐙 Docker Compose

Run the entire application service using Docker Compose:

```bash
docker compose up -d --build
```

To view running containers and health status:
```bash
docker compose ps
```

To stop:
```bash
docker compose down
```

---

## ⚙️ GitHub Actions CI/CD Setup

To enable automated testing, building, and pushing to Docker Hub:

1. Create a new GitHub repository and push this codebase:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Notes FastAPI App"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

2. Go to **Docker Hub** (`https://hub.docker.com/`):
   - **Account Settings → Security → Personal Access Tokens → New Access Token**
   - Copy the generated token.

3. In your **GitHub Repository**:
   - Go to **Settings → Secrets and variables → Actions → New repository secret**
   - Add:
     - `DOCKERUSERNAME`: Your Docker Hub username.
     - `DOCKERTOKEN`: Your Docker Hub personal access token.

4. Push any change to `main` branch:
   - The workflow `.github/workflows/ActionsYaml.yaml` will run automatically.
   - It will run `automationTesting.py`.
   - Upon successful test completion, it logs into Docker Hub, builds the image, and pushes it to your Docker Hub repository.

---

## 📝 PBL Submission Note

As specified in the Unit 4 instructions:
> In your main Backend Development repository, add the link to this repository as `PBL Assignment`.
