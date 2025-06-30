#!/usr/bin/env python3
"""
Monitor Gemini API usage and provide recommendations
"""
import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict
from sqlmodel import Session, select, func
from database import engine
from db import processing_tasks as task_models
from db.user_emails import UserEmails
from utils.config_utils import get_settings

settings = get_settings()


def analyze_rate_limit_logs():
    """Analyze rate limit logs if available"""
    log_file = "gemini_rate_limits.log"
    if not os.path.exists(log_file):
        return None
    
    rate_limits = []
    try:
        with open(log_file, "r") as f:
            for line in f:
                try:
                    rate_limits.append(json.loads(line.strip()))
                except:
                    pass
    except:
        return None
    
    if not rate_limits:
        return None
    
    # Analyze the logs
    limit_types = defaultdict(int)
    last_24h = datetime.now() - timedelta(hours=24)
    recent_limits = []
    
    for limit in rate_limits:
        try:
            timestamp = datetime.fromisoformat(limit["timestamp"])
            if timestamp > last_24h:
                recent_limits.append(limit)
                limit_types[limit["limit_type"]] += 1
        except:
            pass
    
    return {
        "total_limits_24h": len(recent_limits),
        "limit_types": dict(limit_types),
        "most_recent": recent_limits[-1] if recent_limits else None
    }


def get_usage_stats():
    """Get usage statistics from the database"""
    with Session(engine) as db_session:
        # Get total emails processed in last hour
        one_hour_ago = datetime.now() - timedelta(hours=1)
        emails_last_hour = db_session.exec(
            select(func.count(UserEmails.id))
            .where(UserEmails.created_at >= one_hour_ago)
        ).first()
        
        # Get active tasks
        active_tasks = db_session.exec(
            select(task_models.TaskRuns)
            .where(task_models.TaskRuns.status == task_models.STARTED)
        ).all()
        
        # Get recent errors
        recent_errors = db_session.exec(
            select(task_models.TaskRuns)
            .where(task_models.TaskRuns.error_message.is_not(None))
            .where(task_models.TaskRuns.updated >= one_hour_ago)
        ).all()
        
        return {
            "emails_last_hour": emails_last_hour or 0,
            "active_tasks": len(active_tasks),
            "recent_errors": len(recent_errors),
            "error_details": [{"user_id": t.user_id, "error": t.error_message} for t in recent_errors]
        }


def calculate_optimal_settings(stats):
    """Calculate optimal settings based on usage"""
    recommendations = []
    
    # Current settings
    current_rpm = settings.GEMINI_REQUESTS_PER_MINUTE
    current_batch = settings.GEMINI_BATCH_SIZE
    
    # If hitting rate limits frequently
    if stats["recent_errors"] > 0:
        rate_limit_errors = sum(1 for e in stats["error_details"] if "429" in str(e.get("error", "")))
        if rate_limit_errors > 0:
            recommendations.append(f"⚠️  Detected {rate_limit_errors} rate limit errors in the last hour")
            
            if current_batch == 1:
                recommendations.append("💡 Consider enabling batch processing: Set GEMINI_BATCH_SIZE=5")
            else:
                recommendations.append(f"💡 Consider increasing batch size: Set GEMINI_BATCH_SIZE={min(10, current_batch + 2)}")
    
    # Calculate optimal RPM based on usage
    if stats["emails_last_hour"] > 0:
        actual_rpm = stats["emails_last_hour"] / 60
        if actual_rpm > current_rpm * 0.8:
            recommendations.append(f"📈 High usage detected: {actual_rpm:.1f} requests/minute")
            recommendations.append("💡 Consider upgrading your Gemini API tier for higher limits")
    
    return recommendations


def print_report():
    """Print usage report and recommendations"""
    print("\n=== Gemini API Usage Monitor ===\n")
    
    # Current configuration
    print(f"Current Configuration:")
    print(f"  - Model: {settings.GEMINI_MODEL}")
    print(f"  - RPM Limit: {settings.GEMINI_REQUESTS_PER_MINUTE}")
    print(f"  - Batch Size: {settings.GEMINI_BATCH_SIZE}")
    print()
    
    # Get usage stats
    stats = get_usage_stats()
    
    print(f"Usage Statistics (Last Hour):")
    print(f"  - Emails Processed: {stats['emails_last_hour']}")
    print(f"  - Active Tasks: {stats['active_tasks']}")
    print(f"  - Recent Errors: {stats['recent_errors']}")
    print()
    
    # Analyze rate limit logs
    rate_limit_analysis = analyze_rate_limit_logs()
    if rate_limit_analysis:
        print(f"Rate Limit Analysis (Last 24 Hours):")
        print(f"  - Total Rate Limits Hit: {rate_limit_analysis['total_limits_24h']}")
        print(f"  - Limit Types:")
        for limit_type, count in rate_limit_analysis['limit_types'].items():
            print(f"    • {limit_type}: {count}")
        
        if rate_limit_analysis['most_recent']:
            recent = rate_limit_analysis['most_recent']
            print(f"\n  Most Recent Rate Limit:")
            print(f"    - Time: {recent['timestamp']}")
            print(f"    - Type: {recent['limit_type']}")
            print(f"    - Retry Info: {recent['retry_info']}")
            
            # Calculate when we can retry
            timestamp = datetime.fromisoformat(recent['timestamp'])
            time_since = datetime.now() - timestamp
            
            if recent['limit_type'] == 'Requests Per Minute (RPM)':
                if time_since < timedelta(minutes=1):
                    wait_time = timedelta(minutes=1) - time_since
                    print(f"    - Can Retry In: {wait_time.total_seconds():.0f} seconds")
                else:
                    print(f"    - Can Retry: NOW (RPM limit should be reset)")
            elif 'Daily' in recent['limit_type'] or 'RPD' in recent['limit_type']:
                # For daily limits, check if it's past midnight UTC
                utc_now = datetime.utcnow()
                utc_midnight = utc_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                wait_time = utc_midnight - utc_now
                print(f"    - Daily Limit Reset: {wait_time.total_seconds() / 3600:.1f} hours (at midnight UTC)")
        print()
    
    # Get recommendations
    recommendations = calculate_optimal_settings(stats)
    
    if recommendations:
        print("Recommendations:")
        for rec in recommendations:
            print(f"  {rec}")
        print()
    else:
        print("✅ System is running optimally!\n")
    
    # Show how to update settings
    print("To update settings, edit backend/.env:")
    print(f"  GEMINI_REQUESTS_PER_MINUTE=15  # Your new limit")
    print(f"  GEMINI_MODEL=gemini-1.5-flash  # For better performance")
    print(f"  GEMINI_BATCH_SIZE=5  # Process multiple emails at once")
    print()


if __name__ == "__main__":
    print_report()