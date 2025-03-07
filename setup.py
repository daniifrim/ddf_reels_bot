#!/usr/bin/env python3

import os
import sys
import requests
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import telebot
        import flask
        print("✅ All required packages are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return False

def test_coda_connection():
    """Test the connection to the Coda API"""
    load_dotenv()
    
    # Get Coda API details
    CODA_API_KEY = os.getenv("CODA_API_KEY")
    DOC_ID = os.getenv("CODA_DOC_ID")
    TABLE_ID = os.getenv("CODA_TABLE_ID")
    
    if not all([CODA_API_KEY, DOC_ID, TABLE_ID]):
        print("❌ Missing Coda API credentials in .env file.")
        return False
    
    print("Testing Coda API connection...")
    
    # Test connection by querying the table metadata
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {CODA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            table_info = response.json()
            print(f"✅ Successfully connected to Coda!")
            print(f"Table name: {table_info.get('name', 'Unknown')}")
            print(f"Table ID: {table_info.get('id', 'Unknown')}")
            return True
        else:
            print(f"❌ Failed to connect to Coda API. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Coda API: {str(e)}")
        return False

def setup_telegram_webhook():
    """Set up the webhook for Telegram"""
    load_dotenv()
    
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    if not all([BOT_TOKEN, WEBHOOK_URL]):
        print("❌ Missing Telegram Bot token or Webhook URL in .env file.")
        return False
    
    # Construct the webhook URL
    webhook_url = f"{WEBHOOK_URL}/api/webhook"
    
    print(f"Setting up Telegram webhook to: {webhook_url}")
    
    # Call the Telegram API to set the webhook
    set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}"
    
    try:
        response = requests.get(set_webhook_url)
        result = response.json()
        
        if result.get("ok"):
            print("✅ Webhook set successfully!")
            return True
        else:
            print(f"❌ Failed to set webhook: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting webhook: {str(e)}")
        return False

def check_telegram_bot():
    """Check if the Telegram bot is valid"""
    load_dotenv()
    
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not BOT_TOKEN:
        print("❌ Missing Telegram Bot token in .env file.")
        return False
    
    print("Checking Telegram bot...")
    
    # Call the getMe API to verify the bot
    get_me_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    
    try:
        response = requests.get(get_me_url)
        result = response.json()
        
        if result.get("ok"):
            bot_info = result.get("result", {})
            print(f"✅ Bot is valid!")
            print(f"Bot username: @{bot_info.get('username')}")
            print(f"Bot name: {bot_info.get('first_name')}")
            return True
        else:
            print(f"❌ Invalid bot token: {result.get('description')}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking bot: {str(e)}")
        return False

def main():
    """Main function"""
    print("=== DDF Reels Bot Setup ===")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please create a .env file with the required credentials.")
        return
    
    # Check if dependencies are installed
    if not check_dependencies():
        return
    
    # Test Coda connection
    coda_ok = test_coda_connection()
    
    # Check Telegram bot
    telegram_ok = check_telegram_bot()
    
    # Ask if user wants to set up the webhook
    if coda_ok and telegram_ok:
        webhook_choice = input("\nDo you want to set up the Telegram webhook? (y/n): ")
        if webhook_choice.lower() == 'y':
            webhook_ok = setup_telegram_webhook()
            
            if webhook_ok:
                print("\n=== Setup Complete ===")
                print("Your bot is ready to be deployed to Vercel!")
                print("\nTo deploy to Vercel:")
                print("1. Push this code to a GitHub repository")
                print("2. Connect the repository to Vercel")
                print("3. Set the environment variables in Vercel")
                print("4. Deploy the project")
            else:
                print("\n❌ Webhook setup failed. Please check your WEBHOOK_URL in the .env file.")
        else:
            print("\nSkipping webhook setup.")
            print("You'll need to set up the webhook manually after deploying to Vercel.")
    else:
        print("\n❌ Setup failed. Please fix the issues above before continuing.")

if __name__ == "__main__":
    main() 