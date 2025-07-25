"""
Test email data for demo mode and automated testing.
Contains realistic job application emails with various statuses.
"""

from datetime import datetime, timezone
import uuid

# Demo test emails for live presentations
DEMO_TEST_EMAILS = [
    {
        "id": "demo_1",
        "company_name": "Ketryx",
        "application_status": "rejection",
        "received_at": datetime(2024, 3, 15, 14, 30, 0, tzinfo=timezone.utc),
        "subject": "Ketryx | Application Update",
        "job_title": "AI, Digital, and Cyber Compliance",
        "email_from": "people@ketryx.com",
        "email_body": """Thank you for your time and interest in applying to the AI, Digital, and Cyber Compliance position. We were overwhelmed with the amount and quality of applicants received; like you! Upon further review, the team was unable to select you as a top candidate for the current need. However, we highly encourage you to continue to watch our open positions and re-apply for another opportunity that fits your skill set and desire.

Best of luck in your search,

Ketryx People Operations""",
        "is_demo_email": True,
        "category": "rejection"
    },
    {
        "id": "demo_2",
        "company_name": "TechCorp Solutions",
        "application_status": "interview invitation",
        "received_at": datetime(2024, 3, 16, 10, 15, 0, tzinfo=timezone.utc),
        "subject": "Interview Invitation - Senior Software Engineer",
        "job_title": "Senior Software Engineer",
        "email_from": "hr@techcorp.com",
        "email_body": """Dear [Candidate Name],

Thank you for your interest in the Senior Software Engineer position at TechCorp Solutions. We are pleased to invite you for an interview.

We would like to schedule a 45-minute technical interview with our engineering team. Please let us know your availability for the following times:

- Monday, March 25th: 2:00 PM - 4:00 PM EST
- Tuesday, March 26th: 10:00 AM - 12:00 PM EST
- Wednesday, March 27th: 1:00 PM - 3:00 PM EST

The interview will include:
- Technical discussion about your experience
- Coding exercise
- Questions about our tech stack (Python, React, AWS)

Please confirm your preferred time slot and we'll send you the meeting link.

Best regards,
Sarah Johnson
HR Manager
TechCorp Solutions""",
        "is_demo_email": True,
        "category": "interview"
    },
    {
        "id": "demo_3",
        "company_name": "InnovateAI",
        "application_status": "application confirmation",
        "received_at": datetime(2024, 3, 17, 16, 45, 0, tzinfo=timezone.utc),
        "subject": "Application Received - Machine Learning Engineer",
        "job_title": "Machine Learning Engineer",
        "email_from": "noreply@innovateai.com",
        "email_body": """Thank you for your application to the Machine Learning Engineer position at InnovateAI!

We have successfully received your application and it is currently under review by our hiring team. You should expect to hear back from us within 5-7 business days.

Application Details:
- Position: Machine Learning Engineer
- Location: Remote (US)
- Application ID: ML-2024-001

If you have any questions about your application, please reply to this email or contact us at careers@innovateai.com.

Best regards,
InnovateAI Talent Team""",
        "is_demo_email": True,
        "category": "confirmation"
    },
    {
        "id": "demo_4",
        "company_name": "DataFlow Systems",
        "application_status": "assessment sent",
        "received_at": datetime(2024, 3, 18, 11, 20, 0, tzinfo=timezone.utc),
        "subject": "Next Steps: Technical Assessment - Data Engineer",
        "job_title": "Data Engineer",
        "email_from": "assessments@dataflow.com",
        "email_body": """Hello,

Thank you for your application to the Data Engineer position at DataFlow Systems. We'd like to move forward with your candidacy and have prepared a technical assessment for you.

Assessment Details:
- Duration: 90 minutes
- Format: Online coding challenge
- Topics: SQL, Python, Data modeling, ETL processes

Please complete the assessment within 48 hours. You can access it here: [Assessment Link]

The assessment will test your practical skills in:
- Writing efficient SQL queries
- Data pipeline design
- Python programming for data processing
- System design for data infrastructure

Good luck!

Best regards,
Technical Hiring Team
DataFlow Systems""",
        "is_demo_email": True,
        "category": "assessment"
    },
    {
        "id": "demo_5",
        "company_name": "CloudScale Inc",
        "application_status": "availability request",
        "received_at": datetime(2024, 3, 19, 9, 30, 0, tzinfo=timezone.utc),
        "subject": "Scheduling Request - DevOps Engineer Interview",
        "job_title": "DevOps Engineer",
        "email_from": "scheduling@cloudscale.com",
        "email_body": """Hi there,

Thanks for your application to the DevOps Engineer role at CloudScale Inc. We'd like to schedule a phone interview to discuss your background and the position.

Could you please let us know your availability for a 30-minute call during the following times:

This week:
- Thursday, March 21st: 1:00 PM - 5:00 PM EST
- Friday, March 22nd: 10:00 AM - 2:00 PM EST

Next week:
- Monday, March 25th: 2:00 PM - 6:00 PM EST
- Tuesday, March 26th: 9:00 AM - 1:00 PM EST

Please include your timezone and preferred time slots. We'll confirm the exact time and send you the meeting details.

Looking forward to speaking with you!

Best regards,
Mike Chen
Engineering Manager
CloudScale Inc""",
        "is_demo_email": True,
        "category": "scheduling"
    },
    {
        "id": "demo_6",
        "company_name": "StartupXYZ",
        "application_status": "offer made",
        "received_at": datetime(2024, 3, 20, 15, 15, 0, tzinfo=timezone.utc),
        "subject": "Offer Letter - Full Stack Developer",
        "job_title": "Full Stack Developer",
        "email_from": "offers@startupxyz.com",
        "email_body": """Congratulations!

We are excited to extend you an offer for the Full Stack Developer position at StartupXYZ. After reviewing your application and conducting our interviews, we believe you would be a great addition to our team.

Offer Details:
- Position: Full Stack Developer
- Start Date: April 15, 2024
- Salary: $120,000 annually
- Benefits: Health, dental, vision, 401k, unlimited PTO
- Equity: 0.1% stock options

Please review the attached offer letter and employment agreement. We would appreciate your response within 7 days.

If you have any questions about the offer or would like to discuss any terms, please don't hesitate to reach out.

Welcome to the team!

Best regards,
Jennifer Rodriguez
CEO & Co-founder
StartupXYZ""",
        "is_demo_email": True,
        "category": "offer"
    },
    {
        "id": "demo_7",
        "company_name": "Enterprise Solutions",
        "application_status": "information request",
        "received_at": datetime(2024, 3, 21, 13, 45, 0, tzinfo=timezone.utc),
        "subject": "Additional Information Needed - Product Manager",
        "job_title": "Product Manager",
        "email_from": "hr@enterprisesolutions.com",
        "email_body": """Dear Candidate,

Thank you for your application to the Product Manager position at Enterprise Solutions. We need some additional information to proceed with your application.

Please provide the following:

1. Portfolio or examples of products you've managed
2. References from previous employers (minimum 2)
3. Salary expectations for this role
4. Available start date
5. Work authorization status

Additionally, could you elaborate on your experience with:
- Agile/Scrum methodologies
- User research and analytics
- Cross-functional team leadership

Please send these materials within 5 business days to hr@enterprisesolutions.com.

Best regards,
Talent Acquisition Team
Enterprise Solutions""",
        "is_demo_email": True,
        "category": "information"
    },
    {
        "id": "demo_8",
        "company_name": "Growth Ventures",
        "application_status": "did not apply - inbound request",
        "received_at": datetime(2024, 3, 22, 10, 30, 0, tzinfo=timezone.utc),
        "subject": "Opportunity at Growth Ventures - Senior Developer",
        "job_title": "Senior Developer",
        "email_from": "recruiter@growthventures.com",
        "email_body": """Hi there,

I came across your profile and was impressed by your experience with React and Node.js. We have an exciting opportunity at Growth Ventures that I think would be a great fit for your skills.

We're looking for a Senior Developer to join our growing team. The role involves:
- Leading technical projects
- Mentoring junior developers
- Working with modern tech stack (React, Node.js, AWS)
- Competitive salary and benefits

Would you be interested in learning more about this opportunity? I'd love to schedule a quick call to discuss the role and see if it aligns with your career goals.

Best regards,
Alex Thompson
Technical Recruiter
Growth Ventures""",
        "is_demo_email": True,
        "category": "inbound"
    }
]

# Additional test emails for edge cases and testing
EDGE_CASE_TEST_EMAILS = [
    {
        "id": "edge_1",
        "company_name": "Frozen Corp",
        "application_status": "hiring freeze notification",
        "received_at": datetime(2024, 3, 23, 14, 20, 0, tzinfo=timezone.utc),
        "subject": "Position Update - Hiring Freeze",
        "job_title": "Software Engineer",
        "email_from": "hr@frozencorp.com",
        "email_body": """Dear Candidate,

We regret to inform you that due to current economic conditions, we have implemented a hiring freeze across all departments. The Software Engineer position you applied for has been put on hold indefinitely.

We will keep your application on file and will reach out if the position becomes available again in the future.

Thank you for your interest in joining our team.

Best regards,
HR Team
Frozen Corp""",
        "is_demo_email": False,
        "category": "freeze"
    },
    {
        "id": "edge_2",
        "company_name": "Withdrawn Inc",
        "application_status": "withdrew application",
        "received_at": datetime(2024, 3, 24, 16, 10, 0, tzinfo=timezone.utc),
        "subject": "Application Withdrawal Confirmation",
        "job_title": "UX Designer",
        "email_from": "hr@withdrawn.com",
        "email_body": """Hello,

We have received your request to withdraw your application for the UX Designer position. Your application has been successfully withdrawn from our system.

If you change your mind and would like to reapply in the future, please feel free to submit a new application.

Best regards,
HR Team
Withdrawn Inc""",
        "is_demo_email": False,
        "category": "withdrawal"
    }
]

# Function to get all demo emails
def get_demo_emails():
    """Return all demo emails for demo mode."""
    return DEMO_TEST_EMAILS

# Function to get all test emails (demo + edge cases)
def get_all_test_emails():
    """Return all test emails for comprehensive testing."""
    return DEMO_TEST_EMAILS + EDGE_CASE_TEST_EMAILS

# Function to get test emails by category
def get_test_emails_by_category(category):
    """Return test emails filtered by category."""
    all_emails = get_all_test_emails()
    return [email for email in all_emails if email.get("category") == category]

# Function to get test emails by status
def get_test_emails_by_status(status):
    """Return test emails filtered by application status."""
    all_emails = get_all_test_emails()
    return [email for email in all_emails if email.get("application_status") == status] 