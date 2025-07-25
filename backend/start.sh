#!/bin/bash

echo "🚀 Starting application..."

# Run the startup script (sets up demo infrastructure)
python scripts/startup.py

# Start the FastAPI server
echo "🌐 Starting FastAPI server..."
exec uvicorn main:app --reload --host 0.0.0.0 --port 8000 