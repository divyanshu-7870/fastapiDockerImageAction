# Notes API - Backend Development (Unit 4)

A simple Notes application built with FastAPI, containerized with Docker, and automated using GitHub Actions CI/CD.

## Project Structure

```
├── .github/workflows/
│   └── fastapibuild.yml     # GitHub Actions workflow
├── src/
│   └── main.py              # FastAPI application
├── automationTesting.py     # Automated route testing
├── docker-compose.yml       # Docker compose setup
├── Dockerfile               # Docker configuration
├── requirements.txt         # Project dependencies
└── README.md
```

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python src/main.py
   ```
   The app will start on `http://127.0.0.1:8000`.

   - API docs: `http://127.0.0.1:8000/docs`
   - Health check: `http://127.0.0.1:8000/health`
   - Notes list: `http://127.0.0.1:8000/notes`

3. Run automated tests:
   ```bash
   python automationTesting.py
   ```

## Running with Docker

### Manual Build and Run:

1. Build the image:
   ```bash
   docker build -t notes-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 notes-app
   ```

### Using Docker Compose:

Start the service:
```bash
docker compose up -d
```

Stop the service:
```bash
docker compose down
```

## GitHub Actions CI/CD

The workflow in `.github/workflows/fastapibuild.yml` runs on every push to `main`:
1. Checks out the code.
2. Sets up Python and installs dependencies.
3. Runs `automationTesting.py`.
4. Logs into Docker Hub using secrets (`DOCKERUSERNAME` and `DOCKERTOKEN`).
5. Builds and pushes the Docker image to Docker Hub.
