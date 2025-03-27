import os
import re
import requests
import sys
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Instagram link regex pattern (works for reels, posts, etc.)
INSTAGRAM_PATTERN = r'https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?(?:\?[^\s]*)?'

def get_required_env(name):
    """Get a required environment variable or exit with error"""
    value = os.getenv(name)
    if not value:
        error_msg = f"ERROR: Required environment variable '{name}' is not set"
        print(error_msg, file=sys.stderr)
        raise ValueError(error_msg)
    return value

def extract_instagram_links(text):
    """Extract Instagram links from text using regex."""
    return re.findall(INSTAGRAM_PATTERN, text)

def send_to_coda(link, coda_config=None):
    """
    Send Instagram link to Coda database
    
    Args:
        link: The Instagram link
        coda_config: Optional dictionary with Coda configuration. 
                    If None, will use environment variables.
    
    Returns:
        Tuple of (success_boolean, status_code_or_error_message)
    """
    try:
        # Use provided config or get from environment
        if coda_config is None:
            api_key = get_required_env("CODA_API_KEY").strip()
            doc_id = get_required_env("CODA_DOC_ID")
            table_id = get_required_env("CODA_TABLE_ID")
            column_name = "Link"  # Use the column name instead of ID for stability
        else:
            api_key = coda_config.get("api_key")
            doc_id = coda_config.get("doc_id")
            table_id = coda_config.get("table_id")
            column_name = coda_config.get("column_name", "Link")

        url = f"https://coda.io/apis/v1/docs/{doc_id}/tables/{table_id}/rows"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare the data to be sent to Coda
        body = {
            "rows": [
                {
                    "cells": [
                        {"column": column_name, "value": link}
                    ]
                }
            ]
        }
        
        print(f"Sending link to Coda: {link}")
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        print(f"Successfully saved link to Coda. Status code: {response.status_code}")
        return True, response.status_code
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error sending to Coda: {str(e)}"
        print(error_msg)
        return False, error_msg 