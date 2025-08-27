import pytest
import json

@pytest.mark.parametrize("subject, body, expected_status", [
    # Test a positive case for a successful status
    ("Interview Scheduled", "We are pleased to inform you that an interview has been scheduled.", "Interview Scheduled"),
    # Test for a variation
    ("Thank you for your interest", "We have decided not to move forward with your application.", "Rejection"),
    # Test for a successful default status
    ("A generic email", "This email has no keywords.", "No Response"),
])

def test_predict_status_success(logged_in_client, subject, body, expected_status):
    # Prepare the JSON payload for the POST request
    payload = {
        "subject": subject,
        "body": body
    }

    # Make the POST request to your API route
    response = logged_in_client.post("/status", data=json.dumps(payload))

    # Assert that the response was successful
    assert response.status_code == 200

    # Assert that the returned JSON data contains the correct status
    assert response.json()["status"] == expected_status

def test_predict_status_invalid_payload(logged_in_client):
    # Prepare a payload with missing data
    invalid_payload = {
        "subject": "Missing body"
    }

    # Make the POST request with the invalid payload
    response = logged_in_client.post("/status", data=json.dumps(invalid_payload))

    # Assert that the API correctly returns a validation error
    assert response.status_code == 422
    assert "body" in response.json()["detail"][0]["loc"]