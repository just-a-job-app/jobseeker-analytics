import pytest
from status_predictor import predict_interview_status

@pytest.mark.parametrize("subject, body, expected_status", [
    # Tests for 'Applied' status
    ("Your application has been received", "We have received your application.", "Applied"),
    ("Application Update", "Thank you for applying to the role. We have applied to the position.", "Applied"),

    # Tests for 'Interview Scheduled' status
    ("Interview Confirmation", "Your interview is confirmed.", "Interview Scheduled"),
    ("Interview Scheduled", "We are pleased to inform you that an interview has been scheduled.", "Interview Scheduled"),

    # Tests for 'Request for Availability' status
    ("Next Steps", "We would like to schedule a call to discuss your availability.", "Request for Availability"),
    ("Availability", "When are you available to chat?", "Request for Availability"),

    # Tests for 'On Hold' status
    ("Update", "Your application is currently on hold.", "On Hold"),
    ("Application Status", "We are holding your application for a future position.", "On Hold"),

    # Tests for 'Rejection' status
    ("Application Update", "We have decided not to move forward with your application.", "Rejection"),
    ("Thank you for your interest", "You are not the right fit for this position.", "Rejection"),

    # Tests for 'Offer Extended' status
    ("Job Offer", "We would like to extend an offer of employment.", "Offer Extended"),
    ("Congratulations!", "We are pleased to congratulate you on your offer.", "Offer Extended"),

    # Test for 'No Response' status (default)
    ("A generic email", "This email has no keywords.", "No Response"),
])
def test_status_predictor(subject, body, expected_status):
    email_data = {"subject": subject, "body": body}
    assert predict_interview_status(email_data) == expected_status