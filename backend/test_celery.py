#!/usr/bin/env python3
"""
Test script to verify Celery is working correctly
"""
import os
import sys

# Add backend to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from celery_app import celery_app
from tasks.email_tasks import get_processing_status

def test_celery():
    """Test basic Celery functionality"""
    print("Testing Celery connection...")
    
    # Test Redis connection
    try:
        # Send a test task
        result = get_processing_status.delay("test_user_123")
        print(f"Task sent successfully. Task ID: {result.id}")
        
        # Wait for result (with timeout)
        task_result = result.get(timeout=5)
        print(f"Task result: {task_result}")
        
        print("\n✅ Celery is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Celery test failed: {e}")
        print("\nMake sure:")
        print("1. Redis is running (docker-compose up redis)")
        print("2. Celery worker is running")

if __name__ == "__main__":
    test_celery()