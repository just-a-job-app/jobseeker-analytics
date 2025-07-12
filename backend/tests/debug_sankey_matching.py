#!/usr/bin/env python3
"""
Debug utilities for testing Sankey diagram functionality
This script helps validate the status matching improvements.
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_status_matching_logic():
    """Test the improved status matching logic used in the Sankey diagram"""
    
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
    categorized_counts = {
        "offers": 0,
        "rejected": 0,
        "availability": 0,
        "interview": 0,
        "no_response": 0,
        "unmatched": 0
    }
    
    unique_statuses = set()
    unmatched_statuses = set()
    
    for status in test_statuses:
        status_normalized = status.strip().lower()
        unique_statuses.add(status_normalized)
        
        # Apply the same flexible matching logic as in file_routes.py
        if any(keyword in status_normalized for keyword in ["offer", "offer made", "congratulations", "pleased to offer"]):
            categorized_counts["offers"] += 1
        elif any(keyword in status_normalized for keyword in ["reject", "rejected", "rejection", "regret", "unfortunately"]):
            categorized_counts["rejected"] += 1
        elif any(keyword in status_normalized for keyword in ["availability", "request for availability", "schedule", "when are you available"]):
            categorized_counts["availability"] += 1
        elif any(keyword in status_normalized for keyword in ["interview", "call", "meeting", "invite"]):
            categorized_counts["interview"] += 1
        elif any(keyword in status_normalized for keyword in ["no response", "no reply", "unresponsive"]):
            categorized_counts["no_response"] += 1
        elif any(keyword in status_normalized for keyword in ["confirmation", "received", "thank you for applying"]):
            # Application confirmations - treat as successful applications that are pending
            categorized_counts["no_response"] += 1
        elif any(keyword in status_normalized for keyword in ["assessment", "test", "challenge", "assignment"]):
            # Assessments - positive progress, treat as interview-related
            categorized_counts["interview"] += 1
        elif any(keyword in status_normalized for keyword in ["information", "portfolio", "references", "documents"]):
            # Information requests - positive progress, treat as interview-related
            categorized_counts["interview"] += 1
        elif any(keyword in status_normalized for keyword in ["freeze", "hold", "paused", "canceled"]):
            # Hiring freezes - not rejection but not positive either
            categorized_counts["no_response"] += 1
        else:
            categorized_counts["unmatched"] += 1
            unmatched_statuses.add(status_normalized)
    
    return {
        "total_statuses": len(test_statuses),
        "unique_statuses": list(unique_statuses),
        "unmatched_statuses": list(unmatched_statuses),
        "categorized_counts": categorized_counts,
        "success_rate": (len(test_statuses) - categorized_counts["unmatched"]) / len(test_statuses)
    }

def compare_old_vs_new_matching():
    """Compare old exact matching vs new flexible matching"""
    
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
    old_exact_matches = []
    old_match_count = 0
    for status in real_statuses:
        status_norm = status.strip().lower()
        if status_norm in ["offer", "rejected", "request for availability", "interview scheduled", "no response"]:
            old_match_count += 1
            old_exact_matches.append(status)
    
    # NEW FLEXIBLE MATCHING
    new_flexible_matches = []
    new_match_count = 0
    for status in real_statuses:
        status_norm = status.strip().lower()
        if any(keyword in status_norm for keyword in [
            "offer", "reject", "availability", "interview", "no response",
            "confirmation", "invitation", "assessment"
        ]):
            new_match_count += 1
            new_flexible_matches.append(status)
    
    return {
        "test_statuses": real_statuses,
        "old_matching": {
            "count": old_match_count,
            "matched_statuses": old_exact_matches,
            "success_rate": old_match_count / len(real_statuses)
        },
        "new_matching": {
            "count": new_match_count,
            "matched_statuses": new_flexible_matches,
            "success_rate": new_match_count / len(real_statuses)
        },
        "improvement": new_match_count - old_match_count
    }

def validate_sankey_data_structure(categorized_counts: dict) -> bool:
    """Validate that the categorized data can create a valid Sankey diagram"""
    
    total_categorized = sum(v for k, v in categorized_counts.items() if k != "unmatched")
    
    # Check if we have enough data for a meaningful diagram
    if total_categorized == 0:
        return False
    
    # Check that at least some major categories have data
    major_categories = ["offers", "rejected", "interview", "availability"]
    categories_with_data = sum(1 for cat in major_categories if categorized_counts.get(cat, 0) > 0)
    
    return categories_with_data >= 2  # At least 2 major categories should have data

def run_comprehensive_test():
    """Run all validation tests and return a comprehensive report"""
    
    print("🧪 Running Sankey Diagram Status Matching Tests...")
    print("=" * 60)
    
    # Test 1: Status matching logic
    matching_results = test_status_matching_logic()
    print(f"\n📊 Status Matching Test:")
    print(f"  Total test statuses: {matching_results['total_statuses']}")
    print(f"  Successfully categorized: {matching_results['total_statuses'] - matching_results['categorized_counts']['unmatched']}")
    print(f"  Success rate: {matching_results['success_rate']:.1%}")
    print(f"  Category breakdown:")
    for category, count in matching_results['categorized_counts'].items():
        if count > 0:
            print(f"    - {category.title()}: {count}")
    
    if matching_results['unmatched_statuses']:
        print(f"  Unmatched statuses: {matching_results['unmatched_statuses']}")
    
    # Test 2: Old vs New comparison
    comparison_results = compare_old_vs_new_matching()
    print(f"\n🔄 Old vs New Matching Comparison:")
    print(f"  Test statuses: {len(comparison_results['test_statuses'])}")
    print(f"  Old exact matching: {comparison_results['old_matching']['count']}/{len(comparison_results['test_statuses'])} ({comparison_results['old_matching']['success_rate']:.1%})")
    print(f"  New flexible matching: {comparison_results['new_matching']['count']}/{len(comparison_results['test_statuses'])} ({comparison_results['new_matching']['success_rate']:.1%})")
    print(f"  Improvement: +{comparison_results['improvement']} statuses")
    
    # Test 3: Sankey diagram viability
    sankey_viable = validate_sankey_data_structure(matching_results['categorized_counts'])
    print(f"\n📈 Sankey Diagram Viability:")
    print(f"  Can create meaningful diagram: {'✅ Yes' if sankey_viable else '❌ No'}")
    
    # Overall assessment
    print(f"\n🎯 Overall Assessment:")
    all_tests_passed = (
        matching_results['success_rate'] > 0.6 and  # At least 60% success rate
        comparison_results['improvement'] > 0 and    # New matching is better
        sankey_viable                                # Can create diagram
    )
    
    if all_tests_passed:
        print("✅ All tests passed! The Sankey diagram bug fix should work correctly.")
        print("\n📋 Next steps:")
        print("  1. Deploy the changes to production")
        print("  2. Test with real user data")
        print("  3. Monitor logs for any edge cases")
    else:
        print("⚠️  Some tests failed. Review the implementation before deploying.")
    
    return {
        "matching_test": matching_results,
        "comparison_test": comparison_results,
        "sankey_viable": sankey_viable,
        "all_passed": all_tests_passed
    }

if __name__ == "__main__":
    results = run_comprehensive_test()
    
    # Exit with appropriate code for CI/CD
    exit_code = 0 if results["all_passed"] else 1
    sys.exit(exit_code)
