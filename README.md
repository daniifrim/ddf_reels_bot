# DDF Reels Bot

A Telegram bot for collecting Instagram Reel links and sending them to a Coda database.

## Features

- Collects Instagram Reel links shared in Telegram messages
- Automatically saves links to a Coda database
- Provides user-friendly confirmation messages
- Robust error handling and logging
- Serverless deployment to Vercel for instant response times
- **NEW:** Comprehensive monitoring and statistics
- **NEW:** User authorization to control access
- **NEW:** Admin commands for monitoring bot status

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

# Environment configuration (development, production)
ENVIRONMENT=development

# Optional: Comma-separated list of usernames allowed to use the bot
# Leave empty to allow anyone to use the bot
AUTHORIZED_USERS=

# Optional: Comma-separated list of Telegram user IDs who are admins
# Admins can access statistics and other admin commands
ADMIN_USERS=12345678,87654321

# Logging configuration
LOG_LEVEL=INFO
```

4. For local testing with webhooks, run:

```bash
python api/index.py
```

5. For local testing with polling (recommended for development), run:

```bash
python local_bot.py
```

## Testing

Run the comprehensive test suite to verify all functionality:

```bash
python test_bot.py
```

This will run unit tests for:
- Instagram link pattern validation
- Message handling
- Coda integration
- Error handling

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
- `/stats` - **(Admin only)** Displays bot statistics and performance metrics
- `/version` - **(Admin only)** Shows bot version and environment information

## User Authorization

You can restrict who can use the bot by setting the `AUTHORIZED_USERS` environment variable. This should be a comma-separated list of Telegram usernames. If this variable is empty, anyone can use the bot.

## Admin Access

Set the `ADMIN_USERS` environment variable with a comma-separated list of Telegram user IDs to grant administrative access to certain users. Admins can access statistics and other administrative commands.

## Monitoring and Logging

The bot now includes comprehensive monitoring and logging capabilities:

- Detailed logs are stored in the `logs` directory with daily rotation
- Usage statistics are tracked and can be viewed with the `/stats` command
- Error tracking with detailed information for troubleshooting


## Customization

You can modify the bot to add more features:

- Track sender information in Coda by adding additional columns
- Add validation for specific types of Reels
- Implement rate limiting or access control
- Create more admin commands for additional functionality

## Troubleshooting

If you encounter issues:

- Check the Vercel deployment logs for errors
- Look in the `logs` directory for detailed error information
- Verify your Telegram webhook is set correctly
- Make sure all environment variables are set properly
- Test the Coda API connection separately using `test_coda_connection.py`
- Check Telegram Bot API status

## License

This project is licensed under the MIT License - see the LICENSE file for details. 