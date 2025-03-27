import os
import telebot
import sys
import logging
from src.utils import get_required_env, extract_instagram_links, send_to_coda
from src.monitoring import setup_logging, monitor, error_handler

# Configure logging using our enhanced logging setup
logger = setup_logging()

# Configuration with validation
try:
    # Telegram Bot Token (required)
    BOT_TOKEN = get_required_env("TELEGRAM_BOT_TOKEN")
    logger.info(f"Using Bot Token: {BOT_TOKEN[:5]}...{BOT_TOKEN[-5:]}")

    # Coda API Details (all required)
    CODA_API_KEY = get_required_env("CODA_API_KEY")
    logger.info(f"Using Coda API Key: {CODA_API_KEY[:5]}...{CODA_API_KEY[-5:]}")
    
    DOC_ID = get_required_env("CODA_DOC_ID")
    logger.info(f"Using Coda Doc ID: {DOC_ID}")
    
    TABLE_ID = get_required_env("CODA_TABLE_ID")
    logger.info(f"Using Coda Table ID: {TABLE_ID}")
except ValueError as e:
    logger.critical(f"Configuration error: {str(e)}")
    sys.exit(1)

# Non-critical configuration with sensible defaults
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
logger.info(f"Environment: {ENVIRONMENT}")

# Optional: List of authorized users (empty list means anyone can use the bot)
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",") if os.getenv("AUTHORIZED_USERS") else []
logger.info(f"Authorized users: {len(AUTHORIZED_USERS)}")

# Optional: Admin user IDs who can see statistics and manage the bot
ADMIN_USERS = [int(id) for id in os.getenv("ADMIN_USERS", "").split(",") if id.strip()] if os.getenv("ADMIN_USERS") else []
logger.info(f"Admin users: {len(ADMIN_USERS)}")

# Initialize Telegram Bot
bot = telebot.TeleBot(BOT_TOKEN)
logger.info("Bot initialized successfully")

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

@error_handler
def process_instagram_link(link, sender_info):
    """Process an Instagram link and save it to Coda"""
    # Create coda config from environment variables
    coda_config = {
        "api_key": CODA_API_KEY,
        "doc_id": DOC_ID,
        "table_id": TABLE_ID,
        "column_name": "Link"  # Use column name for stability
    }
    
    # Send to Coda using the shared utility
    success, result = send_to_coda(link, coda_config)
    
    # Update monitoring stats
    if success:
        monitor.record_successful_submission()
    else:
        monitor.record_failed_submission()
    
    return success, result

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
    
    # Get version info
    version_info = (
        "🤖 DDF Reels Bot v1.0.0\n"
        "Environment: {}\n"
        "Built with ❤️ for DDF\n"
    ).format(ENVIRONMENT)
    
    bot.reply_to(message, version_info)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Handle all incoming messages and check for Instagram links"""
    # Update monitoring stats
    monitor.record_message()
    
    # Extract the message text and sender information
    text = message.text.strip()
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Check if user is authorized
    if not is_authorized(user_id, username):
        bot.reply_to(
            message,
            "⛔ You are not authorized to use this bot. Please contact the administrator."
        )
        return
        
    sender = username or message.from_user.first_name or "Unknown"
    logger.info(f"Received message from {sender}: {text[:50]}...")
    
    # Extract Instagram links using regex
    instagram_links = extract_instagram_links(text)
    
    if instagram_links:
        logger.info(f"Found {len(instagram_links)} Instagram links")
        
        for link in instagram_links:
            success, result = process_instagram_link(link, sender)
            
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
        logger.info("No Instagram links found in message")
        bot.reply_to(
            message,
            "❓ I didn't recognize any Instagram links in your message.\n\n"
            "Please send a valid Instagram link that starts with https://instagram.com/ or https://www.instagram.com/"
        )

def run_polling():
    """Start the bot in polling mode"""
    # First, remove any webhook
    bot.remove_webhook()
    
    logger.info("Starting bot in polling mode...")
    # Start polling
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    run_polling() 