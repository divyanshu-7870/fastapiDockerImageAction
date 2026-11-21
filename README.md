# Notes App - Backend Development (Unit 4 PBL)

A simple FastAPI Notes Application for the Unit 4 PBL Assignment with Docker containerization, Docker Compose, automated route testing, and GitHub Actions CI/CD.

## Files
- `main.py`: FastAPI app with Notes endpoints and request logging middleware.
- `automationTesting.py`: Automated tests for all routes.
- `Dockerfile`: Container configuration.
- `docker-compose.yml`: Run the application using Docker Compose.
- `.github/workflows/ActionsYaml.yaml`: GitHub Actions pipeline to test and push Docker image.

## How to Run Locally

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   uvicorn main:app --reload
   ```
   Open http://localhost:8000/docs for the Swagger UI.

3. Run automated tests:
   ```bash
   python automationTesting.py
   ```

## Run with Docker

Build and run with Docker:
```bash
docker build -t notes-app:v0.1 .
docker run -p 8000:8000 notes-app:v0.1
```

Or run with Docker Compose:
```bash
docker compose up
```

## GitHub Actions CI/CD Setup

1. Push this project to a new GitHub repository.
2. In GitHub repository **Settings -> Secrets and variables -> Actions**, add:
   - `DOCKERUSERNAME`: Your Docker Hub username.
   - `DOCKERTOKEN`: Your Docker Hub Access Token.
3. Every push to `main` will automatically test the code and push the image to Docker Hub.
