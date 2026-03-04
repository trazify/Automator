"""
Logger Module - Centralized logging for YouTube Shorts automation
"""

import logging
import os
from datetime import datetime
from pathlib import Path


class AutomationLogger:
    """Centralized logger for the automation system"""
    
    def __init__(self, log_dir="logs"):
        """Initialize logger with daily log file"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create daily log file
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = self.log_dir / f"daily_report_{today}.log"
        
        # Configure logging
        self.logger = logging.getLogger("YouTubeAutomation")
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def success(self, channel, video_id, scheduled_time, video_file):
        """Log successful upload and schedule"""
        message = f"✓ [{channel}] Video uploaded | ID: {video_id} | Scheduled: {scheduled_time} | File: {video_file}"
        self.info(message)
    
    def upload_failed(self, channel, video_file, error):
        """Log failed upload"""
        message = f"✗ [{channel}] Upload failed | File: {video_file} | Error: {error}"
        self.error(message)
    
    def validation_failed(self, channel, video_file, reason):
        """Log validation failure"""
        message = f"⚠ [{channel}] Validation failed | File: {video_file} | Reason: {reason}"
        self.warning(message)
    
    def quota_exhausted(self, used, limit):
        """Log quota exhaustion"""
        message = f"⚠ QUOTA EXHAUSTED | Used: {used}/{limit} units | Stopping uploads"
        self.warning(message)
    
    def channel_start(self, channel, video_count):
        """Log channel processing start"""
        message = f"▶ [{channel}] Processing {video_count} video(s)"
        self.info(message)
    
    def channel_complete(self, channel, success_count, fail_count):
        """Log channel processing completion"""
        message = f"✓ [{channel}] Complete | Success: {success_count} | Failed: {fail_count}"
        self.info(message)
    
    def session_start(self):
        """Log session start"""
        self.info("=" * 80)
        self.info("YouTube Shorts Automation - Session Started")
        self.info("=" * 80)
    
    def session_end(self, total_uploaded, total_failed):
        """Log session end"""
        self.info("=" * 80)
        self.info(f"Session Complete | Uploaded: {total_uploaded} | Failed: {total_failed}")
        self.info("=" * 80)


# Singleton instance
_logger_instance = None

def get_logger():
    """Get or create logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AutomationLogger()
    return _logger_instance
