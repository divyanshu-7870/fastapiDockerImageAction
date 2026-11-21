# FastAPI Notes App - Docker & GitHub Actions (Unit 4 PBL)

This project follows the video tutorial: [https://youtu.be/vCpj3W-yHes](https://youtu.be/vCpj3W-yHes) and the [upessocs/fastapiDockerImageAction](https://github.com/upessocs/fastapiDockerImageAction) demonstration repository.

---

## 📁 Project Structure

```bash
.
├── .github/
│   └── workflows/
│       └── fastapibuild.yml     # GitHub Actions workflow from video
├── src/
│   └── main.py                  # FastAPI app with Notes routes, health check & logging
├── automationTesting.py         # Route automated tests required for PBL
├── docker-compose.yml           # Run service with Docker Compose
├── Dockerfile                   # Docker configuration from video tutorial
├── requirements.txt             # Dependencies
└── README.md
```

---

## 1. Run Locally

Install requirements:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python src/main.py
```
App runs on `http://127.0.0.1:8000`.

- Health check: `http://127.0.0.1:8000/health`
- Notes: `http://127.0.0.1:8000/notes`
- Swagger Docs: `http://127.0.0.1:8000/docs`

---

## 2. Run Automated Tests (PBL Requirement)

```bash
python automationTesting.py
```

---

## 3. Manual Docker Build & Push (Following Tutorial Video)

### Step 1: Build Local Image
```bash
docker build -t localfastapiapp .
```

### Step 2: Tag Image for Docker Hub
Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username:
```bash
docker tag localfastapiapp YOUR_DOCKERHUB_USERNAME/notes-app:v0.1
```

### Step 3: Login to Docker Hub
1. Generate an Access Token from Docker Hub (**Account Settings → Security → Personal Access Tokens**).
2. Login securely via CLI:
```bash
echo "<YOUR_DOCKER_TOKEN>" | docker login -u "YOUR_DOCKERHUB_USERNAME" --password-stdin
```

### Step 4: Push to Docker Hub
```bash
docker push YOUR_DOCKERHUB_USERNAME/notes-app:v0.1
```

### Step 5: Run the Docker Image
```bash
docker run -p 8001:8000 YOUR_DOCKERHUB_USERNAME/notes-app:v0.1
```
Now verify `http://127.0.0.1:8001/` and `http://127.0.0.1:8001/health` in your browser.

---

## 4. Run with Docker Compose

```bash
docker compose up -d
```
Access at `http://localhost:8000/health`. To stop:
```bash
docker compose down
```

---

## 5. Automated CI/CD with GitHub Actions

The workflow file `.github/workflows/fastapibuild.yml` automates:
1. Running `automationTesting.py`.
2. Logging into Docker Hub.
3. Building the Docker image.
4. Pushing the image to Docker Hub on every push to `main`.

### Setup GitHub Secrets:
1. In your GitHub repository, go to **Settings → Secrets and variables → Actions → New repository secret**.
2. Add:
   - `DOCKERUSERNAME`: Your Docker Hub username.
   - `DOCKERTOKEN`: Your Docker Hub access token.
3. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "feat: Notes app with docker build action"
   git push -u origin main
   ```
