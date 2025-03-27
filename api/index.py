import os
import json
import telebot
import traceback
import sys
from flask import Flask, request, Response, jsonify
from dotenv import load_dotenv

# Import our shared utility functions
# Use relative imports for Vercel compatibility
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import get_required_env, extract_instagram_links, send_to_coda

# Load environment variables
load_dotenv()

# Initialize Flask app for Vercel serverless function
app = Flask(__name__)

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
except ValueError as e:
    # In production, this will cause the server to fail fast with a clear error
    print(f"Configuration error: {str(e)}")
    if __name__ != "__main__":  # Only exit if not in local development
        sys.exit(1)

# Initialize Telegram Bot
print("Initializing Telegram Bot")
bot = telebot.TeleBot(BOT_TOKEN)
print("Bot initialized successfully")

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
        
        # Extract Instagram links using shared utility function
        instagram_links = extract_instagram_links(text)
        print(f"Extracted Instagram links: {instagram_links}")
        
        if not instagram_links:
            print("No Instagram links found in message")
            send_telegram_message(chat_id, "I don't recognize any Instagram links in your message. Please send a valid Instagram link.")
            return jsonify({"status": "success", "message": "No Instagram links found"}), 200
        
        # Create coda config from environment variables
        coda_config = {
            "api_key": CODA_API_KEY,
            "doc_id": DOC_ID,
            "table_id": TABLE_ID,
            "column_name": "Link"  # Use column name for stability
        }
        
        # Process each link
        success_count = 0
        for link in instagram_links:
            success, _ = send_to_coda(link, coda_config)
            
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