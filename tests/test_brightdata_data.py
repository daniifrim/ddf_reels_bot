#!/usr/bin/env python3

import os
import requests
import json
import time
from dotenv import load_dotenv
from pprint import pprint

def retrieve_data_for_snapshot(snapshot_id, dataset_id):
    """Attempt to retrieve the actual data for a snapshot"""
    
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
    
    # Try multiple endpoint patterns for data retrieval
    endpoints = [
        # Try dataset data endpoint
        f"https://api.brightdata.com/datasets/v3/data/{dataset_id}",
        # Try dataset records endpoint
        f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/records",
        # Try dataset elements endpoint
        f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/elements",
        # Try dataset entries endpoint
        f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/entries",
        # Try dataset results endpoint
        f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/results",
        # Try data endpoint with snapshot parameter
        f"https://api.brightdata.com/datasets/v3/data?snapshot_id={snapshot_id}",
        # Try direct result download
        f"https://api.brightdata.com/datasets/v3/download/{dataset_id}",
        # Try download with snapshot parameter
        f"https://api.brightdata.com/datasets/v3/download?snapshot_id={snapshot_id}",
        # Try dataset unload endpoint
        f"https://api.brightdata.com/datasets/v3/unload/{dataset_id}"
    ]
    
    print(f"Attempting to retrieve data for snapshot ID: {snapshot_id}")
    print(f"Dataset ID: {dataset_id}")
    
    successful_responses = []
    
    for i, endpoint in enumerate(endpoints, 1):
        try:
            print(f"\n=== Testing Endpoint {i}: {endpoint} ===")
            response = requests.get(endpoint, headers=headers)
            
            print(f"Response status code: {response.status_code}")
            
            # Only print a truncated version of potentially large responses
            if response.status_code == 200 and len(response.text) > 500:
                print(f"Response body (truncated): {response.text[:500]}...")
            else:
                print(f"Response body: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successful response!")
                try:
                    data = response.json() if response.text else {}
                    successful_responses.append({
                        "endpoint": endpoint,
                        "data": data
                    })
                except json.JSONDecodeError:
                    print("Response is not JSON. Might be raw data or a file.")
                    successful_responses.append({
                        "endpoint": endpoint,
                        "data": "Raw data (not JSON)"
                    })
            
        except Exception as e:
            print(f"❌ Error with endpoint {endpoint}: {str(e)}")
    
    # If no success with GET requests, try POST requests for some endpoints
    if not successful_responses:
        print("\n=== Trying POST requests ===")
        
        post_endpoints = [
            # Try to query the dataset
            f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/query",
            # Try to get data from the dataset
            f"https://api.brightdata.com/datasets/v3/data",
            # Try to export the dataset
            f"https://api.brightdata.com/datasets/v3/export"
        ]
        
        for i, endpoint in enumerate(post_endpoints, 1):
            try:
                print(f"\n=== Testing POST Endpoint {i}: {endpoint} ===")
                
                # Different payload for each endpoint
                if "query" in endpoint:
                    payload = {
                        "query": {},
                        "limit": 10
                    }
                elif "data" in endpoint:
                    payload = {
                        "dataset_id": dataset_id,
                        "snapshot_id": snapshot_id
                    }
                else:  # export
                    payload = {
                        "dataset_id": dataset_id,
                        "format": "json"
                    }
                
                print(f"Using payload: {json.dumps(payload)}")
                
                response = requests.post(endpoint, json=payload, headers=headers)
                
                print(f"Response status code: {response.status_code}")
                
                # Only print a truncated version of potentially large responses
                if response.status_code == 200 and len(response.text) > 500:
                    print(f"Response body (truncated): {response.text[:500]}...")
                else:
                    print(f"Response body: {response.text}")
                
                if response.status_code == 200:
                    print("✅ Successful response!")
                    try:
                        data = response.json() if response.text else {}
                        successful_responses.append({
                            "endpoint": endpoint,
                            "method": "POST",
                            "data": data
                        })
                    except json.JSONDecodeError:
                        print("Response is not JSON. Might be raw data or a file.")
                        successful_responses.append({
                            "endpoint": endpoint,
                            "method": "POST",
                            "data": "Raw data (not JSON)"
                        })
                
            except Exception as e:
                print(f"❌ Error with POST endpoint {endpoint}: {str(e)}")
    
    return successful_responses

def main():
    """Main function to retrieve data from a Bright Data snapshot"""
    print("=== Bright Data Data Retrieval ===")
    
    # Use the snapshot ID and dataset ID from our previous successful responses
    SNAPSHOT_ID = "s_m8rgr9s92ejjxjf7o7"
    DATASET_ID = "gd_lyclm20il4r5helnj"
    
    # Attempt to retrieve the data
    results = retrieve_data_for_snapshot(SNAPSHOT_ID, DATASET_ID)
    
    if results:
        print("\n=== Successful Data Retrieval Summary ===")
        for i, result in enumerate(results, 1):
            print(f"\n--- Successful Response {i} ---")
            print(f"Endpoint: {result['endpoint']}")
            if 'method' in result:
                print(f"Method: {result['method']}")
            
            # Handle different data types
            if isinstance(result['data'], str):
                print(f"Data: {result['data']}")
            else:
                print("Data:")
                pprint(result['data'])
    else:
        print("\n❌ Failed to retrieve data through any endpoint")
        print("\n=== Suggested Next Steps ===")
        print("1. Contact Bright Data support for specific API documentation for Instagram data retrieval")
        print("2. Check if there's a web interface where you can view and download the results")
        print("3. Verify if the subscription allows for API data retrieval")
        print("4. Consider using the Bright Data command-line tools if available")

if __name__ == "__main__":
    main() 