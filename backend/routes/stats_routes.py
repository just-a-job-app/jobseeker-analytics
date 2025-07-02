import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
import database
from db.user_emails import UserEmails
from session.session_layer import validate_session
from slowapi import Limiter
from slowapi.util import get_remote_address

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/api/stats")
@limiter.limit("10/minute")
async def get_user_stats(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    """Get comprehensive statistics for the user's job applications"""
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        # Get all emails for the user
        statement = select(UserEmails).where(UserEmails.user_id == user_id)
        emails = db_session.exec(statement).all()
        
        # Calculate basic stats
        total_emails = len(emails)
        
        # Count by status
        status_counts = {}
        company_counts = {}
        
        for email in emails:
            # Count statuses
            status = email.application_status.strip()
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count unique companies
            company = email.company_name.strip()
            if company and company.lower() != "unknown":
                company_counts[company] = company_counts.get(company, 0) + 1
        
        # Calculate time-based stats
        if emails:
            sorted_emails = sorted(emails, key=lambda x: x.received_at)
            first_application = sorted_emails[0].received_at
            last_application = sorted_emails[-1].received_at
            days_active = (last_application - first_application).days + 1
            
            # Last 7 days and 30 days stats
            now = datetime.now()
            last_7_days = sum(1 for e in emails if (now - e.received_at).days <= 7)
            last_30_days = sum(1 for e in emails if (now - e.received_at).days <= 30)
            
            # Calculate response rate
            total_applications = status_counts.get("Applied", 0)
            responses = sum(v for k, v in status_counts.items() 
                          if k not in ["Applied", "Action required from company", "False positive"])
            response_rate = (responses / total_applications * 100) if total_applications > 0 else 0
        else:
            first_application = None
            last_application = None
            days_active = 0
            last_7_days = 0
            last_30_days = 0
            response_rate = 0
        
        # Prepare response
        stats = {
            "overview": {
                "total_emails": total_emails,
                "unique_companies": len(company_counts),
                "total_applications": status_counts.get("Applied", 0),
                "days_active": days_active,
                "first_application": first_application.isoformat() if first_application else None,
                "last_application": last_application.isoformat() if last_application else None,
                "response_rate": round(response_rate, 1)
            },
            "status_breakdown": {
                "rejections": status_counts.get("Rejection", 0),
                "interviews": status_counts.get("Interview invitation", 0),
                "offers": status_counts.get("Offer made", 0),
                "assessments": status_counts.get("Assessment sent", 0),
                "awaiting_response": status_counts.get("Action required from company", 0),
                "availability_requests": status_counts.get("Availability request", 0),
                "information_requests": status_counts.get("Information request", 0),
                "inbound_requests": status_counts.get("Did not apply - inbound request", 0),
                "withdrew": status_counts.get("Withdrew application", 0),
                "hiring_freeze": status_counts.get("Hiring freeze notification", 0)
            },
            "activity": {
                "last_7_days": last_7_days,
                "last_30_days": last_30_days,
                "avg_per_week": round(total_emails / max(days_active / 7, 1), 1) if days_active > 0 else 0
            },
            "top_companies": sorted(
                [{"company": k, "count": v} for k, v in company_counts.items()],
                key=lambda x: x["count"],
                reverse=True
            )[:10],
            "status_distribution": [
                {"status": k, "count": v, "percentage": round(v / total_emails * 100, 1)} 
                for k, v in sorted(status_counts.items(), key=lambda x: x[1], reverse=True)
            ]
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")