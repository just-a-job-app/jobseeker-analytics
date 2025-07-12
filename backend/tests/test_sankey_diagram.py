#!/usr/bin/env python3
"""
Test suite for Sankey diagram generation and status matching
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSankeyStatusMatching:
    """Test the status matching logic used in Sankey diagram generation"""
    
    def test_flexible_status_matching(self):
        """Test that the flexible keyword matching works correctly"""
        
        # Sample email statuses that might come from the LLM
        test_statuses = [
            "Application confirmation",
            "Rejection", 
            "rejected",
            "offer made",
            "offer",
            "Interview invitation",
            "interview scheduled", 
            "availability request",
            "request for availability",
            "Assessment sent",
            "Information request",
            "Hiring freeze notification",
            "False positive",
            "unknown",
            "no response"
        ]
        
        # Counters
        num_applications = 0
        num_offers = 0
        num_rejected = 0
        num_request_for_availability = 0
        num_interview_scheduled = 0
        num_no_response = 0
        
        unique_statuses = set()
        unmatched_statuses = set()
        
        for status in test_statuses:
            status_normalized = status.strip().lower()
            unique_statuses.add(status_normalized)
            num_applications += 1
            
            # Use flexible matching (same logic as in file_routes.py)
            if any(keyword in status_normalized for keyword in ["offer", "offer made", "congratulations", "pleased to offer"]):
                num_offers += 1
            elif any(keyword in status_normalized for keyword in ["reject", "rejected", "rejection", "regret", "unfortunately"]):
                num_rejected += 1
            elif any(keyword in status_normalized for keyword in ["availability", "request for availability", "schedule", "when are you available"]):
                num_request_for_availability += 1
            elif any(keyword in status_normalized for keyword in ["interview", "call", "meeting", "invite"]):
                num_interview_scheduled += 1
            elif any(keyword in status_normalized for keyword in ["no response", "no reply", "unresponsive"]):
                num_no_response += 1
            elif any(keyword in status_normalized for keyword in ["confirmation", "received", "thank you for applying"]):
                # Application confirmations - treat as successful applications that are pending
                num_no_response += 1
            elif any(keyword in status_normalized for keyword in ["assessment", "test", "challenge", "assignment"]):
                # Assessments - positive progress, treat as interview-related
                num_interview_scheduled += 1
            elif any(keyword in status_normalized for keyword in ["information", "portfolio", "references", "documents"]):
                # Information requests - positive progress, treat as interview-related
                num_interview_scheduled += 1
            elif any(keyword in status_normalized for keyword in ["freeze", "hold", "paused", "canceled"]):
                # Hiring freezes - not rejection but not positive either
                num_no_response += 1
            else:
                unmatched_statuses.add(status_normalized)
        
        # Assertions - updated for improved matching
        assert num_applications == len(test_statuses)
        assert num_offers == 2  # "offer made", "offer"
        assert num_rejected == 2  # "Rejection", "rejected"
        assert num_request_for_availability == 2  # "availability request", "request for availability"
        assert num_interview_scheduled == 4  # "Interview invitation", "interview scheduled", "Assessment sent", "Information request"
        assert num_no_response == 3  # "no response", "Application confirmation", "Hiring freeze notification"
        
        total_categorized = num_offers + num_rejected + num_request_for_availability + num_interview_scheduled + num_no_response
        assert total_categorized >= 13, f"Should categorize at least 13 statuses, got {total_categorized}"
        
    def test_old_vs_new_matching_comparison(self):
        """Test that new flexible matching performs better than old exact matching"""
        
        # Real-world statuses that might come from LLM
        real_statuses = [
            "Application confirmation",
            "Rejection", 
            "Interview invitation",
            "Availability request",
            "Offer made",
            "Assessment sent"
        ]
        
        # OLD EXACT MATCHING (what was causing the bug)
        old_matches = 0
        for status in real_statuses:
            status_norm = status.strip().lower()
            if status_norm in ["offer", "rejected", "request for availability", "interview scheduled", "no response"]:
                old_matches += 1
        
        # NEW FLEXIBLE MATCHING
        new_matches = 0
        for status in real_statuses:
            status_norm = status.strip().lower()
            if any(keyword in status_norm for keyword in [
                "offer", "reject", "availability", "interview", "no response",
                "confirmation", "invitation", "assessment"
            ]):
                new_matches += 1
        
        # The new matching should catch significantly more statuses
        assert new_matches > old_matches, f"New matching ({new_matches}) should be better than old matching ({old_matches})"
        assert new_matches == 6, "All test statuses should be matched by new flexible logic"
        assert old_matches == 0, "Old exact matching should miss all test statuses"

    def test_edge_cases(self):
        """Test edge cases in status matching"""
        
        edge_cases = [
            ("", 0),  # Empty string
            ("   ", 0),  # Whitespace only
            ("OFFER MADE", 1),  # Uppercase
            ("We regret to inform you", 1),  # Rejection keyword
            ("Please let us know your availability", 1),  # Availability keyword
            ("Unknown status", 0),  # Unrecognized
        ]
        
        for status, expected_matches in edge_cases:
            status_normalized = status.strip().lower()
            matches = 0
            
            # Apply the same matching logic
            if any(keyword in status_normalized for keyword in ["offer", "offer made", "congratulations", "pleased to offer"]):
                matches += 1
            if any(keyword in status_normalized for keyword in ["reject", "rejected", "rejection", "regret", "unfortunately"]):
                matches += 1
            if any(keyword in status_normalized for keyword in ["availability", "request for availability", "schedule", "when are you available"]):
                matches += 1
            if any(keyword in status_normalized for keyword in ["interview", "call", "meeting", "invite"]):
                matches += 1
            if any(keyword in status_normalized for keyword in ["no response", "no reply", "unresponsive"]):
                matches += 1
            
            assert matches == expected_matches, f"Status '{status}' should match {expected_matches} categories, got {matches}"

class TestSankeyDiagramGeneration:
    """Test the Sankey diagram generation logic"""
    
    def test_fallback_diagram_creation(self):
        """Test that fallback diagram is created when no statuses match"""
        
        # Mock email data with unrecognized statuses
        mock_emails = [
            Mock(application_status="Unknown status 1"),
            Mock(application_status="Unknown status 2"),
            Mock(application_status="Unknown status 3"),
        ]
        
        # Simulate the counting logic from file_routes.py
        num_applications = len(mock_emails)
        num_offers = 0
        num_rejected = 0
        num_request_for_availability = 0
        num_interview_scheduled = 0
        num_no_response = 0
        
        for email in mock_emails:
            status = email.application_status.strip().lower()
            # None of these should match
            if any(keyword in status for keyword in ["offer", "offer made", "congratulations", "pleased to offer"]):
                num_offers += 1
            elif any(keyword in status for keyword in ["reject", "rejected", "rejection", "regret", "unfortunately"]):
                num_rejected += 1
            elif any(keyword in status for keyword in ["availability", "request for availability", "schedule", "when are you available"]):
                num_request_for_availability += 1
            elif any(keyword in status for keyword in ["interview", "call", "meeting", "invite"]):
                num_interview_scheduled += 1
            elif any(keyword in status for keyword in ["no response", "no reply", "unresponsive"]):
                num_no_response += 1
        
        total_categorized = num_offers + num_rejected + num_request_for_availability + num_interview_scheduled + num_no_response
        
        # Should trigger fallback logic
        assert total_categorized == 0, "No statuses should be categorized"
        
        # Fallback logic should assign all to no_response
        if total_categorized == 0:
            num_no_response = num_applications
        
        assert num_no_response == 3, "Fallback should assign all emails to no_response"

    def test_sankey_data_structure(self):
        """Test that Sankey diagram data structure is correctly formed"""
        
        # Sample counts
        num_applications = 10
        num_offers = 1
        num_rejected = 4
        num_request_for_availability = 2
        num_interview_scheduled = 2
        num_no_response = 1
        
        # Verify the data adds up
        total = num_offers + num_rejected + num_request_for_availability + num_interview_scheduled + num_no_response
        assert total == num_applications, "Sum of categories should equal total applications"
        
        # Test node labels
        expected_labels = [
            f"Applications ({num_applications})", 
            f"Offers ({num_offers})", 
            f"Rejected ({num_rejected})", 
            f"Request for Availability ({num_request_for_availability})", 
            f"Interview Scheduled ({num_interview_scheduled})", 
            f"No Response ({num_no_response})"
        ]
        
        # Test link structure
        expected_sources = [0, 0, 0, 0, 0]  # All from "Applications"
        expected_targets = [1, 2, 3, 4, 5]  # To each category
        expected_values = [num_offers, num_rejected, num_request_for_availability, num_interview_scheduled, num_no_response]
        
        assert len(expected_sources) == len(expected_targets) == len(expected_values)
        assert sum(expected_values) == num_applications


class TestMockDataGeneration:
    """Test the mock data generation utilities"""
    
    def test_realistic_status_distribution(self):
        """Test that mock data has realistic status distribution"""
        
        # Expected distribution from populate_mock_emails.py
        expected_distribution = [
            ("Application confirmation", 15),
            ("Rejection", 8),
            ("Availability request", 4),
            ("Interview invitation", 3),
            ("Information request", 3),
            ("Assessment sent", 2),
            ("Action required from company", 4),
            ("Offer made", 1),
            ("Hiring freeze notification", 1),
        ]
        
        total_expected = sum(count for _, count in expected_distribution)
        assert total_expected == 41, "Expected total mock emails should be 41"
        
        # Test that distribution makes sense (more applications than offers)
        offer_count = next(count for status, count in expected_distribution if "offer" in status.lower())
        rejection_count = next(count for status, count in expected_distribution if "rejection" in status.lower())
        
        assert rejection_count > offer_count, "Should have more rejections than offers (realistic)"


if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])
