import os
import telebot
import requests
import time
import re
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

# Telegram Bot Token - using environment variable or direct assignment
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7780725841:AAEkNzWjmG6jr2wDCS5w--YjupCQDSPmkm0")

# Coda API Details - using environment variables or direct assignment
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
                        {"column": LINK_COLUMN_ID, "value": link},
                        # You can add additional columns here if needed:
                        # {"column": "SOME_COLUMN_ID", "value": sender_info}
                    ]
                }
            ]
        }
        
        logger.info(f"Sending link to Coda: {link} from {sender_info}")
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        
        logger.info(f"Successfully saved link to Coda. Status code: {response.status_code}")
        return True, response.status_code
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error sending to Coda: {str(e)}"
        logger.error(error_msg)
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
    sender_id = message.from_user.id
    
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

def main():
    """Main function to start the bot"""
    logger.info("Starting DDF Reels Bot...")
    
    # Print a message with instructions
    print(f"DDF Reels Bot is running!")
    print(f"Bot username: @ddfreelsbot")
    print(f"Press Ctrl+C to stop the bot")
    
    # Start the bot polling for new messages
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            logger.error(f"Bot polling error: {str(e)}")
            time.sleep(10)  # Wait before retrying

if __name__ == "__main__":
    main() 