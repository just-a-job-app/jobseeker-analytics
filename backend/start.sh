#!/bin/bash

echo "🚀 Starting application..."

# Run the startup script (sets up demo infrastructure)
python scripts/startup.py

# Start the FastAPI server
echo "🌐 Starting FastAPI server..."

# Check if we're in development mode
if [ "$ENV" = "dev" ] || [ "$ENV" = "" ]; then
    echo "🔧 Development mode detected - disabling access logs for privacy"
    exec uvicorn main:app --reload --host 0.0.0.0 --port 8000 --no-access-log --log-level info
else
    echo "🚀 Production mode detected - keeping access logs"
    exec uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info
fi 