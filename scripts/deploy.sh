#!/bin/bash

# Script to deploy the Telegram Bot to an existing Vercel project

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project details
PROJECT_NAME="ddf-reels-bot"

# Load environment variables
ENV_FILE=.env
if [ -f "$ENV_FILE" ]; then
    echo -e "${BLUE}Loading environment variables from $ENV_FILE...${NC}"
    source "$ENV_FILE"
else
    echo -e "${RED}Error: $ENV_FILE not found. Please make sure the .env file exists.${NC}"
    exit 1
fi

# Check if required environment variables are set
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$CODA_API_KEY" ] || [ -z "$CODA_DOC_ID" ] || [ -z "$CODA_TABLE_ID" ] || [ -z "$CODA_LINK_COLUMN_ID" ]; then
    echo -e "${RED}Error: Required environment variables are missing in $ENV_FILE.${NC}"
    exit 1
fi

# Create temporary files for environment variables
echo -e "${BLUE}Creating temporary files for environment variables...${NC}"
echo "$TELEGRAM_BOT_TOKEN" > .env.TELEGRAM_BOT_TOKEN
echo "$CODA_API_KEY" > .env.CODA_API_KEY
echo "$CODA_DOC_ID" > .env.CODA_DOC_ID
echo "$CODA_TABLE_ID" > .env.CODA_TABLE_ID
echo "$CODA_LINK_COLUMN_ID" > .env.CODA_LINK_COLUMN_ID

# Set environment variables in Vercel
echo -e "${BLUE}Setting up environment variables in Vercel...${NC}"
echo -e "${YELLOW}You may be prompted to select your project and scope during this process.${NC}"

# Add each environment variable to Vercel for production
echo -e "${BLUE}Adding TELEGRAM_BOT_TOKEN...${NC}"
vercel env add TELEGRAM_BOT_TOKEN production < .env.TELEGRAM_BOT_TOKEN

echo -e "${BLUE}Adding CODA_API_KEY...${NC}"
vercel env add CODA_API_KEY production < .env.CODA_API_KEY

echo -e "${BLUE}Adding CODA_DOC_ID...${NC}"
vercel env add CODA_DOC_ID production < .env.CODA_DOC_ID

echo -e "${BLUE}Adding CODA_TABLE_ID...${NC}"
vercel env add CODA_TABLE_ID production < .env.CODA_TABLE_ID

echo -e "${BLUE}Adding CODA_LINK_COLUMN_ID...${NC}"
vercel env add CODA_LINK_COLUMN_ID production < .env.CODA_LINK_COLUMN_ID

# Clean up temporary files
rm .env.TELEGRAM_BOT_TOKEN .env.CODA_API_KEY .env.CODA_DOC_ID .env.CODA_TABLE_ID .env.CODA_LINK_COLUMN_ID

# Deploy the application
echo -e "${BLUE}Deploying application to Vercel...${NC}"
DEPLOY_OUTPUT=$(vercel --prod)
echo "$DEPLOY_OUTPUT"

# Extract deployment URL from the output
DEPLOYMENT_URL=$(echo "$DEPLOY_OUTPUT" | grep -o "https://[^ ]*\.vercel\.app" | head -n 1)

if [ -z "$DEPLOYMENT_URL" ]; then
    echo -e "${YELLOW}Couldn't automatically get the deployment URL.${NC}"
    read -p "Please enter your deployment URL manually (e.g., https://ddf-reels-bot.vercel.app): " DEPLOYMENT_URL
fi

# Set up Telegram webhook
if [ ! -z "$DEPLOYMENT_URL" ]; then
    echo -e "${BLUE}Setting up Telegram webhook...${NC}"
    WEBHOOK_URL="$DEPLOYMENT_URL/api/webhook"
    TELEGRAM_WEBHOOK_URL="https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook?url=$WEBHOOK_URL"
    
    WEBHOOK_RESPONSE=$(curl -s "$TELEGRAM_WEBHOOK_URL")
    
    if [[ $WEBHOOK_RESPONSE == *"\"ok\":true"* ]]; then
        echo -e "${GREEN}Successfully set up Telegram webhook at $WEBHOOK_URL${NC}"
    else
        echo -e "${RED}Failed to set up Telegram webhook.${NC}"
        echo -e "${YELLOW}Response: $WEBHOOK_RESPONSE${NC}"
        echo -e "${YELLOW}Try manually setting up the webhook by visiting:${NC}"
        echo "$TELEGRAM_WEBHOOK_URL"
    fi
    
    # Update local .env file with the webhook URL
    if grep -q "WEBHOOK_URL=" "$ENV_FILE"; then
        sed -i.bak "s|WEBHOOK_URL=.*|WEBHOOK_URL=$DEPLOYMENT_URL|" "$ENV_FILE"
        rm -f "$ENV_FILE.bak" # Remove backup file
    else
        echo "WEBHOOK_URL=$DEPLOYMENT_URL" >> "$ENV_FILE"
    fi
    
    echo -e "${GREEN}Deployment complete!${NC}"
    echo -e "${GREEN}Your Telegram bot is now running at $DEPLOYMENT_URL${NC}"
    echo -e "${BLUE}Bot username: @ddfreelsbot${NC}"
    echo -e "${BLUE}Try sending an Instagram Reel link to your bot on Telegram!${NC}"
fi 