#!/usr/bin/env python3

import os
import requests
import json
from dotenv import load_dotenv

def test_connection(doc_id):
    """Test connection to a Coda document"""
    CODA_API_KEY = os.getenv("CODA_API_KEY", "3e92f721-91d1-485e-aab9-b7d50e4fa4da")
    
    print(f"Testing connection to Coda document {doc_id}...")
    
    # Test connection by getting the list of tables in the document
    url = f"https://coda.io/apis/v1/docs/{doc_id}/tables"
    headers = {
        "Authorization": f"Bearer {CODA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            tables = response.json()
            print(f"✅ Successfully connected to Coda document!")
            print(f"Document contains {len(tables.get('items', []))} tables:")
            
            for table in tables.get('items', []):
                print(f"  - Table: '{table.get('name')}' (ID: {table.get('id')})")
                
                # For each table, get the columns
                columns_url = f"https://coda.io/apis/v1/docs/{doc_id}/tables/{table.get('id')}/columns"
                columns_response = requests.get(columns_url, headers=headers)
                
                if columns_response.status_code == 200:
                    columns = columns_response.json()
                    print(f"    Columns: {len(columns.get('items', []))}")
                    for column in columns.get('items', []):
                        print(f"      * {column.get('name')} (ID: {column.get('id')})")
                else:
                    print(f"    ❌ Failed to get columns. Status code: {columns_response.status_code}")
            
            return True
        else:
            print(f"❌ Failed to connect to Coda API. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Coda API: {str(e)}")
        return False

def main():
    """Try different document ID formats"""
    # Load environment variables
    load_dotenv()
    
    # Try different formats of the document ID
    test_doc_ids = [
        "NYzN0H9At4",     # Original format from data.md
        "dNYzN0H9At4",    # Format with 'd' prefix
        "_dNYzN0H9At4"    # Format with '_d' prefix
    ]
    
    for doc_id in test_doc_ids:
        print("\n" + "="*50)
        success = test_connection(doc_id)
        if success:
            print(f"\nDocument ID {doc_id} is working! Update your .env file with this value.")
            break
    else:
        print("\nNone of the document ID formats worked. Please check your Coda API key and document ID.")

if __name__ == "__main__":
    main() 