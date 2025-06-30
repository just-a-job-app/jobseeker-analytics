#!/usr/bin/env python3
"""
Manage and analyze Gemini API rate limits
"""
import sys
import argparse
import json
from datetime import datetime, timedelta
from collections import defaultdict
from sqlmodel import Session, select
from database import engine
from db import processing_tasks as task_models
from utils.config_utils import get_settings

settings = get_settings()


def analyze_logs():
    """Analyze rate limit logs"""
    try:
        with open("gemini_rate_limits.log", "r") as f:
            logs = [json.loads(line) for line in f]
    except FileNotFoundError:
        print("No rate limit logs found.")
        return
    
    # Group by limit type
    by_type = defaultdict(list)
    for log in logs:
        by_type[log['limit_type']].append(log)
    
    print("\n=== Rate Limit Analysis ===\n")
    
    for limit_type, entries in by_type.items():
        print(f"{limit_type}:")
        print(f"  Total hits: {len(entries)}")
        
        if entries:
            # Find time patterns
            timestamps = [datetime.fromisoformat(e['timestamp']) for e in entries]
            
            # Check for bursts
            bursts = []
            for i in range(1, len(timestamps)):
                diff = (timestamps[i] - timestamps[i-1]).total_seconds()
                if diff < 300:  # Within 5 minutes
                    bursts.append(timestamps[i])
            
            if bursts:
                print(f"  Burst periods detected: {len(bursts)}")
            
            # Most recent
            most_recent = max(timestamps)
            time_since = datetime.now() - most_recent
            print(f"  Most recent: {time_since.total_seconds() / 60:.1f} minutes ago")
            
            # Can we retry now?
            if 'RPM' in limit_type:
                if time_since > timedelta(minutes=1):
                    print("  ✅ Can retry now (RPM limits reset after 1 minute)")
                else:
                    wait = 60 - time_since.total_seconds()
                    print(f"  ⏱️  Wait {wait:.0f} more seconds")
            elif 'Daily' in limit_type or 'RPD' in limit_type:
                utc_now = datetime.utcnow()
                last_midnight = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
                if most_recent.replace(tzinfo=None) < last_midnight:
                    print("  ✅ Can retry now (daily limit reset at midnight UTC)")
                else:
                    next_midnight = last_midnight + timedelta(days=1)
                    wait = (next_midnight - utc_now).total_seconds() / 3600
                    print(f"  ⏱️  Wait {wait:.1f} hours until midnight UTC")
        print()


def clear_logs():
    """Clear rate limit logs"""
    try:
        with open("gemini_rate_limits.log", "w") as f:
            f.write("")
        print("✅ Rate limit logs cleared")
    except:
        print("No logs to clear")


def reset_stuck_tasks():
    """Reset tasks that are stuck due to rate limits"""
    with Session(engine) as db_session:
        stuck_tasks = db_session.exec(
            select(task_models.TaskRuns)
            .where(task_models.TaskRuns.status == task_models.STARTED)
            .where(task_models.TaskRuns.error_message.like("%rate%"))
        ).all()
        
        if not stuck_tasks:
            print("No stuck tasks found")
            return
        
        print(f"\nFound {len(stuck_tasks)} stuck tasks:")
        for task in stuck_tasks:
            print(f"  - User: {task.user_id}")
            print(f"    Progress: {task.processed_emails}/{task.total_emails}")
            print(f"    Error: {task.error_message}")
        
        response = input("\nReset these tasks to allow retry? (y/N): ")
        if response.lower() == 'y':
            for task in stuck_tasks:
                # Keep progress but clear error and mark as finished
                task.status = task_models.FINISHED
                task.error_message = "Reset by admin - can retry"
            db_session.commit()
            print("✅ Tasks reset. Users can now retry processing.")


def show_recommendations():
    """Show recommendations based on current setup"""
    print("\n=== Recommendations ===\n")
    
    print("To avoid rate limits:")
    print("1. Enable billing in Google Cloud Console")
    print("   - Free tier: 2 RPM, 1000 requests/day")
    print("   - Paid tier: 15+ RPM, higher daily limits")
    print()
    print("2. Use batch processing:")
    print("   - Set GEMINI_BATCH_SIZE=5 in .env")
    print("   - This processes 5 emails per API call")
    print()
    print("3. Use a faster model:")
    print("   - gemini-2.0-flash-lite (current)")
    print("   - gemini-1.5-flash (faster, more expensive)")
    print()
    print("4. Request quota increase:")
    print("   - Go to Google Cloud Console")
    print("   - APIs & Services → Quotas")
    print("   - Request higher limits")


def main():
    parser = argparse.ArgumentParser(description="Manage Gemini API rate limits")
    parser.add_argument('command', choices=['analyze', 'clear', 'reset', 'recommend'],
                        help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_logs()
    elif args.command == 'clear':
        clear_logs()
    elif args.command == 'reset':
        reset_stuck_tasks()
    elif args.command == 'recommend':
        show_recommendations()


if __name__ == "__main__":
    main()