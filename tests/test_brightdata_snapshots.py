#!/usr/bin/env python3

import os
import requests
import json
import time
from dotenv import load_dotenv
from pprint import pprint

def get_snapshots_list():
    """Get a list of all snapshots from the Bright Data API"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
    
    # Endpoint for listing snapshots
    endpoint = "https://api.brightdata.com/datasets/v3/snapshots"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("Fetching list of snapshots...")
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved snapshots list")
            return response.json()
        else:
            print(f"Response body: {response.text}")
            print(f"❌ Failed to retrieve snapshots: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error retrieving snapshots list: {str(e)}")
        return None

def check_snapshot_data(snapshot_id):
    """Check specific snapshot data and availability"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try to get snapshot data directly
    print(f"Checking snapshot data for ID: {snapshot_id}")
    
    # Since the snapshots endpoint worked previously, let's try to query this endpoint
    # with the ?id parameter
    endpoint = f"https://api.brightdata.com/datasets/v3/snapshots?id={snapshot_id}"
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved snapshot data")
            return response.json()
        else:
            print(f"Response body: {response.text}")
            print(f"❌ Failed to retrieve snapshot data: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error retrieving snapshot data: {str(e)}")
    
    # Try to get snapshot data through the results endpoint
    print("\nTrying results endpoint...")
    endpoint = f"https://api.brightdata.com/datasets/v3/results?snapshot_id={snapshot_id}"
    
    try:
        response = requests.get(endpoint, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved results data")
            return response.json()
        else:
            print(f"Response body: {response.text}")
            print(f"❌ Failed to retrieve results data: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error retrieving results data: {str(e)}")
    
    return None

def extract_data_from_snapshot(snapshot):
    """Extract and display relevant data from a snapshot object"""
    
    print("\n=== Snapshot Details ===")
    print(f"Snapshot ID: {snapshot.get('id')}")
    print(f"Dataset ID: {snapshot.get('dataset_id')}")
    print(f"Status: {snapshot.get('status')}")
    print(f"Dataset Size: {snapshot.get('dataset_size')}")
    print(f"Created: {snapshot.get('created')}")
    
    # Extract additional data if available
    for key, value in snapshot.items():
        if key not in ['id', 'dataset_id', 'status', 'dataset_size', 'created']:
            print(f"{key}: {value}")

def main():
    """Main function to retrieve and process snapshots from Bright Data API"""
    print("=== Bright Data Snapshots Analysis ===")
    
    # Get the list of snapshots
    snapshots = get_snapshots_list()
    
    if not snapshots:
        print("❌ Failed to retrieve snapshots list")
        return
    
    print(f"\nFound {len(snapshots)} snapshots:")
    
    # Print a simplified summary of all snapshots
    for i, snapshot in enumerate(snapshots, 1):
        print(f"\n--- Snapshot {i} ---")
        extract_data_from_snapshot(snapshot)
    
    # Check specific snapshot details for our target
    print("\n=== Checking Specific Snapshot ===")
    
    # Use the snapshot ID from our previous successful response
    TARGET_SNAPSHOT_ID = "s_m8rgr9s92ejjxjf7o7"
    
    # Find our target snapshot in the list
    target_snapshot = None
    for snapshot in snapshots:
        if snapshot.get('id') == TARGET_SNAPSHOT_ID:
            target_snapshot = snapshot
            break
    
    if target_snapshot:
        print(f"Found target snapshot with ID: {TARGET_SNAPSHOT_ID}")
        extract_data_from_snapshot(target_snapshot)
        
        # Try to get additional data for this snapshot
        additional_data = check_snapshot_data(TARGET_SNAPSHOT_ID)
        
        if additional_data:
            print("\n=== Additional Snapshot Data ===")
            pprint(additional_data)
    else:
        print(f"❌ Target snapshot with ID {TARGET_SNAPSHOT_ID} not found in the list")

if __name__ == "__main__":
    main() 