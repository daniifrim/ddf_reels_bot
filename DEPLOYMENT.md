# Deploying DDF Reels Bot to Vercel

This guide will walk you through the process of deploying the DDF Reels Bot to Vercel for serverless operation.

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

## Troubleshooting

If you encounter issues:

- **Bot not responding**: Check the Vercel function logs to see if there are any errors
- **Webhook errors**: Make sure you've set the correct URL in the webhook setup
- **Environment variables**: Verify all environment variables are set correctly in Vercel
- **Deployment issues**: Check if the build was successful in the Vercel dashboard

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