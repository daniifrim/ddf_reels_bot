#!/usr/bin/env python3
"""
DDF Reels Bot - Local Development Entrypoint

This is the main entry point for local development.
It allows running the bot in polling mode locally.
"""

from src.bot import run_polling

if __name__ == "__main__":
    print("Starting DDF Reels Bot in polling mode...")
    print("Press Ctrl+C to stop")
    run_polling() 