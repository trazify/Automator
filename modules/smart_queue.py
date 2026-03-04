"""
Smart Queue Manager - Automatically selects videos for daily upload
Limits uploads to 2 videos per day from a large pool
"""

import os
import json
from pathlib import Path
from datetime import datetime
import random


class SmartQueueManager:
    """Manages daily video selection from large queue"""
    
    def __init__(self, state_file='logs/queue_state.json', daily_limit=2):
        """
        Initialize smart queue manager
        
        Args:
            state_file: Path to state tracking file
            daily_limit: Maximum videos to process per day (default: 2)
        """
        self.state_file = Path(state_file)
        self.daily_limit = daily_limit
        self.state = self._load_state()
    
    def _load_state(self):
        """Load queue state from file"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                
                # Check if state is from today
                state_date = datetime.fromisoformat(state.get('date', '2000-01-01'))
                today = datetime.now().date()
                
                if state_date.date() == today:
                    return state
            except Exception as e:
                print(f"Error loading queue state: {e}")
        
        # Return fresh state for today
        return {
            'date': datetime.now().isoformat(),
            'videos_processed_today': 0,
            'processed_videos': []
        }
    
    def _save_state(self):
        """Save queue state to file"""
        self.state_file.parent.mkdir(exist_ok=True)
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Error saving queue state: {e}")
    
    def reset_if_new_day(self):
        """Reset counter if it's a new day"""
        state_date = datetime.fromisoformat(self.state['date'])
        today = datetime.now().date()
        
        if state_date.date() != today:
            print(f"🔄 New day detected - resetting daily video counter")
            self.state = {
                'date': datetime.now().isoformat(),
                'videos_processed_today': 0,
                'processed_videos': []
            }
            self._save_state()
    
    def can_process_more(self):
        """
        Check if we can process more videos today
        
        Returns:
            tuple: (can_process, remaining_slots)
        """
        remaining = self.daily_limit - self.state['videos_processed_today']
        return remaining > 0, remaining
    
    def select_videos(self, queue_folder, video_extensions=['.mp4', '.mov', '.avi', '.mkv', '.webm']):
        """
        Select videos from queue folder for today's upload
        
        Args:
            queue_folder: Path to queue folder
            video_extensions: List of valid video extensions
        
        Returns:
            list: Selected video paths (limited by remaining daily slots)
        """
        queue_path = Path(queue_folder)
        
        if not queue_path.exists():
            return []
        
        # Get all videos in queue
        all_videos = []
        for ext in video_extensions:
            all_videos.extend(queue_path.glob(f'*{ext}'))
        
        if not all_videos:
            return []
        
        # Filter out already processed videos
        unprocessed_videos = [
            v for v in all_videos 
            if str(v) not in self.state['processed_videos']
        ]
        
        if not unprocessed_videos:
            print(f"  ℹ All videos in {queue_folder} have been processed")
            return []
        
        # Check how many we can process
        can_process, remaining = self.can_process_more()
        
        if not can_process:
            print(f"  ⚠ Daily limit reached ({self.daily_limit} videos/day)")
            return []
        
        # Select videos (random or sequential - using random for variety)
        num_to_select = min(remaining, len(unprocessed_videos))
        selected = random.sample(unprocessed_videos, num_to_select)
        
        return selected
    
    def mark_processed(self, video_path):
        """
        Mark a video as processed
        
        Args:
            video_path: Path to processed video
        """
        self.state['videos_processed_today'] += 1
        self.state['processed_videos'].append(str(video_path))
        self.state['date'] = datetime.now().isoformat()
        self._save_state()
    
    def get_status(self):
        """
        Get current queue status
        
        Returns:
            dict with status information
        """
        can_process, remaining = self.can_process_more()
        return {
            'date': self.state['date'],
            'processed_today': self.state['videos_processed_today'],
            'daily_limit': self.daily_limit,
            'remaining_slots': remaining,
            'can_process': can_process
        }
    
    def get_queue_stats(self, queue_folders):
        """
        Get statistics about queue folders
        
        Args:
            queue_folders: List of queue folder paths
        
        Returns:
            dict with queue statistics
        """
        stats = {}
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        
        for folder in queue_folders:
            folder_path = Path(folder)
            if not folder_path.exists():
                stats[folder] = {'total': 0, 'unprocessed': 0}
                continue
            
            # Count total videos
            total_videos = []
            for ext in video_extensions:
                total_videos.extend(folder_path.glob(f'*{ext}'))
            
            # Count unprocessed videos
            unprocessed = [
                v for v in total_videos 
                if str(v) not in self.state['processed_videos']
            ]
            
            stats[folder] = {
                'total': len(total_videos),
                'unprocessed': len(unprocessed)
            }
        
        return stats
