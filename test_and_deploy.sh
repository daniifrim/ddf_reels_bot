#!/bin/bash
# Test and deploy script for DDF Reels Bot
# This script runs tests and deploys the bot to Vercel if tests pass

set -e  # Exit on error

echo "=== DDF Reels Bot Testing and Deployment ==="
echo "Starting at $(date)"

# Create logs directory if it doesn't exist
mkdir -p logs

# Function to log messages
log_message() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a logs/deployment.log
}

# Setup virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    log_message "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
log_message "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
log_message "Installing dependencies..."
pip install -r requirements.txt

# Run tests
log_message "Running bot tests..."
python test_bot.py

# If tests pass, proceed with deployment
if [ $? -eq 0 ]; then
    log_message "All tests passed! Proceeding with deployment..."
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        log_message "Vercel CLI not found. Installing..."
        npm install -g vercel
    fi
    
    # Deploy to Vercel
    log_message "Deploying to Vercel..."
    
    # First check if user is logged in to Vercel
    if ! vercel whoami &> /dev/null; then
        log_message "Not logged in to Vercel. Please login:"
        vercel login
    fi
    
    # Deploy
    vercel --prod
    
    if [ $? -eq 0 ]; then
        log_message "Deployment successful!"
        
        # Set up webhook
        WEBHOOK_URL=$(grep WEBHOOK_URL .env | cut -d '=' -f2)
        TOKEN=$(grep TELEGRAM_BOT_TOKEN .env | cut -d '=' -f2)
        
        log_message "Setting up Telegram webhook..."
        WEBHOOK_RESPONSE=$(curl -s "https://api.telegram.org/bot$TOKEN/setWebhook?url=$WEBHOOK_URL/api/webhook")
        
        if [[ $WEBHOOK_RESPONSE == *"\"ok\":true"* ]]; then
            log_message "Webhook set up successfully!"
        else
            log_message "Error setting up webhook. Response: $WEBHOOK_RESPONSE"
        fi
    else
        log_message "Deployment failed."
    fi
else
    log_message "Tests failed. Fix the issues before deploying."
    exit 1
fi

log_message "Process completed at $(date)"
echo "=== Done ===" 