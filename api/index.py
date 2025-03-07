import os
import json
import telebot
import requests
import re
from flask import Flask, request, Response
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app for Vercel serverless function
app = Flask(__name__)

# Telegram Bot Token 
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7780725841:AAEkNzWjmG6jr2wDCS5w--YjupCQDSPmkm0")

# Coda API Details
CODA_API_KEY = os.getenv("CODA_API_KEY", "3e92f721-91d1-485e-aab9-b7d50e4fa4da")
DOC_ID = os.getenv("CODA_DOC_ID", "NYzN0H9At4")
TABLE_ID = os.getenv("CODA_TABLE_ID", "grid-Pyccn7MrAA")

# Define a regex pattern for any Instagram link
INSTAGRAM_PATTERN = r'https://(?:www\.)?instagram\.com/[^\s"]+(?:\?[^\s"]*)?'

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

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
        
        # Prepare the data to be sent to Coda using column name
        body = {
            "rows": [
                {
                    "cells": [
                        {"column": "Link", "value": link}
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
    # Extract the message text and sender information
    text = message.text.strip()
    sender = message.from_user.username or message.from_user.first_name or "Unknown"
    print(f"Received message: {text} from {sender}")
    
    # Use regex to find all Instagram links in the message
    instagram_links = re.findall(INSTAGRAM_PATTERN, text)
    print(f"Found links: {instagram_links}")
    
    if instagram_links:
        for link in instagram_links:
            success, result = send_to_coda(link, sender)
            
            if success:
                bot.reply_to(
                    message, 
                    f"✅ Link saved successfully to the DDF database!"
                )
            else:
                bot.reply_to(
                    message,
                    f"❌ Failed to save link. Error: {result}. Please try again later."
                )
    else:
        bot.reply_to(
            message,
            "❓ I didn't recognize any Instagram links in your message.\n\n"
            "Please send a valid Instagram link that starts with https://instagram.com/ or https://www.instagram.com/"
        )

# Process webhook calls - this is the endpoint Vercel will expose
@app.route('/api/webhook', methods=['POST'])
def webhook():
    # Always return 200 OK for Telegram's webhook verification
    if request.method == 'POST':
        try:
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return '', 200
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            # Still return 200 to avoid Telegram's retry mechanism
            return '', 200
    return '', 200

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
        bot.set_webhook(url=WEBHOOK_URL)
        print(f"Webhook set to {WEBHOOK_URL}")
        
        # Start Flask server for local testing
        app.run(host='0.0.0.0', port=8080)
    else:
        print("WEBHOOK_URL environment variable not set. Cannot start webhook server.") 