import csv
import os
import logging
import plotly.graph_objects as go
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import FileResponse, RedirectResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import database
from utils.file_utils import get_user_filepath
from session.session_layer import validate_session
from routes.email_routes import query_emails
from utils.config_utils import get_settings

settings = get_settings()

# Logger setup
logger = logging.getLogger(__name__)

# FastAPI router for file routes
router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/download-file")
async def download_file(request: Request, user_id: str = Depends(validate_session)):
    if not user_id:
        return RedirectResponse("/logout", status_code=303)
    directory = get_user_filepath(user_id)
    filename = "emails.csv"
    filepath = f"{directory}/{filename}"
    if os.path.exists(filepath):
        logger.info("user_id:%s downloading from filepath %s", user_id, filepath)
        return FileResponse(filepath)
    raise HTTPException(status_code=400, detail="File not found")


# Write and download csv
@router.get("/process-csv")
@limiter.limit("2/minute")
async def process_csv(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    if not user_id:
        return RedirectResponse("/logout", status_code=303)

    directory = get_user_filepath(user_id)
    filename = "emails.csv"
    filepath = os.path.join(directory, filename)
    
    # Get job related email data from DB
    emails = query_emails(request, db_session=db_session, user_id=user_id)
    if not emails:
        raise HTTPException(status_code=400, detail="No data found to write")
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Key: DB field name; Value: Human-readable field name
    field_mapping = {
        "company_name": "Company Name",
        "application_status": "Application Status",
        "received_at": "Received At",
        "job_title": "Job Title",
        "subject": "Subject",
        "email_from": "Sender"
    }

    if not settings.is_publicly_deployed:
        logger.info("DEBUG: Adding message id to output")
        field_mapping.update({"id": "Message ID"})

    selected_fields = list(field_mapping.keys())
    headers = list(field_mapping.values())

    # Filter out unwanted fields
    processed_emails = [
        {key: value for key, value in email if key in selected_fields} for email in emails
    ]

    # Write to CSV
    with open(filepath, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in processed_emails:
            writer.writerow([row[field] for field in selected_fields])

    logger.info("CSV file created at %s", filepath)
    
    # Download CSV
    if os.path.exists(filepath):
        logger.info("user_id:%s downloading from filepath %s", user_id, filepath)
        return FileResponse(filepath)
    
    # File not found error
    raise HTTPException(status_code=400, detail="File not found")


# Write and download sankey diagram
@router.get("/process-sankey")
@limiter.limit("2/minute")
async def process_sankey(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    # Validate user session, redirect if invalid
    if not user_id:
        return RedirectResponse("/logout", status_code=303)
    
    num_applications = 0
    num_offers = 0
    num_rejected = 0
    num_request_for_availability = 0
    num_interview_scheduled = 0
    num_no_response = 0

    # Get job related email data from DB
    emails = query_emails(request, db_session=db_session, user_id=user_id)
    if not emails:
        raise HTTPException(status_code=400, detail="No data found to write")
    
    for email in emails:
        # normalize the output
        status = email.application_status.strip().lower()
        num_applications += 1
        
        # Use more flexible matching to handle variations in LLM output
        if any(keyword in status for keyword in ["offer", "offer made", "congratulations", "pleased to offer"]):
            num_offers += 1
        elif any(keyword in status for keyword in ["reject", "rejected", "rejection", "regret", "unfortunately"]):
            num_rejected += 1
        elif any(keyword in status for keyword in ["availability", "request for availability", "schedule", "when are you available"]):
            num_request_for_availability += 1
        elif any(keyword in status for keyword in ["interview", "call", "meeting", "invite"]):
            num_interview_scheduled += 1
        elif any(keyword in status for keyword in ["no response", "no reply", "unresponsive", "freeze", "hold", "paused", "canceled"]):
            num_no_response += 1
        elif any(keyword in status for keyword in ["assessment", "test", "challenge", "assignment"]):
            num_interview_scheduled += 1
        else:
            # Fallback: treat unknown statuses as no response
            num_no_response += 1
    
    # Check if we have any categorized data
    total_categorized = num_offers + num_rejected + num_request_for_availability + num_interview_scheduled + num_no_response
    if total_categorized == 0:
        logger.warning("user_id:%s - No emails matched any status categories, creating fallback diagram", user_id)
        # Create a simple fallback diagram
        num_no_response = num_applications

    # Create the enhanced Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color="black", width=1),
            label=[f"Applications ({num_applications})", 
                   f"Offers ({num_offers})", 
                   f"Rejected ({num_rejected})", 
                   f"Request for Availability ({num_request_for_availability})", 
                   f"Interview Scheduled ({num_interview_scheduled})", 
                   f"No Response ({num_no_response})"],
            color=["#1f77b4", "#2ca02c", "#d62728", "#ff7f0e", "#9467bd", "#8c564b"]
        ),
        link=dict(
            source=[0, 0, 0, 0, 0], 
            target=[1, 2, 3, 4, 5], 
            value=[num_offers, num_rejected, num_request_for_availability, num_interview_scheduled, num_no_response],
            color=["rgba(50, 160, 44, 0.4)", "rgba(214, 39, 40, 0.4)", "rgba(255, 127, 14, 0.4)", 
                   "rgba(148, 103, 189, 0.4)", "rgba(140, 86, 75, 0.4)"]
        )
    ))
    
    # Add proper layout configuration
    fig.update_layout(
        title={
            'text': f"Job Application Flow Analysis<br><sub>Total Applications: {num_applications}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': '#2E86AB'}
        },
        font=dict(size=18, family="Arial, sans-serif"),
        width=1200,
        height=700,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=50, r=50, t=100, b=50)
    )


    # Define the user's file path and ensure the directory exists
    directory = get_user_filepath(user_id)
    filename = "sankey_diagram.png"
    filepath = os.path.join(directory, filename)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    try:
        # Save the Sankey diagram as PNG with enhanced settings
        fig.write_image(
            filepath, 
            width=1200, 
            height=700, 
            scale=2,  # High resolution
            format="png",
            engine="kaleido"
        )
        
        # Verify the file was created and has content
        if not os.path.exists(filepath):
            raise Exception("Sankey diagram file was not created")
        
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            raise Exception("Sankey diagram file is empty")
        
        logger.info("user_id:%s Sankey diagram saved to %s (size: %d bytes)", user_id, filepath, file_size)

        # Return the file with correct headers and explicit filename
        return FileResponse(
            filepath,
            media_type="image/png",  # Correct media type for PNG
            filename=filename, 
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except Exception as e:
        logger.error("Error generating Sankey diagram for user_id:%s - %s", user_id, str(e))
        
        # Clean up any partially created file
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info("Cleaned up partially created file: %s", filepath)
            except Exception as cleanup_error:
                logger.warning("Failed to clean up file %s: %s", filepath, str(cleanup_error))
        
        # Try to create a simple text-based fallback image
        try:
            import matplotlib.pyplot as plt
            
            fig_fallback, ax = plt.subplots(figsize=(12, 8))
            ax.text(0.5, 0.7, f"Sankey Diagram Generation Failed", 
                   ha='center', va='center', fontsize=20, color='red')
            ax.text(0.5, 0.5, f"Total Applications: {num_applications}", 
                   ha='center', va='center', fontsize=16)
            ax.text(0.5, 0.4, f"Offers: {num_offers} | Rejected: {num_rejected}", 
                   ha='center', va='center', fontsize=14)
            ax.text(0.5, 0.3, f"Interviews: {num_interview_scheduled} | Availability Requests: {num_request_for_availability}", 
                   ha='center', va='center', fontsize=14)
            ax.text(0.5, 0.1, "Please contact support if this issue persists", 
                   ha='center', va='center', fontsize=12, color='gray')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            fallback_filename = "sankey_fallback.png"
            fallback_filepath = os.path.join(directory, fallback_filename)
            plt.savefig(fallback_filepath, dpi=150, bbox_inches='tight')
            plt.close()
            
            return FileResponse(
                fallback_filepath,
                media_type="image/png",
                filename=fallback_filename,
                headers={"Content-Disposition": f"attachment; filename={fallback_filename}"}
            )
        except Exception as fallback_error:
            logger.error("Fallback diagram creation also failed: %s", str(fallback_error))
            raise HTTPException(status_code=500, detail=f"Error generating Sankey diagram: {str(e)}")

   