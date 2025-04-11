#!/usr/bin/env python3

import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

def test_brightdata_direct(reel_url):
    """Test Bright Data API using the exact URL structure from the citation"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
    
    # Using the exact dataset_id from the citation URL
    dataset_id = "gd_lyclm20il4r5helnj"
    pdp_id = "hl_f96c6424"  # This was in the citation URL
    
    # Try multiple endpoint structures
    endpoints = [
        # From the citation URL structure, this seems to be a PDP-type endpoint
        f"https://api.brightdata.com/datasets/v3/trigger?dataset_id={dataset_id}&id={pdp_id}",
        # General trigger with direct ID reference
        f"https://api.brightdata.com/datasets/v3/trigger/gd_lyclm20il4r5helnj/pdp",
        # Standard approach in payload
        "https://api.brightdata.com/datasets/v3/trigger"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"Testing Bright Data API with direct URL structure for: {reel_url}")
    print(f"Dataset ID: {dataset_id}")
    print(f"PDP ID: {pdp_id}")
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"\n=== Testing Endpoint {i}: {endpoint} ===")
        
        # Prepare payload - adjust based on endpoint
        if "?" in endpoint:
            # If endpoint already has query parameters, send URL only
            payload = [{"url": reel_url}]
        else:
            # Standard payload with dataset_id
            payload = {
                "dataset_id": dataset_id,
                "inputs": [{"url": reel_url}]
            }
        
        print(f"Using payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successfully sent request to Bright Data API")
                return response.json()
        except Exception as e:
            print(f"❌ Error with endpoint {endpoint}: {str(e)}")
    
    # If none of the above worked, try the PDP API directly
    print("\n=== Testing PDP Direct API ===")
    pdp_endpoint = "https://api.brightdata.com/datasets/v3/pdp"
    pdp_payload = {
        "url": reel_url
    }
    
    try:
        response = requests.post(pdp_endpoint, json=pdp_payload, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Successfully sent request to Bright Data PDP API")
            return response.json()
    except Exception as e:
        print(f"❌ Error with PDP endpoint: {str(e)}")
    
    return None

def main():
    """Main function to test direct Bright Data API connection"""
    print("=== Testing Direct Bright Data API Connection ===")
    
    # Test Instagram Reel URL
    TEST_REEL_URL = "https://www.instagram.com/reel/C02GCxFoJnK/"
    
    print(f"Testing with URL: {TEST_REEL_URL}")
    
    # Try the direct API connection
    result = test_brightdata_direct(TEST_REEL_URL)
    
    if result:
        print("\n=== Results from Bright Data API ===")
        pprint(result)
    else:
        print("\n❌ Failed to get results from any Bright Data API endpoint")
        
        # Suggest next steps
        print("\n=== Suggested Next Steps ===")
        print("1. Contact Bright Data support to verify your account's access to the Instagram Reels scraper")
        print("2. Check if the dataset ID gd_lyclm20il4r5helnj is correctly associated with your account")
        print("3. Confirm if you need to purchase a specific subscription for the Instagram Reels scraper")
        print("4. Request the exact API endpoint and parameters for your account configuration")

if __name__ == "__main__":
    main() 