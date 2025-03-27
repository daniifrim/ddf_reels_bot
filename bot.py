import os
import telebot
import requests
import time
import re
import logging
from dotenv import load_dotenv
from monitoring import setup_logging, monitor, error_handler

# Configure logging using our enhanced logging setup
logger = setup_logging()

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

# Optional: List of authorized users (empty list means anyone can use the bot)
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",") if os.getenv("AUTHORIZED_USERS") else []

# Optional: Admin user IDs who can see statistics and manage the bot
ADMIN_USERS = [int(id) for id in os.getenv("ADMIN_USERS", "").split(",") if id.strip()] if os.getenv("ADMIN_USERS") else []

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)

@error_handler
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
        
        # Update monitoring stats
        monitor.record_successful_submission()
        
        return True, response.status_code
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Error sending to Coda: {str(e)}"
        logger.error(error_msg)
        
        # Update monitoring stats
        monitor.record_failed_submission()
        
        return False, error_msg

def is_authorized(user_id, username):
    """Check if the user is authorized to use the bot"""
    # If no authorized users specified, everyone is authorized
    if not AUTHORIZED_USERS:
        return True
    
    # Check if username is in the authorized list
    if username and username in AUTHORIZED_USERS:
        return True
    
    # User is not authorized
    return False

def is_admin(user_id):
    """Check if user is an admin"""
    return user_id in ADMIN_USERS

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle /start and /help commands"""
    # Update monitoring stats
    monitor.record_message()
    
    # Extract user details
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Check if user is authorized
    if not is_authorized(user_id, username):
        bot.reply_to(
            message,
            "⛔ You are not authorized to use this bot. Please contact the administrator."
        )
        return
    
    welcome_text = (
        "👋 Welcome to DDF Reels Bot!\n\n"
        "I collect Instagram Reel links and save them to the DDF Coda database.\n\n"
        "Just send me an Instagram Reel link, and I'll take care of the rest. "
        "The link should look like: https://www.instagram.com/reel/ABC123/\n\n"
        "Available commands:\n"
        "/help - Show this help message\n"
    )
    
    # Add admin commands if user is admin
    if is_admin(user_id):
        welcome_text += (
            "/stats - View bot statistics\n"
            "/version - Show bot version info\n"
        )
    
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    """Send bot statistics (admin only)"""
    # Update monitoring stats
    monitor.record_message()
    
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        bot.reply_to(
            message,
            "⛔ This command is only available to administrators."
        )
        return
    
    # Get stats from the monitor
    stats_report = monitor.get_status_report()
    bot.reply_to(message, stats_report)

@bot.message_handler(commands=['version'])
def send_version(message):
    """Send bot version information (admin only)"""
    # Update monitoring stats
    monitor.record_message()
    
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        bot.reply_to(
            message,
            "⛔ This command is only available to administrators."
        )
        return
    
    version_info = (
        "🤖 DDF Reels Bot v1.1.0\n\n"
        "💻 Environment: " + os.getenv("ENVIRONMENT", "production") + "\n"
        "📝 Last updated: March 16, 2024\n"
        "🔧 Features:\n"
        "  - Instagram Reel link collection\n"
        "  - Coda database integration\n"
        "  - Bot statistics\n"
        "  - User authorization\n"
        "  - Error monitoring\n\n"
        "📊 Running since: " + monitor.start_time.strftime("%Y-%m-%d %H:%M:%S")
    )
    
    bot.reply_to(message, version_info)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all incoming messages and check for Instagram Reel links"""
    # Update monitoring stats
    monitor.record_message()
    
    # Extract the message text and sender information
    text = message.text.strip()
    sender = message.from_user.username or message.from_user.first_name or "Unknown"
    sender_id = message.from_user.id
    
    # Check if user is authorized
    if not is_authorized(sender_id, sender):
        bot.reply_to(
            message,
            "⛔ You are not authorized to use this bot. Please contact the administrator."
        )
        return
    
    # Use regex to find all Instagram reel links in the message
    reel_links = re.findall(INSTAGRAM_REEL_PATTERN, text)
    
    if reel_links:
        # Update monitoring stats
        monitor.record_valid_link()
        
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
        # Update monitoring stats
        monitor.record_invalid_link()
        
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
    
    # Log environment info
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'production')}")
    logger.info(f"Authorized users: {len(AUTHORIZED_USERS)}")
    logger.info(f"Admin users: {len(ADMIN_USERS)}")
    
    # Start the bot polling for new messages
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            # Log the error and update monitoring stats
            logger.error(f"Bot polling error: {str(e)}")
            monitor.record_error(e, "Polling Error")
            
            # Wait before retrying
            time.sleep(10)

if __name__ == "__main__":
    main() 