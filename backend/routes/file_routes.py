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
    
    # Get job related email data from DB
    emails = query_emails(request, db_session=db_session, user_id=user_id)
    if not emails:
        raise HTTPException(status_code=400, detail="No data found to write")
    
    # Count unique company-job combinations and track statuses
    unique_applications = set()
    status_counts = {}
    unique_status_counts = {}
    
    for email in emails:
        # Create unique identifier for company-job combination
        company = email.company_name.strip()
        job_title = email.job_title.strip() if email.job_title else "Unknown Position"
        unique_key = f"{company}-{job_title}"
        
        # Track status
        status = email.application_status.strip()
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Track unique applications by status
        if unique_key not in unique_applications:
            unique_applications.add(unique_key)
            unique_status_counts[status] = unique_status_counts.get(status, 0) + 1
    
    # Use unique counts for Sankey diagram
    num_unique_applications = len(unique_applications)
    num_offers = unique_status_counts.get("Offer made", 0)
    num_rejected = unique_status_counts.get("Rejection", 0)
    num_interview = unique_status_counts.get("Interview invitation", 0)
    num_availability = unique_status_counts.get("Availability request", 0)
    num_assessment = unique_status_counts.get("Assessment sent", 0)
    num_no_response = unique_status_counts.get("Action required from company", 0)
    
    # Calculate ghosted/no reply (applications with "Applied" status)
    num_ghosted = unique_status_counts.get("Applied", 0)

    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            label=[f"Unique Applications ({num_unique_applications})", 
                   f"Offers ({num_offers})", 
                   f"Rejected ({num_rejected})", 
                   f"Interviews ({num_interview})", 
                   f"Availability Requests ({num_availability})", 
                   f"Assessments ({num_assessment})",
                   f"Awaiting Response ({num_no_response})",
                   f"Ghosted/No Reply ({num_ghosted})"],
            color=["blue", "green", "red", "orange", "yellow", "purple", "gray", "black"]
        ),
        link=dict(
            source=[0, 0, 0, 0, 0, 0, 0], 
            target=[1, 2, 3, 4, 5, 6, 7], 
            value=[num_offers, num_rejected, num_interview, num_availability, num_assessment, num_no_response, num_ghosted]
        )
    ))
    
    # Update layout for better visibility
    fig.update_layout(
        title="Job Application Flow",
        font=dict(size=12),
        width=1200,
        height=600
    )


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


# Generate pie chart for application status distribution
@router.get("/process-pie-chart")
@limiter.limit("2/minute")
async def process_pie_chart(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    if not user_id:
        return RedirectResponse("/logout", status_code=303)
    
    # Get job related email data from DB
    emails = query_emails(request, db_session=db_session, user_id=user_id)
    if not emails:
        raise HTTPException(status_code=400, detail="No data found to write")
    
    # Count statuses
    status_counts = {}
    for email in emails:
        status = email.application_status.strip()
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(status_counts.keys()),
        values=list(status_counts.values()),
        hole=0.3,  # Creates a donut chart
        textinfo='label+percent',
        textposition='auto',
        marker=dict(
            colors=['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
        )
    )])
    
    fig.update_layout(
        title="Application Status Distribution",
        font=dict(size=14),
        width=800,
        height=600,
        showlegend=True
    )
    
    # Save the chart
    directory = get_user_filepath(user_id)
    filename = "status_pie_chart.png"
    filepath = os.path.join(directory, filename)
    os.makedirs(directory, exist_ok=True)
    
    try:
        fig.write_image(filepath)
        logger.info("user_id:%s Pie chart saved to %s", user_id, filepath)
        
        return FileResponse(
            filepath,
            media_type="image/png",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error("Error generating pie chart for user_id:%s - %s", user_id, str(e))
        raise HTTPException(status_code=500, detail="Error generating pie chart")


# Generate weekly applications timeline graph
@router.get("/process-weekly-graph")
@limiter.limit("2/minute")
async def process_weekly_graph(request: Request, db_session: database.DBSession, user_id: str = Depends(validate_session)):
    if not user_id:
        return RedirectResponse("/logout", status_code=303)
    
    # Get job related email data from DB
    emails = query_emails(request, db_session=db_session, user_id=user_id)
    if not emails:
        raise HTTPException(status_code=400, detail="No data found to write")
    
    from datetime import datetime, timedelta
    from collections import defaultdict
    
    # Group emails by week
    weekly_counts = defaultdict(int)
    
    for email in emails:
        # Get the start of the week for this email
        email_date = email.received_at
        start_of_week = email_date - timedelta(days=email_date.weekday())
        week_key = start_of_week.strftime("%Y-%m-%d")
        weekly_counts[week_key] += 1
    
    # Sort weeks chronologically
    sorted_weeks = sorted(weekly_counts.items())
    
    # Prepare data for plotting
    weeks = [week[0] for week in sorted_weeks]
    counts = [week[1] for week in sorted_weeks]
    
    # Create line graph with markers
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=counts,
        mode='lines+markers+text',
        name='Applications',
        line=dict(color='#3498db', width=3),
        marker=dict(size=10, color='#2c3e50'),
        text=counts,
        textposition="top center",
        textfont=dict(size=12)
    ))
    
    # Add a bar chart overlay for better visibility
    fig.add_trace(go.Bar(
        x=weeks,
        y=counts,
        name='Weekly Total',
        marker_color='rgba(52, 152, 219, 0.3)',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Weekly Job Applications",
        xaxis_title="Week Starting",
        yaxis_title="Number of Applications",
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            showticklabels=False
        ),
        font=dict(size=12),
        width=1200,
        height=600,
        hovermode='x unified',
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white'
    )
    
    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    # Save the graph
    directory = get_user_filepath(user_id)
    filename = "weekly_applications_graph.png"
    filepath = os.path.join(directory, filename)
    os.makedirs(directory, exist_ok=True)
    
    try:
        fig.write_image(filepath)
        logger.info("user_id:%s Weekly graph saved to %s", user_id, filepath)
        
        return FileResponse(
            filepath,
            media_type="image/png",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        logger.error("Error generating weekly graph for user_id:%s - %s", user_id, str(e))
        raise HTTPException(status_code=500, detail="Error generating weekly graph")