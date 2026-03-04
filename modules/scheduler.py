"""
Scheduler Module - Schedule videos with publishAt
"""

from datetime import datetime, timedelta
import random
import pytz
from googleapiclient.errors import HttpError


class VideoScheduler:
    """Schedule YouTube videos for publishing"""
    
    def __init__(self, youtube_service, timezone='Asia/Kolkata'):
        """
        Initialize scheduler
        
        Args:
            youtube_service: Authenticated YouTube service object
            timezone: Timezone for scheduling (default: Asia/Kolkata)
        """
        self.youtube = youtube_service
        self.timezone = pytz.timezone(timezone)
    
    def schedule_video(self, video_id, schedule_time_str, add_jitter=True):
        """
        Schedule video for publishing
        
        Args:
            video_id: YouTube video ID
            schedule_time_str: Time string in HH:MM format (e.g., "10:00")
            add_jitter: Add random 5-10 minute jitter to avoid spam detection
        
        Returns:
            ISO-8601 formatted publish time if successful, None otherwise
        """
        try:
            # Calculate next available schedule time
            now = datetime.now(self.timezone)
            
            # Parse schedule time
            hour, minute = map(int, schedule_time_str.split(':'))
            
            # Create scheduled datetime for today
            scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if scheduled <= now:
                scheduled = scheduled + timedelta(days=1)
            
            # Add random jitter (5-10 minutes)
            if add_jitter:
                jitter_minutes = random.randint(5, 10)
                scheduled = scheduled + timedelta(minutes=jitter_minutes)
            
            # Convert to ISO-8601 format with timezone
            publish_at = scheduled.isoformat()
            
            # Update video status with publishAt
            body = {
                'id': video_id,
                'status': {
                    'privacyStatus': 'private',
                    'publishAt': publish_at,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            request = self.youtube.videos().update(
                part='status',
                body=body
            )
            
            response = request.execute()
            
            print(f"  ⏰ Scheduled for: {scheduled.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            
            return publish_at
        
        except HttpError as e:
            print(f"  ✗ HTTP Error during scheduling: {e}")
            return None
        except Exception as e:
            print(f"  ✗ Error during scheduling: {e}")
            return None
    
    def get_next_schedule_time(self, schedule_time_str):
        """
        Get next available schedule time (for display purposes)
        
        Args:
            schedule_time_str: Time string in HH:MM format
        
        Returns:
            datetime object
        """
        now = datetime.now(self.timezone)
        hour, minute = map(int, schedule_time_str.split(':'))
        scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if scheduled <= now:
            scheduled = scheduled + timedelta(days=1)
        
        return scheduled
