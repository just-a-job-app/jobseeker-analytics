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
        if status == "offer":
            num_offers += 1
        elif status == "rejected":
            num_rejected += 1
        elif status == "request for availability":
            num_request_for_availability += 1
        elif status == "interview scheduled":
            num_interview_scheduled += 1
        elif status == "no response":
            num_no_response += 1

    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(label=[f"Applications ({num_applications})", 
                         f"Offers ({num_offers})", 
                         f"Rejected ({num_rejected})", 
                         f"Request for Availability ({num_request_for_availability})", 
                         f"Interview Scheduled ({num_interview_scheduled})", 
                         f"No Response ({num_no_response})"]),
        link=dict(source=[0, 0, 0, 0, 0], target=[1, 2, 3, 4, 5], 
                  value=[num_offers, num_rejected, num_request_for_availability, num_interview_scheduled, num_no_response])))


    # Define the user's file path and ensure the directory exists
    directory = get_user_filepath(user_id)
    filename = "sankey_diagram.png"
    filepath = os.path.join(directory, filename)

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    try:
        # Save the Sankey diagram as PNG
        fig.write_image(filepath)  # Requires Kaleido for image export
        logger.info("user_id:%s Sankey diagram saved to %s", user_id, filepath)

        # Return the file with correct headers and explicit filename
        return FileResponse(
            filepath,
            media_type="image/png",  # Correct media type for PNG
            filename=filename, 
            headers={"Content-Disposition": f"attachment; filename={filename}"}  # Ensure correct filename in header
        )
    except Exception as e:
        logger.error("Error generating Sankey diagram for user_id:%s - %s", user_id, str(e))
        raise HTTPException(status_code=500, detail="Error generating Sankey diagram")

   