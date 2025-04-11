#!/usr/bin/env python3

import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint

def list_available_datasets():
    """List all available datasets/collectors in the Bright Data account"""
    
    # Load API key from environment variables
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return
    
    # Endpoint to list datasets (based on common API patterns)
    endpoint = "https://api.brightdata.com/datasets/v3/datasets"
    
    # Headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    print("Fetching available datasets from Bright Data...")
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved datasets")
            datasets = response.json()
            print(f"Found {len(datasets)} datasets:")
            pprint(datasets)
        else:
            print(f"❌ Error retrieving datasets: {response.text}")
            
            # Let's try some alternative endpoints
            alternative_endpoints = [
                "https://api.brightdata.com/datasets/v3/collectors",
                "https://api.brightdata.com/datasets/v3/list",
                "https://api.brightdata.com/datasets/v3/scrapers"
            ]
            
            print("\nTrying alternative endpoints...")
            
            for alt_endpoint in alternative_endpoints:
                print(f"\nTrying: {alt_endpoint}")
                try:
                    alt_response = requests.get(alt_endpoint, headers=headers)
                    print(f"Response status code: {alt_response.status_code}")
                    print(f"Response body: {alt_response.text[:500]}...")
                except Exception as e:
                    print(f"Error with endpoint {alt_endpoint}: {str(e)}")
    
    except Exception as e:
        print(f"❌ Error making request: {str(e)}")
        return

def test_instagram_endpoints():
    """Test various Instagram-related endpoints that might be available"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return
    
    # Common Instagram-related dataset IDs to try
    dataset_ids = [
        "gd_lyclm20il4r5helnj",  # The one we've been using
        "gd_instagram_reels",
        "gd_instagram",
        "instagram_reels",
        "instagram"
    ]
    
    # Headers with API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_url = "https://www.instagram.com/share/reel/_kZE3ysBY"
    
    print("\nTesting various Instagram dataset IDs...")
    
    for dataset_id in dataset_ids:
        print(f"\nTesting dataset ID: {dataset_id}")
        
        # Build payload
        payload = {
            "dataset_id": dataset_id,
            "inputs": [{"url": test_url}]
        }
        
        try:
            response = requests.post(
                "https://api.brightdata.com/datasets/v3/trigger", 
                json=payload, 
                headers=headers
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text}")
        except Exception as e:
            print(f"Error testing dataset ID {dataset_id}: {str(e)}")

def main():
    """Main function"""
    print("=== Bright Data API Information Tool ===")
    print("This tool will help identify available datasets/collectors\n")
    
    # List available datasets
    list_available_datasets()
    
    # Test Instagram-related endpoints
    test_instagram_endpoints()

if __name__ == "__main__":
    main() 