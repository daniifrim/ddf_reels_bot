#!/usr/bin/env python3

import os
import requests
import json
import time
from dotenv import load_dotenv
from pprint import pprint

def retrieve_snapshot(snapshot_id):
    """Retrieve a snapshot from Bright Data API using its ID"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
    
    # Endpoint for retrieving snapshots
    endpoint = f"https://api.brightdata.com/datasets/v3/snapshots/{snapshot_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"Retrieving snapshot with ID: {snapshot_id}")
    
    # Try to retrieve the snapshot with retries
    max_retries = 10
    retry_delay = 3  # seconds
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\nAttempt {attempt}/{max_retries} to retrieve snapshot")
            response = requests.get(endpoint, headers=headers)
            
            print(f"Response status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                print(f"Snapshot status: {status}")
                
                # If the snapshot is ready, return the data
                if status == "success":
                    print("✅ Successfully retrieved snapshot data")
                    return data
                
                # If the snapshot is still processing, wait and retry
                elif status in ["pending", "processing", "in_progress"]:
                    print(f"Snapshot is still {status}, waiting before retry...")
                    time.sleep(retry_delay)
                    continue
                
                # If the snapshot failed, return the error
                else:
                    print(f"❌ Snapshot processing failed with status: {status}")
                    return data
            
            else:
                print(f"Response body: {response.text}")
                
                # If we're getting a 404 or other error, it might not be ready yet
                if response.status_code == 404:
                    print(f"Snapshot not found, might still be processing. Waiting before retry...")
                    time.sleep(retry_delay)
                    continue
                
                print(f"❌ Failed to retrieve snapshot: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving snapshot: {str(e)}")
            time.sleep(retry_delay)
    
    print("❌ Max retries reached. Could not retrieve the snapshot.")
    return None

def main():
    """Main function to retrieve a snapshot from Bright Data API"""
    print("=== Retrieving Bright Data API Snapshot ===")
    
    # Use the snapshot ID from our previous successful response
    # You can replace this with any snapshot ID you want to retrieve
    SNAPSHOT_ID = "s_m8rgr9s92ejjxjf7o7"
    
    print(f"Attempting to retrieve snapshot ID: {SNAPSHOT_ID}")
    
    # Retrieve the snapshot
    result = retrieve_snapshot(SNAPSHOT_ID)
    
    if result:
        print("\n=== Snapshot Data ===")
        pprint(result)
        
        # If there's output data, show a sample
        output_data = result.get("output")
        if output_data:
            print("\n=== Sample Output Data ===")
            if isinstance(output_data, list) and len(output_data) > 0:
                pprint(output_data[0])
            else:
                pprint(output_data)
    else:
        print("\n❌ Failed to retrieve snapshot data")

if __name__ == "__main__":
    main() 