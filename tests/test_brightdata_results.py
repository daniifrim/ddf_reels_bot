#!/usr/bin/env python3

import os
import requests
import json
import time
from dotenv import load_dotenv
from pprint import pprint

def check_snapshot_status(snapshot_id):
    """Check the status of a snapshot using different endpoint approaches"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
    
    dataset_id = "gd_lyclm20il4r5helnj"
    pdp_id = "hl_f96c6424"
    
    # Try multiple endpoints for status checking
    endpoints = [
        f"https://api.brightdata.com/datasets/v3/jobs/{snapshot_id}",
        f"https://api.brightdata.com/datasets/v3/results/{snapshot_id}",
        f"https://api.brightdata.com/datasets/v3/results?id={snapshot_id}",
        f"https://api.brightdata.com/datasets/v3/snapshots/{snapshot_id}",
        f"https://api.brightdata.com/datasets/v3/trigger/jobs/{snapshot_id}",
        f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/snapshots/{snapshot_id}",
        f"https://api.brightdata.com/datasets/v3/pdp/snapshots/{snapshot_id}"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    successful_responses = []
    
    print(f"Checking status for snapshot ID: {snapshot_id}")
    
    for i, endpoint in enumerate(endpoints, 1):
        try:
            print(f"\n=== Testing Endpoint {i}: {endpoint} ===")
            response = requests.get(endpoint, headers=headers)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response body: {response.text[:200]}..." if len(response.text) > 200 else f"Response body: {response.text}")
            
            if response.status_code == 200:
                print("✅ Successful response!")
                successful_responses.append({
                    "endpoint": endpoint,
                    "response": response.json() if response.text else {}
                })
            
        except Exception as e:
            print(f"❌ Error with endpoint {endpoint}: {str(e)}")
    
    return successful_responses

def try_alternative_approaches(snapshot_id):
    """Try alternative approaches to get data from the Bright Data API"""
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("BRIGHT_DATA_API_KEY")
    
    if not api_key:
        print("❌ Error: BRIGHT_DATA_API_KEY not found in environment variables")
        return None
    
    dataset_id = "gd_lyclm20il4r5helnj"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 1. Try to check dataset information
    print("\n=== Checking Dataset Information ===")
    dataset_endpoint = f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}"
    
    try:
        response = requests.get(dataset_endpoint, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text[:200]}..." if len(response.text) > 200 else f"Response body: {response.text}")
    except Exception as e:
        print(f"❌ Error checking dataset: {str(e)}")
    
    # 2. Try to list all snapshots
    print("\n=== Listing All Snapshots ===")
    snapshots_endpoint = "https://api.brightdata.com/datasets/v3/snapshots"
    
    try:
        response = requests.get(snapshots_endpoint, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text[:200]}..." if len(response.text) > 200 else f"Response body: {response.text}")
    except Exception as e:
        print(f"❌ Error listing snapshots: {str(e)}")
    
    # 3. Try to check job status with a POST request
    print("\n=== Checking Job Status with POST ===")
    job_endpoint = "https://api.brightdata.com/datasets/v3/jobs/status"
    
    try:
        job_payload = {
            "job_id": snapshot_id
        }
        response = requests.post(job_endpoint, json=job_payload, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text[:200]}..." if len(response.text) > 200 else f"Response body: {response.text}")
    except Exception as e:
        print(f"❌ Error checking job status: {str(e)}")
    
    # 4. Try to query the dataset directly
    print("\n=== Directly Querying Dataset ===")
    query_endpoint = f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/query"
    
    try:
        query_payload = {
            "query": {},
            "limit": 1
        }
        response = requests.post(query_endpoint, json=query_payload, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text[:200]}..." if len(response.text) > 200 else f"Response body: {response.text}")
    except Exception as e:
        print(f"❌ Error querying dataset: {str(e)}")
    
    # 5. Try to get dataset schema
    print("\n=== Getting Dataset Schema ===")
    schema_endpoint = f"https://api.brightdata.com/datasets/v3/datasets/{dataset_id}/schema"
    
    try:
        response = requests.get(schema_endpoint, headers=headers)
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text[:200]}..." if len(response.text) > 200 else f"Response body: {response.text}")
    except Exception as e:
        print(f"❌ Error getting schema: {str(e)}")

def main():
    """Main function to try multiple approaches to retrieve data from Bright Data API"""
    print("=== Comprehensive Bright Data API Results Check ===")
    
    # Use the snapshot ID from our previous successful response
    SNAPSHOT_ID = "s_m8rgr9s92ejjxjf7o7"
    
    print(f"Testing with snapshot ID: {SNAPSHOT_ID}")
    
    # Check snapshot status with different endpoints
    successful_responses = check_snapshot_status(SNAPSHOT_ID)
    
    if successful_responses:
        print("\n=== Successful Responses Summary ===")
        for i, result in enumerate(successful_responses, 1):
            print(f"\nSuccessful Response {i}:")
            print(f"Endpoint: {result['endpoint']}")
            print("Data:")
            pprint(result['response'])
    else:
        print("\n❌ No successful responses from any endpoints")
        print("Trying alternative approaches...")
        try_alternative_approaches(SNAPSHOT_ID)
        
        print("\n=== Suggested Next Steps ===")
        print("1. Contact Bright Data support to get the correct API endpoints for your account")
        print("2. Request the exact API documentation for the Instagram Reels scraper")
        print("3. Check if there's a Bright Data web interface to view results")
        print("4. Verify if there's a different dataset ID you should be using")

if __name__ == "__main__":
    main() 