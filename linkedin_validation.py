#!/usr/bin/env python3
"""
LinkedIn Job Search Validation Script

This script validates the LinkedIn job search automation by performing test searches
and checking the results against specified criteria.
"""

import sys
import json
import time
from datetime import datetime
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# Configuration
CONFIG = {
    "test_positions": [
        "Head of Growth",
        "VP of Business Development"
    ],
    "test_industries": [
        "SaaS",
        "Digital Platforms"
    ],
    "locations": [
        "Porto",
        "Lisbon",
        "Portugal",
        "Remote",
        "Europe"
    ],
    "exclude_locations": ["Russia", "Russian Federation"],
    "min_salary": 8200,  # EUR per month
    "preferred_formats": ["hybrid", "remote"],
    "validation_results_file": "linkedin_validation_results.json",
    "log_file": "linkedin_validation_log.txt"
}

def log_message(message):
    """Log a message with timestamp to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CONFIG["log_file"], "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def test_search_linkedin_jobs(keywords, start=0):
    """
    Test search for jobs on LinkedIn using the LinkedIn API.
    
    Args:
        keywords: Search keywords
        start: Starting position for pagination
        
    Returns:
        Search results from LinkedIn API
    """
    client = ApiClient()
    try:
        log_message(f"TEST: Searching LinkedIn with keywords: {keywords}, start: {start}")
        results = client.call_api('LinkedIn/search_people', query={
            'keywords': keywords,
            'start': str(start)
        })
        return results
    except Exception as e:
        log_message(f"TEST ERROR: Error searching LinkedIn: {str(e)}")
        return {"success": False, "message": str(e), "data": {"items": []}}

def test_get_profile_details(username):
    """
    Test getting detailed profile information for a LinkedIn user.
    
    Args:
        username: LinkedIn username
        
    Returns:
        Profile details from LinkedIn API
    """
    client = ApiClient()
    try:
        log_message(f"TEST: Getting profile details for: {username}")
        profile = client.call_api('LinkedIn/get_user_profile_by_username', query={
            'username': username
        })
        return profile
    except Exception as e:
        log_message(f"TEST ERROR: Error getting profile details: {str(e)}")
        return {"success": False, "message": str(e), "data": {}}

def validate_api_access():
    """
    Validate that the LinkedIn API is accessible.
    
    Returns:
        Boolean indicating if API is accessible
    """
    try:
        # Test with a sample search
        test_result = test_search_linkedin_jobs("VP Business Development")
        if test_result.get("success", False):
            log_message("API Access Validation: SUCCESS - LinkedIn API is accessible")
            return True
        else:
            log_message(f"API Access Validation: FAILED - {test_result.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        log_message(f"API Access Validation: FAILED - Exception: {str(e)}")
        return False

def validate_profile_retrieval():
    """
    Validate that profile details can be retrieved.
    
    Returns:
        Boolean indicating if profile retrieval works
    """
    try:
        # Test with a sample profile (using default from API docs)
        test_result = test_get_profile_details("adamselipsky")
        if test_result.get("success", False):
            log_message("Profile Retrieval Validation: SUCCESS - Profile details can be retrieved")
            return True
        else:
            log_message(f"Profile Retrieval Validation: FAILED - {test_result.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        log_message(f"Profile Retrieval Validation: FAILED - Exception: {str(e)}")
        return False

def validate_filtering_logic():
    """
    Validate the job filtering logic.
    
    Returns:
        Boolean indicating if filtering logic works correctly
    """
    # Test cases for filtering logic
    test_cases = [
        {
            "location": "Porto, Portugal",
            "expected_result": True,
            "reason": "Location is in allowed list"
        },
        {
            "location": "Moscow, Russian Federation",
            "expected_result": False,
            "reason": "Location is in excluded list"
        },
        {
            "location": "Remote, Europe",
            "expected_result": True,
            "reason": "Remote location is allowed"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases):
        # Create a mock job data object
        mock_job = {"location": test_case["location"]}
        
        # Test the filtering function
        from linkedin_search_automation import is_job_relevant
        result = is_job_relevant(mock_job)
        
        # Check if result matches expected
        if result == test_case["expected_result"]:
            log_message(f"Filtering Test {i+1}: PASSED - {test_case['reason']}")
        else:
            log_message(f"Filtering Test {i+1}: FAILED - Expected {test_case['expected_result']} but got {result} for {test_case['reason']}")
            all_passed = False
    
    return all_passed

def save_validation_results(results):
    """
    Save validation results to a JSON file.
    
    Args:
        results: Validation results to save
    """
    try:
        with open(CONFIG["validation_results_file"], "w") as f:
            json.dump(results, f, indent=2)
        log_message(f"Validation results saved to {CONFIG['validation_results_file']}")
    except Exception as e:
        log_message(f"Error saving validation results: {str(e)}")

def main():
    """Main validation function."""
    log_message("Starting LinkedIn job search validation")
    
    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Validate API access
    validation_results["tests"]["api_access"] = validate_api_access()
    
    # Validate profile retrieval
    validation_results["tests"]["profile_retrieval"] = validate_profile_retrieval()
    
    # Validate filtering logic
    try:
        validation_results["tests"]["filtering_logic"] = validate_filtering_logic()
    except Exception as e:
        log_message(f"Error validating filtering logic: {str(e)}")
        validation_results["tests"]["filtering_logic"] = False
    
    # Overall validation result
    validation_results["overall_success"] = all(validation_results["tests"].values())
    
    # Save validation results
    save_validation_results(validation_results)
    
    if validation_results["overall_success"]:
        log_message("Validation SUCCESSFUL - All tests passed")
    else:
        log_message("Validation FAILED - Some tests did not pass")
    
    return validation_results["overall_success"]

if __name__ == "__main__":
    main()
