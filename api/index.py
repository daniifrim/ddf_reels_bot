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
DOC_ID = os.getenv("CODA_DOC_ID", "dNYzN0H9At4")
TABLE_ID = os.getenv("CODA_TABLE_ID", "tun7MrAA")
LINK_COLUMN_ID = os.getenv("CODA_LINK_COLUMN_ID", "c-LFekrYG0se")

# Define a regex pattern for Instagram Reel links
INSTAGRAM_REEL_PATTERN = r'https://(?:www\.)?instagram\.com/(?:reel|p)/[\w-]+/?'

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

def send_to_coda(link, sender_info):
    """
    Send Instagram reel link to Coda database
    
    Args:
        link: The Instagram reel link
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
        
        # Prepare the data to be sent to Coda
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
        "I collect Instagram Reel links and save them to the DDF database.\n\n"
        "Just send me an Instagram Reel link, and I'll take care of the rest. "
        "The link should look like: https://www.instagram.com/reel/ABC123/"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all incoming messages and check for Instagram Reel links"""
    # Extract the message text and sender information
    text = message.text.strip()
    sender = message.from_user.username or message.from_user.first_name or "Unknown"
    
    # Use regex to find all Instagram reel links in the message
    reel_links = re.findall(INSTAGRAM_REEL_PATTERN, text)
    
    if reel_links:
        for link in reel_links:
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
            "❓ I didn't recognize any Instagram Reel links in your message.\n\n"
            "Please send a valid Instagram Reel link that looks like:\n"
            "https://www.instagram.com/reel/ABC123/"
        )

# Process webhook calls - this is the endpoint Vercel will expose
@app.route('/api/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return Response(status=403)

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