#!/usr/bin/env python3

import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

def test_brightdata_scraper_api(reel_url):
    """Test the Bright Data API using the /scrape endpoint with the instagram_reels scraper"""
    
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
        
    # API endpoint for Bright Data - using the scrape endpoint from original documentation
    endpoint = "https://api.brightdata.com/datasets/v3/scrape"
    
    # Prepare headers and payload
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Using the format from the original documentation
    payload = {
        "scraper": "instagram_reels",
        "inputs": [{"url": reel_url}]
    }
    
    print(f"Sending request to Bright Data API for URL: {reel_url}")
    print(f"Using payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Successfully sent request to Bright Data API")
            return response.json()
        else:
            print(f"❌ Error response from Bright Data API: {response.text}")
            
            # If we got a 404, let's try some variations of the scraper name
            if response.status_code == 404:
                print("\nTrying alternative scraper names...")
                scrapers = [
                    "instagram_reel",
                    "ig_reels",
                    "instagram",
                    "instagram_post"
                ]
                
                for scraper in scrapers:
                    print(f"\nTrying scraper: {scraper}")
                    alt_payload = {
                        "scraper": scraper,
                        "inputs": [{"url": reel_url}]
                    }
                    
                    try:
                        alt_response = requests.post(endpoint, json=alt_payload, headers=headers)
                        print(f"Response status code: {alt_response.status_code}")
                        print(f"Response body: {alt_response.text}")
                        
                        if alt_response.status_code == 200:
                            print(f"✅ Success with scraper: {scraper}")
                            return alt_response.json()
                    except Exception as e:
                        print(f"Error with scraper {scraper}: {str(e)}")
            
            return None
            
    except Exception as e:
        print(f"❌ Error making request to Bright Data API: {str(e)}")
        return None

def main():
    """Main function to test the Bright Data scraper API"""
    print("=== Testing Bright Data /scrape Endpoint ===")
    
    # Test Instagram Reel URL
    TEST_REEL_URL = "https://www.instagram.com/share/reel/_kZE3ysBY"
    
    print(f"Testing with URL: {TEST_REEL_URL}")
    
    # Try the API
    result = test_brightdata_scraper_api(TEST_REEL_URL)
    
    if result:
        print("\n=== Results from Bright Data API ===")
        pprint(result)
    else:
        print("\n❌ Failed to get results from Bright Data API")

if __name__ == "__main__":
    main() 