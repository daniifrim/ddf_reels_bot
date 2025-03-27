#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

def main():
    """Test adding a link directly to the Coda database"""
    # Load environment variables
    load_dotenv()
    
    # Coda API Details
    CODA_API_KEY = os.getenv("CODA_API_KEY", "3e92f721-91d1-485e-aab9-b7d50e4fa4da")
    DOC_ID = os.getenv("CODA_DOC_ID", "NYzN0H9At4")
    TABLE_ID = os.getenv("CODA_TABLE_ID", "grid-Pyccn7MrAA")
    LINK_COLUMN_ID = os.getenv("CODA_LINK_COLUMN_ID", "c-LFekrYG0se")
    
    # Test link to add
    TEST_LINK = "https://www.instagram.com/p/DG0RCJAKupnGahHLNM-RsH1HyJM8AntYgIkLxU0/?hl=en"
    
    print(f"Testing Coda connection with the following parameters:")
    print(f"Document ID: {DOC_ID}")
    print(f"Table ID: {TABLE_ID}")
    print(f"Link Column ID: {LINK_COLUMN_ID}")
    print(f"Test Link: {TEST_LINK}")
    
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
                    {"column": LINK_COLUMN_ID, "value": TEST_LINK}
                ]
            }
        ]
    }
    
    print("\nSending request to Coda API...")
    try:
        response = requests.post(url, json=body, headers=headers)
        
        # Print the response details
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 202:
            print("\n✅ Success! The link was successfully added to the Coda database.")
            print("Check your Coda document to verify the link was added.")
        else:
            print("\n❌ Failed to add the link to the Coda database.")
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 