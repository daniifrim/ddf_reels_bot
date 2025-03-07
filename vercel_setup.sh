#!/bin/bash

# Script to set up the Telegram Bot on Vercel

# Color definitions
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

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

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

# Project name with a timestamp to ensure uniqueness
DEFAULT_PROJECT_NAME="ddf-reels-bot-$(date +%s)"

# Ask for Vercel project name
read -p "Enter your Vercel project name (default: $DEFAULT_PROJECT_NAME): " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-$DEFAULT_PROJECT_NAME}

# Prompt for team/scope
echo -e "${BLUE}Do you want to deploy to a specific Vercel team? (Useful if you have multiple teams)${NC}"
read -p "Enter team slug or leave empty for personal account: " TEAM_SLUG

# Set team flag if a team was specified
TEAM_FLAG=""
if [ ! -z "$TEAM_SLUG" ]; then
    TEAM_FLAG="--scope $TEAM_SLUG"
fi

# Log in to Vercel if not already logged in
echo -e "${BLUE}Checking Vercel login status...${NC}"
vercel whoami &> /dev/null || vercel login

# Check if this is already a Vercel project
if [ ! -f ".vercel/project.json" ]; then
    echo -e "${BLUE}Initializing Vercel project...${NC}"
    vercel $TEAM_FLAG --confirm
fi

# Set environment variables
echo -e "${BLUE}Setting up environment variables...${NC}"
vercel env add TELEGRAM_BOT_TOKEN $TEAM_FLAG <<< "$TELEGRAM_BOT_TOKEN"
vercel env add CODA_API_KEY $TEAM_FLAG <<< "$CODA_API_KEY"
vercel env add CODA_DOC_ID $TEAM_FLAG <<< "$CODA_DOC_ID"
vercel env add CODA_TABLE_ID $TEAM_FLAG <<< "$CODA_TABLE_ID"
vercel env add CODA_LINK_COLUMN_ID $TEAM_FLAG <<< "$CODA_LINK_COLUMN_ID"

# Deploy the application
echo -e "${BLUE}Deploying application to Vercel...${NC}"
DEPLOYMENT_URL=$(vercel $TEAM_FLAG --prod | grep "https://" | head -n 1)

if [ -z "$DEPLOYMENT_URL" ]; then
    echo -e "${RED}Failed to retrieve deployment URL.${NC}"
    echo -e "${YELLOW}Please check the Vercel dashboard for your deployment URL.${NC}"
else
    # Set up Telegram webhook
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
    sed -i.bak "s|WEBHOOK_URL=.*|WEBHOOK_URL=$DEPLOYMENT_URL|" "$ENV_FILE"
    rm "$ENV_FILE.bak" # Remove backup file
    
    echo -e "${GREEN}Deployment complete!${NC}"
    echo -e "${GREEN}Your Telegram bot is now running at $DEPLOYMENT_URL${NC}"
    echo -e "${BLUE}Bot username: @ddfreelsbot${NC}"
    echo -e "${BLUE}Try sending an Instagram Reel link to your bot on Telegram!${NC}"
fi 