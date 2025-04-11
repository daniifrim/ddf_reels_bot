#!/usr/bin/env python3

import os
import requests
import json
from dotenv import load_dotenv

def main():
    """A simplified test of the Bright Data Instagram scraper with minimal parameters"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return
    
    # Try different URLs - the link format might be the issue
    test_urls = [
        # Standard Instagram reel URL format
        "https://www.instagram.com/reel/C02GCxFoJnK/",
        
        # Alternative formats
        "https://www.instagram.com/p/C02GCxFoJnK/",
        "https://www.instagram.com/share/reel/_kZE3ysBY"
    ]
    
    # Try both API endpoints
    endpoints = [
        "https://api.brightdata.com/datasets/v3/trigger",
        "https://api.brightdata.com/datasets/v3/scrape"
    ]
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("=== Testing Bright Data API with Simplified Parameters ===")
    
    # Try each combination
    for endpoint in endpoints:
        print(f"\n=== Testing endpoint: {endpoint} ===")
        
        for test_url in test_urls:
            print(f"\nTesting URL: {test_url}")
            
            # Try with dataset_id parameter (for /trigger endpoint)
            if "trigger" in endpoint:
                payload = {
                    "dataset_id": "gd_lyclm20il4r5helnj",
                    "inputs": [{"url": test_url}]
                }
                
                print("Using payload with dataset_id")
                print(json.dumps(payload, indent=2))
                
                try:
                    response = requests.post(endpoint, json=payload, headers=headers)
                    print(f"Response status code: {response.status_code}")
                    print(f"Response body: {response.text}")
                except Exception as e:
                    print(f"Error: {str(e)}")
            
            # Try with scraper parameter (for /scrape endpoint)
            if "scrape" in endpoint:
                payload = {
                    "scraper": "instagram_reels",
                    "inputs": [{"url": test_url}]
                }
                
                print("Using payload with scraper")
                print(json.dumps(payload, indent=2))
                
                try:
                    response = requests.post(endpoint, json=payload, headers=headers)
                    print(f"Response status code: {response.status_code}")
                    print(f"Response body: {response.text}")
                except Exception as e:
                    print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 