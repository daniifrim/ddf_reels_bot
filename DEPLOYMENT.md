# Deployment Guide for DDF Reels Bot

This guide explains how to properly deploy the DDF Reels Bot to Vercel with the correct environment setup.

## Required Environment Variables

The bot requires the following environment variables to function properly:

| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot API token | `123456789:ABCDefGhIJKlmnOPQRstUVwxyz` |
| `CODA_API_KEY` | Coda API key | `3e92f721-91d1-485e-aab9-b7d50e4fa4da` |
| `CODA_DOC_ID` | Coda document ID | `NYzN0H9At4` |
| `CODA_TABLE_ID` | Coda table ID | `grid-Pyccn7MrAA` |
| `CODA_LINK_COLUMN_ID` | Column ID for links | `c-LFekrYG0se` |

## Optional Environment Variables

These variables are optional and have sensible defaults:

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `production` |
| `AUTHORIZED_USERS` | Comma-separated list of usernames | *empty* (all users allowed) |
| `ADMIN_USERS` | Comma-separated list of telegram user IDs | *empty* (no admins) |
| `LOG_LEVEL` | Logging level | `INFO` |
| `WEBHOOK_URL` | Webhook URL for Telegram | *required for webhook mode* |

## Setting up Environment Variables on Vercel

### Method 1: Using the Vercel Dashboard

1. Go to your project on the Vercel dashboard
2. Navigate to Settings > Environment Variables
3. Add each required environment variable
4. Deploy or redeploy your project

### Method 2: Using Vercel CLI

Create a `.env` file locally with all your environment variables:

```
TELEGRAM_BOT_TOKEN=your_bot_token
CODA_API_KEY=your_coda_api_key
CODA_DOC_ID=your_doc_id
CODA_TABLE_ID=your_table_id
CODA_LINK_COLUMN_ID=your_column_id
```

Then use Vercel CLI to set these variables:

```bash
# First login to Vercel
vercel login

# Pull existing environment variables and merge with your local .env
vercel env pull

# Add each environment variable
cat .env | while IFS= read -r line; do
  if [[ $line != \#* && $line != "" ]]; then
    key=$(echo $line | cut -d= -f1)
    value=$(echo $line | cut -d= -f2-)
    echo "Adding $key..."
    echo $value | vercel env add $key production
  fi
done

# Deploy with the updated environment
vercel --prod
```

## Testing Your Deployment

After deployment, you should test your bot:

1. Send a message to your bot on Telegram
2. Try sending an Instagram link
3. Check your Coda database to verify the link was saved

## Troubleshooting

### 1. Environment Variable Issues

If your bot fails with environment variable errors, check:
- That all required variables are properly set
- There are no typos in the variable names
- The values are correctly formatted (especially the Coda IDs)

### 2. Coda 404 Errors

If you get a 404 error when saving to Coda:
- Verify the `CODA_DOC_ID` - should NOT include any "d" prefix
- Check that `CODA_TABLE_ID` includes the full ID (e.g., `grid-Pyccn7MrAA` not just `Pyccn7MrAA`)
- Ensure your Coda API key has access to the document

### 3. Telegram Webhook Issues

If the bot isn't responding to messages:
- Verify the webhook is properly set
- Check Vercel logs for any errors
- Ensure the Telegram bot token is correct

## Security Notes

- Never commit your `.env` file or any files containing sensitive tokens to version control
- Use environment secrets in CI/CD pipelines instead of hardcoded values
- Regularly rotate your API keys for better security

## Why Vercel?

Vercel offers several advantages for deploying this bot:

1. **Instant response times**: Serverless functions run on-demand, providing quick responses to messages.
2. **Zero maintenance**: No need to manage servers or worry about uptime.
3. **Automatic scaling**: Handles any number of concurrent messages without configuration.
4. **Simple deployment**: Easy integration with GitHub for continuous deployment.

## Prerequisites

Before you begin, make sure you have:

1. A GitHub account
2. A Vercel account (you can sign up at [vercel.com](https://vercel.com) using your GitHub account)
3. Your Telegram bot token (from BotFather)
4. Your Coda API credentials

## Step 1: Prepare Your Repository

1. Push your bot code to a GitHub repository:

```bash
# Initialize git repository if needed
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/ddf-reels-bot.git

# Push to GitHub
git push -u origin main
```

## Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with your GitHub account
2. Click "Add New" → "Project"
3. Select your GitHub repository from the list
4. Vercel will automatically detect that this is a Python project

## Step 3: Configure Environment Variables

1. In the Vercel project settings, add the following environment variables:

| Name | Value | Description |
|------|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `7780725841:AAEkNzWjmG6jr2wDCS5w--YjupCQDSPmkm0` | Your Telegram bot token |
| `CODA_API_KEY` | `3e92f721-91d1-485e-aab9-b7d50e4fa4da` | Your Coda API key |
| `CODA_DOC_ID` | `dNYzN0H9At4` | Your Coda document ID |
| `CODA_TABLE_ID` | `tun7MrAA` | Your Coda table ID |
| `CODA_LINK_COLUMN_ID` | `c-LFekrYG0se` | The column ID for links |

## Step 4: Deploy

1. Click "Deploy" to start the deployment process
2. Vercel will build and deploy your project
3. Once complete, you'll get a deployment URL (e.g., `https://ddf-reels-bot.vercel.app`)

## Step 5: Set Up the Webhook

After deployment, you need to set up the webhook to connect Telegram to your Vercel deployment:

1. Open your browser and navigate to the following URL (replace with your actual values):

```
https://api.telegram.org/bot7780725841:AAEkNzWjmG6jr2wDCS5w--YjupCQDSPmkm0/setWebhook?url=https://your-vercel-url.vercel.app/api/webhook
```

2. You should see a response indicating the webhook was set successfully:

```json
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

## Step 6: Testing the Bot

1. Open Telegram and start a conversation with your bot (@ddfreelsbot)
2. Send a message like `/start` to check if the bot responds
3. Send an Instagram Reel link to test the full functionality

## Updating the Bot

When you need to update the bot:

1. Make changes to your local code
2. Commit and push to GitHub
3. Vercel will automatically redeploy the updated code

## Monitor Performance

You can monitor the performance of your bot using Vercel's dashboard:

1. Go to your project in the Vercel dashboard
2. Click on "Analytics" to see function invocations, execution time, and errors

## Additional Tips

- **Custom Domain**: You can set up a custom domain for your bot in the Vercel project settings
- **Development Environment**: Use the local development server for testing before deploying
- **Logs**: Check the Vercel Function Logs for debugging information 