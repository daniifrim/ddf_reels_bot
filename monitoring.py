import os
import logging
import traceback
from datetime import datetime
import json
import time

# Configure logging with rotating file handler
def setup_logging():
    """Set up logging configuration with file rotation"""
    log_directory = "logs"
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers to avoid duplication
    if logger.handlers:
        logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler with current date in filename
    log_filename = os.path.join(
        log_directory, 
        f"bot_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Create a simple in-memory counter for monitoring
class BotMonitor:
    """Simple monitoring class for the bot"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.stats = {
            "messages_received": 0,
            "valid_links_received": 0,
            "invalid_links_received": 0,
            "successful_submissions": 0,
            "failed_submissions": 0,
            "errors": 0,
            "last_activity": self.start_time.isoformat()
        }
        self.logger = logging.getLogger("BotMonitor")
        self.log_path = "logs/stats.json"
    
    def record_message(self):
        """Record a received message"""
        self.stats["messages_received"] += 1
        self.update_activity()
    
    def record_valid_link(self):
        """Record a valid Instagram link"""
        self.stats["valid_links_received"] += 1
        self.update_activity()
    
    def record_invalid_link(self):
        """Record an invalid link"""
        self.stats["invalid_links_received"] += 1
        self.update_activity()
    
    def record_successful_submission(self):
        """Record a successful submission to Coda"""
        self.stats["successful_submissions"] += 1
        self.update_activity()
    
    def record_failed_submission(self):
        """Record a failed submission to Coda"""
        self.stats["failed_submissions"] += 1
        self.update_activity()
    
    def record_error(self, error, error_type="General Error"):
        """Record an error with details"""
        self.stats["errors"] += 1
        
        # Log the full traceback
        self.logger.error(f"{error_type}: {error}")
        self.logger.error(traceback.format_exc())
        
        self.update_activity()
    
    def update_activity(self):
        """Update the last activity timestamp"""
        self.stats["last_activity"] = datetime.now().isoformat()
        
        # Save stats to disk periodically
        if self.stats["messages_received"] % 10 == 0:  # Save every 10 messages
            self.save_stats()
    
    def save_stats(self):
        """Save the current stats to a JSON file"""
        try:
            # Create logs directory if it doesn't exist
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            
            # Add uptime to stats before saving
            uptime = (datetime.now() - self.start_time).total_seconds()
            stats_with_uptime = self.stats.copy()
            stats_with_uptime["uptime_seconds"] = uptime
            
            with open(self.log_path, 'w') as f:
                json.dump(stats_with_uptime, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save stats: {e}")
    
    def get_status_report(self):
        """Generate a human-readable status report"""
        uptime = datetime.now() - self.start_time
        uptime_str = f"{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds // 60) % 60}m"
        
        return (
            f"📊 Bot Status Report 📊\n\n"
            f"🕒 Uptime: {uptime_str}\n"
            f"📨 Messages: {self.stats['messages_received']}\n"
            f"✅ Valid links: {self.stats['valid_links_received']}\n"
            f"❌ Invalid links: {self.stats['invalid_links_received']}\n"
            f"📤 Successful submissions: {self.stats['successful_submissions']}\n"
            f"📥 Failed submissions: {self.stats['failed_submissions']}\n"
            f"⚠️ Errors: {self.stats['errors']}\n"
            f"🔄 Last activity: {self.format_time_ago(self.stats['last_activity'])}"
        )
    
    def format_time_ago(self, iso_time_str):
        """Format time as 'X minutes ago'"""
        try:
            activity_time = datetime.fromisoformat(iso_time_str)
            now = datetime.now()
            seconds_ago = (now - activity_time).total_seconds()
            
            if seconds_ago < 60:
                return f"{int(seconds_ago)} seconds ago"
            if seconds_ago < 3600:
                return f"{int(seconds_ago / 60)} minutes ago"
            if seconds_ago < 86400:
                return f"{int(seconds_ago / 3600)} hours ago"
            return f"{int(seconds_ago / 86400)} days ago"
        except Exception:
            return "unknown"

# Create a global instance for use in other modules
monitor = BotMonitor()

# Exception handler decorator for functions
def error_handler(func):
    """Decorator to catch and log exceptions in functions"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Record the error in the monitor
            monitor.record_error(e, f"Error in {func.__name__}")
            
            # Re-raise exceptions in development, swallow in production
            if os.getenv("ENVIRONMENT") == "development":
                raise
            
            # Return a suitable fallback value based on function context
            if func.__name__ == "send_to_coda":
                return False, f"Internal error: {str(e)}"
            return None
    return wrapper 