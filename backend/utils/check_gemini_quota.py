#!/usr/bin/env python3
"""
Check Gemini API quota and limits information
"""
import os
import sys
import google.generativeai as genai
from utils.config_utils import get_settings
from datetime import datetime

settings = get_settings()

# Configure API
genai.configure(api_key=settings.GOOGLE_API_KEY)


def check_quota():
    """Check current quota by making a test request"""
    print("\n=== Gemini API Quota Check ===\n")
    print(f"Current Time: {datetime.now()}")
    print(f"Model: {settings.GEMINI_MODEL}")
    print()
    
    try:
        # List available models to check API access
        print("Available Models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
        print()
        
        # Make a minimal test request
        print("Making test request...")
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content("Say 'test'")
        
        print("✅ API is accessible and working!")
        print(f"Response: {response.text.strip()}")
        print()
        
        print("Rate Limit Information:")
        print("  Based on https://ai.google.dev/gemini-api/docs/rate-limits")
        print()
        print("  Free Tier Limits:")
        print("    - 2 RPM (requests per minute)")
        print("    - 1,000 requests per day")
        print("    - 1.5M tokens per minute")
        print()
        print("  Pay-as-you-go Limits:")
        print("    - 15 RPM for Gemini Flash models")
        print("    - 2 RPM for Gemini Pro models")
        print("    - 1,000 - 4,000 RPM with increased quota")
        print()
        
        print(f"Your Current Settings:")
        print(f"  - GEMINI_REQUESTS_PER_MINUTE: {settings.GEMINI_REQUESTS_PER_MINUTE}")
        print()
        
        if settings.GEMINI_REQUESTS_PER_MINUTE <= 2:
            print("⚠️  You appear to be on the Free Tier")
            print("   To increase limits:")
            print("   1. Go to https://console.cloud.google.com/billing")
            print("   2. Enable billing for your project")
            print("   3. Your limits will automatically increase")
        elif settings.GEMINI_REQUESTS_PER_MINUTE <= 15:
            print("💳 You appear to be on Pay-as-you-go tier")
            print("   To increase limits further:")
            print("   1. Go to https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas")
            print("   2. Click 'EDIT QUOTAS'")
            print("   3. Request a higher limit")
        
    except Exception as e:
        print(f"❌ Error checking quota: {e}")
        
        error_str = str(e)
        if "quota" in error_str.lower() or "429" in error_str.lower():
            print("\n⚠️  Rate limit detected!")
            print(f"Error details: {error_str}")
            
            # Check log file for more info
            if os.path.exists("gemini_rate_limits.log"):
                print("\nChecking rate limit logs...")
                try:
                    with open("gemini_rate_limits.log", "r") as f:
                        lines = f.readlines()
                        if lines:
                            import json
                            last_limit = json.loads(lines[-1])
                            print(f"Last rate limit: {last_limit['timestamp']}")
                            print(f"Limit type: {last_limit['limit_type']}")
                except:
                    pass


if __name__ == "__main__":
    check_quota()