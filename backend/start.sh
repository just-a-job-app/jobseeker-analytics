#!/bin/bash
# Startup script for backend services

echo "Starting backend services..."

# Skip migrations for now - database is already set up
echo "Skipping database migrations (database already configured)..."
# alembic upgrade head

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A celery_app worker --loglevel=info --queues=email_processing,default &
CELERY_PID=$!

# Give Celery a moment to start
sleep 2

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# If FastAPI exits, kill Celery worker
kill $CELERY_PID