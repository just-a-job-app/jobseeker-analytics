# Dockerfile
FROM python:3.11

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the startup scripts executable
RUN chmod +x scripts/startup.py && chmod +x start.sh

# Expose the port (important for Uvicorn)
EXPOSE 8000

# Use the startup script as the entry point
CMD ["/app/start.sh"]