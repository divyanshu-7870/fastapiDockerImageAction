FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container (from video tutorial)
COPY ./src /app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application (from video tutorial)
CMD ["python", "main.py"]
