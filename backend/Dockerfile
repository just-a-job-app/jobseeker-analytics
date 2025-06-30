# Dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port (important for Uvicorn)
EXPOSE 8000

# Use startup script to run both Uvicorn and Celery
CMD ["./start.sh"]