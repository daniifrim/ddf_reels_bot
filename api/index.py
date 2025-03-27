import os
import json
import telebot
import requests
import re
import traceback
from flask import Flask, request, Response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app for Vercel serverless function
app = Flask(__name__)

# Telegram Bot Token 
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7780725841:AAEkNzWjmG6jr2wDCS5w--YjupCQDSPmkm0")
print(f"Using Bot Token: {BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}")

# Coda API Details
CODA_API_KEY = os.getenv("CODA_API_KEY", "3e92f721-91d1-485e-aab9-b7d50e4fa4da")
print(f"Using Coda API Key: {CODA_API_KEY[:5]}...{CODA_API_KEY[-5:]}")
DOC_ID = os.getenv("CODA_DOC_ID", "dNYzN0H9At4")
print(f"Using Coda Doc ID: {DOC_ID}")
TABLE_ID = os.getenv("CODA_TABLE_ID", "grid-tun7MrAA")
print(f"Using Coda Table ID: {TABLE_ID}")
LINK_COLUMN_ID = os.getenv("CODA_LINK_COLUMN_ID", "c-LFekrYG0se")
print(f"Using Coda Link Column ID: {LINK_COLUMN_ID}")

# Define a regex pattern for any Instagram link
INSTAGRAM_PATTERN = r'https://(?:www\.)?instagram\.com/(?:[^/\s"]+/)*[^/\s"]+/?(?:\?[^\s"]*)?'
print(f"Using Instagram pattern: {INSTAGRAM_PATTERN}")

# Initialize Telegram Bot
print("Initializing Telegram Bot")
bot = telebot.TeleBot(BOT_TOKEN)
print("Bot initialized successfully")

def send_to_coda(link):
    """
    Send Instagram link to Coda database
    
    Args:
        link: The Instagram link
    
    Returns:
        Tuple of (success_boolean, status_code_or_error_message)
    """
    try:
        print(f"Sending link to Coda: {link}")
        url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"
        headers = {
            "Authorization": f"Bearer {CODA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Prepare the data to be sent to Coda using column ID
        body = {
            "rows": [
                {
                    "cells": [
                        {"column": LINK_COLUMN_ID, "value": link}
                    ]
                }
            ]
        }
        
        print(f"Request body: {json.dumps(body)}")
        response = requests.post(url, json=body, headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        print(f"Successfully saved link to Coda. Status code: {response.status_code}")
        return True, response.status_code
    
    except Exception as e:
        error_msg = f"Error sending to Coda: {str(e)}"
        print(error_msg)
        print(f"Traceback: {traceback.format_exc()}")
        return False, error_msg

# Process webhook calls - this is the endpoint Vercel will expose
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle webhook calls from Telegram"""
    print("Webhook endpoint called")
    
    if request.method == 'POST':
        try:
            print(f"Request headers: {request.headers}")
            data = request.get_json(force=True)
            print(f"Received data: {json.dumps(data)}")
            
            # Extract message from the update
            if 'message' in data and 'text' in data['message']:
                message_text = data['message']['text']
                print(f"Extracted message text: {message_text}")
                
                # Search for Instagram links
                links = re.findall(INSTAGRAM_PATTERN, message_text)
                print(f"Found Instagram links: {links}")
                
                if links:
                    # Save link to Coda
                    link = links[0]  # Take the first link
                    success, result = send_to_coda(link)
                    
                    # Send response back to user via Telegram API directly
                    chat_id = data['message']['chat']['id']
                    if success:
                        response_text = "✅ Link saved successfully to the DDF database!"
                    else:
                        response_text = f"❌ Failed to save link. Error: {result}. Please try again later."
                    
                    response_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    response_params = {
                        "chat_id": chat_id,
                        "text": response_text
                    }
                    
                    print(f"Sending response to Telegram: {json.dumps(response_params)}")
                    telegram_response = requests.post(response_url, json=response_params)
                    print(f"Telegram response: {telegram_response.status_code} - {telegram_response.text}")
                else:
                    # No Instagram links found
                    chat_id = data['message']['chat']['id']
                    response_text = "❓ I didn't recognize any Instagram links in your message.\n\nPlease send a valid Instagram link that starts with https://instagram.com/ or https://www.instagram.com/"
                    
                    response_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    response_params = {
                        "chat_id": chat_id,
                        "text": response_text
                    }
                    
                    print(f"Sending response to Telegram: {json.dumps(response_params)}")
                    telegram_response = requests.post(response_url, json=response_params)
                    print(f"Telegram response: {telegram_response.status_code} - {telegram_response.text}")
            
            return '', 200
            
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return '', 500
            
    return '', 403

# The main entry point for Vercel
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If POST request, process as webhook
        return webhook()
    else:
        # For GET requests, return a simple confirmation page
        return "DDF Reels Bot is running! This is the webhook endpoint for the Telegram bot."

# This will be ignored by Vercel but can be used for local testing
if __name__ == "__main__":
    # Set webhook URL for your Vercel deployment
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    if WEBHOOK_URL:
        # Set webhook
        webhook_url = f"{WEBHOOK_URL}/api/webhook"
        print(f"Would set webhook to: {webhook_url}")
        
        # Start Flask server for local testing
        app.run(host='0.0.0.0', port=8080)
    else:
        print("WEBHOOK_URL environment variable not set. Cannot start webhook server.") 