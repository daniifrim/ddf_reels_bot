import os
import json
import telebot
import requests
import re
import traceback
import sys
from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app for Vercel serverless function
app = Flask(__name__)

# Environment variable validation function
def get_required_env(name):
    """Get a required environment variable or exit with error"""
    value = os.getenv(name)
    if not value:
        error_msg = f"ERROR: Required environment variable '{name}' is not set"
        print(error_msg, file=sys.stderr)
        raise ValueError(error_msg)
    return value

# Configuration with validation
try:
    # Telegram Bot Token (required)
    BOT_TOKEN = get_required_env("TELEGRAM_BOT_TOKEN")
    print(f"Using Bot Token: {BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}")

    # Coda API Details (all required)
    CODA_API_KEY = get_required_env("CODA_API_KEY").strip()  # Strip whitespace
    print(f"Using Coda API Key: {CODA_API_KEY[:5]}...{CODA_API_KEY[-5:]}")
    
    DOC_ID = get_required_env("CODA_DOC_ID")
    print(f"Using Coda Doc ID: {DOC_ID}")
    
    TABLE_ID = get_required_env("CODA_TABLE_ID")
    print(f"Using Coda Table ID: {TABLE_ID}")
    
    LINK_COLUMN_ID = get_required_env("CODA_LINK_COLUMN_ID")
    print(f"Using Coda Link Column ID: {LINK_COLUMN_ID}")
except ValueError as e:
    # In production, this will cause the server to fail fast with a clear error
    print(f"Configuration error: {str(e)}")
    if __name__ != "__main__":  # Only exit if not in local development
        sys.exit(1)

# Define a regex pattern for any Instagram link (non-sensitive default is fine)
INSTAGRAM_PATTERN = r'https?://(?:www\.)?instagram\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?(?:\?[^\s]*)?'
print(f"Using Instagram pattern: {INSTAGRAM_PATTERN}")

# Initialize Telegram Bot
print("Initializing Telegram Bot")
bot = telebot.TeleBot(BOT_TOKEN)
print("Bot initialized successfully")

def send_to_coda(link):
    """
    Send the Instagram link to the Coda database.
    """
    # Use the exact same values from test_coda_direct.py that we know work
    api_key = "3e92f721-91d1-485e-aab9-b7d50e4fa4da"
    doc_id = "NYzN0H9At4" 
    table_id = "grid-Pyccn7MrAA"
    
    # Debug prints to troubleshoot
    print(f"Using hardcoded values from test_coda_direct.py")
    print(f"Doc ID: {doc_id}")
    print(f"Table ID: {table_id}")
    
    url = f"https://coda.io/apis/v1/docs/{doc_id}/tables/{table_id}/rows"
    auth_header = f"Bearer {api_key}"
    print(f"Auth header format: Bearer {api_key[:5]}...")
    
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
    
    # Use hardcoded "Link" to match the working test
    body = {
        "rows": [
            {
                "cells": [
                    {"column": "Link", "value": link}
                ]
            }
        ]
    }
    
    print(f"Request body: {body}")
    print(f"Request URL: {url}")
    print(f"Request headers: {headers}")
    
    try:
        response = requests.post(url, headers=headers, json=body)
        print(f"Response status: {response.status_code}")
        
        # Add detailed response debugging
        response_text = response.text[:500]  # Get first 500 chars to avoid huge logs
        print(f"Response first 500 chars: {response_text}")
        
        # Check if the response is HTML (login page) instead of JSON (API response)
        if "<!DOCTYPE html>" in response_text or "<html" in response_text:
            print("Error: Received HTML response instead of API response. Authentication failed.")
            return False
            
        if response.status_code == 202:
            print("Link successfully added to Coda")
            return True
        else:
            print(f"Failed to add link to Coda: {response.text}")
            return False
    except Exception as e:
        print(f"Exception when sending to Coda: {e}")
        return False

def extract_instagram_links(text):
    """Extract Instagram links from text using regex."""
    return re.findall(INSTAGRAM_PATTERN, text)

def send_telegram_message(chat_id, text):
    """Send a message to a Telegram chat."""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '').strip()
    
    if not bot_token:
        print("Error: No Telegram bot token found in environment variables")
        return False
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

# Process webhook calls - this is the endpoint Vercel will expose
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """
    Handle incoming webhook from Telegram.
    Extract Instagram links and save them to Coda.
    """
    print("Webhook endpoint called")
    
    # Parse the incoming JSON data
    try:
        data = request.json
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400
    
    # Extract message text from webhook data
    try:
        message = data.get('message', {})
        text = message.get('text', '')
        chat_id = message.get('chat', {}).get('id')
        
        if not chat_id:
            print("No chat_id found in webhook data")
            return jsonify({"status": "error", "message": "No chat_id found"}), 400
            
        print(f"Received message: {text}")
        
        # Extract Instagram links using regex
        instagram_links = extract_instagram_links(text)
        print(f"Extracted Instagram links: {instagram_links}")
        
        if not instagram_links:
            print("No Instagram links found in message")
            send_telegram_message(chat_id, "I don't recognize any Instagram links in your message. Please send a valid Instagram link.")
            return jsonify({"status": "success", "message": "No Instagram links found"}), 200
        
        # Process each link
        success_count = 0
        for link in instagram_links:
            success = send_to_coda(link)
            
            if success:
                success_count += 1
            
        # Send response back to user
        if success_count > 0:
            send_telegram_message(chat_id, "✅ Link saved successfully to the DDF database!")
        else:
            send_telegram_message(chat_id, "❌ Failed to save link to the database. Please try again later or contact support.")
        
        return jsonify({"status": "success", "message": f"Processed {len(instagram_links)} links, saved {success_count} successfully"}), 200
            
    except Exception as e:
        print(f"Error in webhook handler: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": f"Failed to process webhook: {str(e)}"}), 500

# The main entry point for Vercel
@app.route('/', methods=['GET'])
def index():
    """Root endpoint for health check"""
    return {"status": "ok", "message": "Bot is running"}

# This will be ignored by Vercel but can be used for local testing
if __name__ == "__main__":
    # Set webhook URL for your Vercel deployment (optional)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    if WEBHOOK_URL:
        # Set webhook
        webhook_url = f"{WEBHOOK_URL}/api/webhook"
        print(f"Would set webhook to: {webhook_url}")
        
        # Start Flask server for local testing
        app.run(host='0.0.0.0', port=8080)
    else:
        print("WEBHOOK_URL environment variable not set. Cannot start webhook server.") 