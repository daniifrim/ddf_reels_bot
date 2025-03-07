# DDF Reels Bot

A Telegram bot for collecting Instagram Reel links and sending them to a Coda database.

## Features

- Collects Instagram Reel links shared in Telegram messages
- Automatically saves links to a Coda database
- Provides user-friendly confirmation messages
- Robust error handling and logging
- Serverless deployment to Vercel for instant response times

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- A Telegram Bot (already created via BotFather)
- Coda API key and document access
- Vercel account (for deployment)

## Local Development

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/ddf_reels_bot.git
cd ddf_reels_bot
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with the following contents:

```
TELEGRAM_BOT_TOKEN=7780725841:AAEkNzWjmG6jr2wDCS5w--YjupCQDSPmkm0
CODA_API_KEY=3e92f721-91d1-485e-aab9-b7d50e4fa4da
CODA_DOC_ID=dNYzN0H9At4
CODA_TABLE_ID=tun7MrAA
CODA_LINK_COLUMN_ID=c-LFekrYG0se
WEBHOOK_URL=https://your-vercel-deployment-url.vercel.app
```

4. For local testing with webhooks, run:

```bash
python api/index.py
```

## Deploying to Vercel

This bot is designed to run as a serverless function on Vercel, which ensures instant responses to messages.

### Automatic Deployment (Recommended)

1. Fork/Push this repository to GitHub
2. Log in to Vercel and create a new project from your GitHub repository
3. During the setup, Vercel will automatically detect the Python project
4. Set the environment variables in the Vercel project settings
5. Deploy the project

### Manual Deployment

1. Install the Vercel CLI:

```bash
npm install -g vercel
```

2. Login to Vercel:

```bash
vercel login
```

3. Deploy the project:

```bash
vercel
```

## Setting up the Webhook for Telegram

After deploying to Vercel, you need to set up the webhook for your Telegram bot:

1. Get your Vercel deployment URL (e.g., `https://your-project.vercel.app`)
2. Set the webhook by visiting the following URL in your browser:

```
https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={VERCEL_URL}/api/webhook
```

Replace `{TELEGRAM_BOT_TOKEN}` with your bot token and `{VERCEL_URL}` with your Vercel deployment URL.

## Usage

1. Deploy the bot to Vercel following the instructions above
2. Set up the webhook for your Telegram bot
3. Open Telegram and start a conversation with your bot (@ddfreelsbot)
4. Send an Instagram Reel link to the bot
5. The bot will instantly save the link to your Coda database and provide confirmation

## Bot Commands

- `/start` - Initiates the bot and displays a welcome message
- `/help` - Shows help information about how to use the bot

## Customization

You can modify the bot to add more features:

- Track sender information in Coda by adding additional columns
- Add validation for specific types of Reels
- Implement rate limiting or access control
- Create admin commands for statistics

## Troubleshooting

If you encounter issues:

- Check the Vercel deployment logs for errors
- Verify your Telegram webhook is set correctly
- Make sure all environment variables are set properly
- Test the Coda API connection separately
- Check Telegram Bot API status

## License

This project is licensed under the MIT License - see the LICENSE file for details. 