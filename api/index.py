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
TABLE_ID = os.getenv("CODA_TABLE_ID", "tun7MrAA")
print(f"Using Coda Table ID: {TABLE_ID}")
LINK_COLUMN_ID = os.getenv("CODA_LINK_COLUMN_ID", "c-LFekrYG0se")
print(f"Using Coda Link Column ID: {LINK_COLUMN_ID}")

# Define a regex pattern for any Instagram link
INSTAGRAM_PATTERN = r'https://(?:www\.)?instagram\.com/[^\s"]+(?:\?[^\s"]*)?'

# Initialize Telegram Bot
print("Initializing Telegram Bot")
bot = telebot.TeleBot(BOT_TOKEN)
print("Bot initialized successfully")

def send_to_coda(link, sender_info):
    """
    Send Instagram link to Coda database
    
    Args:
        link: The Instagram link
        sender_info: Information about the sender (username or first name)
    
    Returns:
        Tuple of (success_boolean, status_code_or_error_message)
    """
    try:
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
        
        print(f"Sending link to Coda: {link} from {sender_info}")
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        print(f"Successfully saved link to Coda. Status code: {response.status_code}")
        return True, response.status_code
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error sending to Coda: {str(e)}"
        print(error_msg)
        return False, error_msg

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle /start and /help commands"""
    welcome_text = (
        "👋 Welcome to DDF Reels Bot!\n\n"
        "I collect Instagram links and save them to the DDF database.\n\n"
        "Just send me any Instagram link, and I'll take care of the rest."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all incoming messages and check for Instagram links"""
    print("*** handle_message function was called ***")
    # Extract the message text and sender information
    text = message.text.strip()
    sender = message.from_user.username or message.from_user.first_name or "Unknown"
    print(f"Received message: {text} from {sender}")
    
    # Use regex to find all Instagram links in the message
    try:
        print(f"About to process text with regex: {text}")
        instagram_links = re.findall(INSTAGRAM_PATTERN, text)
        print(f"Found links: {instagram_links}")
        
        if instagram_links:
            print(f"Processing {len(instagram_links)} links")
            for link in instagram_links:
                try:
                    print(f"Sending link to Coda: {link}")
                    success, result = send_to_coda(link, sender)
                    print(f"Coda result: {success}, {result}")
                    
                    if success:
                        print(f"Sending success message to user")
                        bot.reply_to(
                            message, 
                            f"✅ Link saved successfully to the DDF database!"
                        )
                    else:
                        print(f"Sending failure message to user")
                        bot.reply_to(
                            message,
                            f"❌ Failed to save link. Error: {result}. Please try again later."
                        )
                except Exception as e:
                    print(f"Error processing link {link}: {str(e)}")
        else:
            print(f"No links found, sending message to user")
            bot.reply_to(
                message,
                "❓ I didn't recognize any Instagram links in your message.\n\n"
                "Please send a valid Instagram link that starts with https://instagram.com/ or https://www.instagram.com/"
            )
    except Exception as e:
        print(f"ERROR in handle_message: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

# Process webhook calls - this is the endpoint Vercel will expose
@app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle webhook calls from Telegram"""
    print("Webhook endpoint called")
    if request.method == 'POST':
        try:
            # Get the request data
            print(f"Request headers: {request.headers}")
            if not request.is_json:
                print("Error: Request is not JSON")
                return '', 400

            # Get the raw data
            raw_data = request.get_data()
            print(f"Raw request data: {raw_data}")
            
            # Get the update from Telegram
            update = telebot.types.Update.de_json(request.get_json(force=True))
            
            if not update:
                print("Error: Could not parse Telegram update")
                return '', 400
                
            print(f"Received update: {update}")
            
            # Process the update with better error handling
            print("About to process update with bot.process_new_updates")
            try:
                bot.process_new_updates([update])
                print("Finished processing update")
            except Exception as e:
                print(f"ERROR in process_new_updates: {str(e)}")
                print(f"Traceback for process_new_updates error: {traceback.format_exc()}")
                
                # Attempt to handle the message directly as a fallback
                print("Trying to handle message directly")
                try:
                    if hasattr(update, 'message') and update.message:
                        handle_message(update.message)
                        print("Handled message directly")
                except Exception as direct_e:
                    print(f"ERROR in direct handle_message: {str(direct_e)}")
                    print(f"Traceback for direct handle: {traceback.format_exc()}")
            
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
        # Remove any existing webhook
        bot.remove_webhook()
        
        # Set webhook
        bot.set_webhook(url=f"{WEBHOOK_URL}/api/webhook")
        print(f"Webhook set to {WEBHOOK_URL}/api/webhook")
        
        # Start Flask server for local testing
        app.run(host='0.0.0.0', port=8080)
    else:
        print("WEBHOOK_URL environment variable not set. Cannot start webhook server.") 