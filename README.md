# DDF Reels Bot

A Telegram bot for collecting Instagram links and saving them to a Coda database.

## Project Structure

```
ddf_reels_bot/
├── api/                    # Vercel serverless functions
│   └── index.py            # Main webhook handler
├── scripts/                # Utility scripts
│   ├── deploy.sh           # Deployment scripts
│   └── vercel_setup.js     # Vercel configuration
├── src/                    # Source code
│   ├── __init__.py         # Package initialization
│   ├── bot.py              # Main bot logic
│   ├── monitoring.py       # Monitoring utilities
│   └── utils.py            # Common utilities
├── tests/                  # Test files
│   ├── test_bot.py         # Bot testing
│   └── test_coda_*.py      # Coda API tests
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── DEPLOYMENT.md           # Deployment documentation
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel configuration
└── README.md               # Project documentation
```

## Features

- Collects Instagram links from Telegram messages
- Saves links to a Coda database
- Supports both polling and webhook modes
- Configurable authorization system
- Admin commands for monitoring

## Setup

1. Clone this repository
2. Copy `.env.example` to `.env` and fill in the required values
3. Install dependencies with `pip install -r requirements.txt`
4. Run the bot locally with `python -m src.bot`

## Environment Variables

The following environment variables are required:

| Name | Description | Example |
|------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `CODA_API_KEY` | Coda API key | `3e92f721-91d1-485e-aab9-b7d50e4fa4da` |
| `CODA_DOC_ID` | Coda document ID | `NYzN0H9At4` |
| `CODA_TABLE_ID` | Coda table ID | `grid-Pyccn7MrAA` |

Optional environment variables:

| Name | Description | Default |
|------|-------------|---------|
| `ENVIRONMENT` | Environment name | `production` |
| `AUTHORIZED_USERS` | Comma-separated list of usernames | Empty (all users allowed) |
| `ADMIN_USERS` | Comma-separated list of Telegram user IDs | Empty (no admins) |
| `LOG_LEVEL` | Logging level | `INFO` |
| `WEBHOOK_URL` | Webhook URL for Telegram | Required for webhook mode |

## Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Quick Deployment to Vercel

1. Ensure all environment variables are set up on Vercel
2. Deploy using the Vercel CLI or GitHub integration
3. Set up the Telegram webhook using the following URL:
   ```
   https://api.telegram.org/bot{YOUR_BOT_TOKEN}/setWebhook?url={YOUR_VERCEL_URL}/api/webhook
   ```

## Development

To run the bot locally:

```bash
# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the bot in polling mode
python -m src.bot
```

## Testing

Run tests with:

```bash
python -m unittest discover tests
```

Individual tests can be run with:

```bash
python -m tests.test_bot
python -m tests.test_coda_connection
```

## License

This project is proprietary and owned by DDF. 