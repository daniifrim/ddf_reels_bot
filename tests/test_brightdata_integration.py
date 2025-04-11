#!/usr/bin/env python3

import os
import requests
import json
import time
from dotenv import load_dotenv
from pprint import pprint

def test_brightdata_api(reel_url):
    """Test the Bright Data API with a single Instagram Reel URL"""
    
    # Load API key from environment variables
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
        
    # API endpoint for Bright Data - using the trigger endpoint per documentation
    endpoint = "https://api.brightdata.com/datasets/v3/trigger"
    
    # Prepare headers and payload
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # According to the updated documentation, dataset_id goes in the JSON payload
    dataset_id = "gd_lyclm20il4r5helnj"  # Instagram Reels dataset ID
    
    # Build the payload according to the documentation
    payload = {
        "dataset_id": dataset_id,
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
            result = response.json()
            return result
        else:
            print(f"❌ Error response from Bright Data API: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error making request to Bright Data API: {str(e)}")
        return None

def get_scraping_results(snapshot_id):
    """Get the results of a scraping job using the snapshot ID"""
    
    # Load API key from environment variables
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
        
    # API endpoint to get results - CORRECTED from documentation
    # Note: it's "snapshot" (singular), not "snapshots"
    endpoint = f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"
    
    # Add query parameters for format and compression
    query_params = {
        "format": "json",
        "compress": "false"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    print(f"Fetching results for snapshot ID: {snapshot_id}")
    
    try:
        response = requests.get(endpoint, params=query_params, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body preview: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved results")
            result = response.json()
            return result
        else:
            print(f"❌ Error retrieving results: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error making request: {str(e)}")
        return None

def update_coda_with_results(reel_url, results):
    """Update the Coda database with the results from Bright Data"""
    
    # Load environment variables
    CODA_API_KEY = os.getenv("CODA_API_KEY")
    DOC_ID = os.getenv("CODA_DOC_ID")
    TABLE_ID = os.getenv("CODA_TABLE_ID")
    
    if not all([CODA_API_KEY, DOC_ID, TABLE_ID]):
        print("❌ Error: Missing Coda environment variables")
        return False
    
    # First, find the row with the matching URL
    search_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
    headers = {
        "Authorization": f"Bearer {CODA_API_KEY}"
    }
    
    try:
        # Get all rows to find the one with our URL
        response = requests.get(search_url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Error searching for row: {response.text}")
            return False
            
        rows = response.json().get("items", [])
        target_row_id = None
        
        for row in rows:
            cells = row.get("values", {})
            # Iterate through cells to find the one with our URL
            for col_id, value in cells.items():
                if value == reel_url:
                    target_row_id = row.get("id")
                    break
            
            if target_row_id:
                break
                
        if not target_row_id:
            print(f"❌ Error: Could not find row with URL: {reel_url}")
            return False
            
        # Now update the row with the scraped data
        # The structure of the results depends on which endpoint we used
        if not results:
            print("❌ Error: No results data to update")
            return False
            
        # Try to determine where the actual reel data is in the response
        # According to documentation, results should be in the "results" array
        if "results" in results:
            if not results["results"]:
                print("❌ Error: Empty results array")
                return False
            reel_data = results["results"][0]  # Get the first item from results
        elif "items" in results:
            if not results["items"]:
                print("❌ Error: Empty items array")
                return False
            reel_data = results["items"][0]  # Get the first item from results
        else:
            print("❌ Error: Unexpected results format, could not find reel data")
            print(f"Results keys: {results.keys()}")
            return False
        
        # Map Bright Data fields to Coda columns
        update_url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows/{target_row_id}"
        update_headers = {
            "Authorization": f"Bearer {CODA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Prepare update payload - mapping Bright Data fields to Coda columns
        # Field names might vary depending on the API response format
        update_payload = {
            "row": {
                "cells": [
                    {"column": "Account", "value": reel_data.get("username", reel_data.get("user_posted", ""))},
                    {"column": "Name", "value": reel_data.get("description", "")},
                    {"column": "Likes", "value": reel_data.get("likes", 0)},
                    {"column": "Comments", "value": reel_data.get("comments", reel_data.get("num_comments", 0))},
                    {"column": "Views", "value": reel_data.get("views", 0)}
                ]
            }
        }
        
        print(f"Updating Coda row with data: {json.dumps(update_payload, indent=2)}")
        
        update_response = requests.put(update_url, json=update_payload, headers=update_headers)
        
        if update_response.status_code == 200:
            print("✅ Successfully updated Coda row with scraped data")
            return True
        else:
            print(f"❌ Error updating row: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error interacting with Coda API: {str(e)}")
        return False

def add_url_to_coda(reel_url):
    """Add a new URL to the Coda database"""
    
    # Load environment variables
    CODA_API_KEY = os.getenv("CODA_API_KEY")
    DOC_ID = os.getenv("CODA_DOC_ID")
    TABLE_ID = os.getenv("CODA_TABLE_ID")
    
    if not all([CODA_API_KEY, DOC_ID, TABLE_ID]):
        print("❌ Error: Missing Coda environment variables")
        return False
    
    # Prepare the API request
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
    headers = {
        "Authorization": f"Bearer {CODA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the data to be sent to Coda
    body = {
        "rows": [
            {
                "cells": [
                    {"column": "Link", "value": reel_url}
                ]
            }
        ]
    }
    
    print(f"Adding URL to Coda: {reel_url}")
    
    try:
        response = requests.post(url, json=body, headers=headers)
        
        if response.status_code == 202:
            print("✅ Successfully added URL to Coda")
            return True
        else:
            print(f"❌ Error adding URL to Coda: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error making request to Coda API: {str(e)}")
        return False

def main():
    """Main function to run the full integration test"""
    # Load environment variables
    load_dotenv()
    
    # Test Instagram Reel URL
    TEST_REEL_URL = "https://www.instagram.com/share/reel/_kZE3ysBY"
    
    print("=== Starting Bright Data Integration Test ===")
    print(f"Testing with URL: {TEST_REEL_URL}")
    
    # Skip step 1 (adding to Coda) as we assume the URL is already in Coda
    
    # Step 2: Send URL to Bright Data API
    print("\n=== Step 2: Sending URL to Bright Data API ===")
    result = test_brightdata_api(TEST_REEL_URL)
    
    if not result:
        print("Failed to get response from Bright Data API. Exiting test.")
        return
    
    # In the updated API, we need to wait for the snapshot to complete
    snapshot_id = result.get("snapshot_id")
    
    if not snapshot_id:
        print("❌ Error: No snapshot_id in response. Exiting test.")
        return
    
    print(f"\n=== Step 3: Waiting for scraping to complete for snapshot {snapshot_id} ===")
    print("Note: In a production system, this would be handled by a webhook callback")
    
    # Wait for a moment to allow the scraping to begin
    wait_time = 10
    print(f"Waiting {wait_time} seconds before checking results...")
    time.sleep(wait_time)
    
    # Step 4: Get the results from Bright Data
    print("\n=== Step 4: Getting results from Bright Data ===")
    scraping_results = get_scraping_results(snapshot_id)
    
    if not scraping_results:
        print("Failed to get scraping results. Exiting test.")
        return
    
    print("\nScraping Results:")
    pprint(scraping_results)
    
    # Step 5: Update Coda with the scraped data
    print("\n=== Step 5: Updating Coda with scraped data ===")
    if update_coda_with_results(TEST_REEL_URL, scraping_results):
        print("\n✅ Full integration test completed successfully!")
    else:
        print("\n❌ Failed to update Coda with scraped data.")

if __name__ == "__main__":
    main() 