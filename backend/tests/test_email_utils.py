from unittest import mock
import pytest

from tests.test_constants import SAMPLE_MESSAGE, SUBJECT_LINE
import utils.email_utils as email_utils
import db.utils.user_email_utils as user_email_utils

def test_get_top_consecutive_capitalized_words():
    test_cases = {
        (
            ("Hello", 10),  # capitalized, highest frequency, prioritize
            ("World", 8),  # capitalized, lower frequency, ignore
        ): "Hello",
        (
            ("Hello", 10),  # capitalized, highest frequency, prioritize
            ("World", 10),  # capitalized, highest frequency, add to result
            ("How", 5),  # capitalized, lower frequency, ignore
        ): "Hello World",
        (
            ("hello", 5),  # not capitalized, highest frequency, ignore
            ("World", 5),  # capitalized, highest frequency, prioritize
            ("How", 5),  # capitalized, highest frequency, add to result
            ("are", 5),  # not capitalized, highest frequency, ignore
        ): "World How",
        (
            ("hello", 5),  # not capitalized, highest frequency, ignore
            ("world", 5),  # capitalized, highest frequency, prioritize
            ("how", 5),  # capitalized, highest frequency, add to result
            ("are", 5),  # not capitalized, highest frequency, ignore
        ): "",  # no consecutive capitalized words
    }
    for word_list, expected_value in test_cases.items():
        result = email_utils.get_top_consecutive_capitalized_words(word_list)
        assert result == expected_value


def test_is_valid_email():
    email_test_cases = {
        "no-reply@gmail.com": True,
        "no-reply@example.com": False,  # Invalid domain
        "no-reply.com": False,  # Missing @
    }
    for email, expected_value in email_test_cases.items():
        is_valid = email_utils.is_valid_email(email)
        assert is_valid == expected_value, "email: %s" % email


def test_is_email_automated():
    email_test_cases = {
        "no-reply@example.com": True,
        "team@hi.wellfound.com": True,
        "hello@otta.com": True,
        "do-not-reply@example.com": True,
        "notifications@smartrecruiters.com": True,
        "person@yesimreal.com": False,
    }
    for email, expected_value in email_test_cases.items():
        is_automated = email_utils.is_automated_email(email)
        assert is_automated == expected_value, "email: %s" % email


def test_get_email_subject_line():
    subject_line = email_utils.get_email_subject_line(SAMPLE_MESSAGE)
    assert (
        subject_line
        == "Invitation from an unknown sender: Interview with TestCompanyName @ Thu May 2, 2024 11:00am - 12pm (PDT) (appuser@gmail.com)"
    )


def test_get_email_from_address():
    from_address = email_utils.get_email_from_address(SAMPLE_MESSAGE)
    assert from_address == "recruitername@testcompanyname.com"


def test_get_email_domain():
    from_email_domain = email_utils.get_email_domain_from_address(
        "recruitername@testcompanyname.com"
    )
    assert from_email_domain == "testcompanyname.com"


def test_is_generic_email_domain():
    assert email_utils.is_generic_email_domain("hire.lever.co")
    assert email_utils.is_generic_email_domain("us.greenhouse-mail.io")


def test_get_last_capitalized_words_in_line():
    last_capitalized_words = email_utils.get_last_capitalized_words_in_line(
        "Thank you for your application to CompanyName"
    )
    assert last_capitalized_words == "CompanyName"


def test_get_company_name_returns_email_domain():
    company_name = email_utils.get_company_name(
        id="abc123", msg=SAMPLE_MESSAGE, subject_line=SUBJECT_LINE
    )
    assert company_name == "testcompanyname"


def test_get_company_name_returns_top_word():
    """Default behavior for company name is to return the
    highest frequency word that appears in the email body."""
    with mock.patch(
        "utils.email_utils.get_top_word_in_email_body", return_value="FakeCompany"
    ):
        company_name = email_utils.get_company_name(
            id="abc123", msg=SAMPLE_MESSAGE, subject_line=SUBJECT_LINE
        )
        assert company_name == "FakeCompany"


def test_get_company_name_returns_last_capital_word_in_subject_line():
    """Default behavior for company name is to return the
    highest frequency word that appears in the email body."""
    with (
        mock.patch(
            "utils.email_utils.get_top_word_in_email_body", return_value="interview"
        ),
        mock.patch(
            "utils.email_utils.get_email_from_address",
            return_value="no-reply@us.greenhouse-mail.io",
        ),
    ):
        company_name = email_utils.get_company_name(
            id="abc123",
            msg=SAMPLE_MESSAGE,
            subject_line="Thanks for interviewing with CoolCompany",
        )
        assert company_name == "CoolCompany"


def test_get_email_received_at_timestamp():
    received_at = email_utils.get_received_at_timestamp(1, SAMPLE_MESSAGE)
    assert received_at == "Thu, 2 May 2024 16:45:00 +0000"


@pytest.fixture
def mock_user():
    user = mock.MagicMock()
    user.user_id = "test_user_123"
    return user


@pytest.fixture
def message_data_with_list_values():
    """Message data where received_at is a list instead of a string"""
    return {
        "id": "19501385930c533f",
        "company_name": "",
        "application_status": "",
        "received_at": "Thu, 13 Feb 2025 21:30:24 +0000 (UTC)",
        "subject": "Message replied: Are you looking for Remote opportunities?",
        "job_title": "",
        "from": "Tester Recruiter <hit-reply@linkedin.com>"
    }


@mock.patch('db.utils.user_email_utils.check_email_exists')
def test_create_user_email_with_list_values(mock_check_email, mock_user, message_data_with_list_values, caplog):
    """Test that create_user_email handles message_data_with_list_values correctly"""
    mock_check_email.return_value = False
    result = user_email_utils.create_user_email(mock_user, message_data_with_list_values)
    assert result is not None  # user email created successfully

def test_clean_whitespace():
    assert email_utils.clean_whitespace("hello\nworld\r\ttest") == "helloworldtest"
    assert email_utils.clean_whitespace("nowhitespace") == "nowhitespace"
    assert email_utils.clean_whitespace("") == ""
    assert email_utils.clean_whitespace(None) == ""
    
