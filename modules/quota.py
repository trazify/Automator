"""
Quota Module - Track and enforce YouTube API quota limits
"""

from datetime import datetime, timezone
import json
from pathlib import Path


class QuotaManager:
    """Manage YouTube API quota usage"""
    
    # API costs (in quota units)
    UPLOAD_COST = 1600
    UPDATE_COST = 50
    TOTAL_COST_PER_SHORT = UPLOAD_COST + UPDATE_COST  # 1650 units
    
    def __init__(self, max_daily_quota=10000, max_shorts_per_day=6, quota_file='logs/quota.json'):
        """
        Initialize quota manager
        
        Args:
            max_daily_quota: Maximum daily quota (default 10000)
            max_shorts_per_day: Maximum Shorts per day (default 6)
            quota_file: Path to quota tracking file
        """
        self.max_daily_quota = max_daily_quota
        self.max_shorts_per_day = max_shorts_per_day
        self.quota_file = Path(quota_file)
        self.quota_file.parent.mkdir(exist_ok=True)
        
        self.usage = self._load_usage()
    
    def _load_usage(self):
        """Load quota usage from file"""
        if self.quota_file.exists():
            try:
                with open(self.quota_file, 'r') as f:
                    usage = json.load(f)
                
                # Check if usage is from today
                usage_date = datetime.fromisoformat(usage.get('date', '2000-01-01'))
                today = datetime.now().date()
                
                if usage_date.date() == today:
                    return usage
            except Exception as e:
                print(f"Error loading quota file: {e}")
        
        # Return fresh usage for today
        return {
            'date': datetime.now().isoformat(),
            'units_used': 0,
            'shorts_uploaded': 0
        }
    
    def _save_usage(self):
        """Save quota usage to file"""
        try:
            with open(self.quota_file, 'w') as f:
                json.dump(self.usage, f, indent=2)
        except Exception as e:
            print(f"Error saving quota file: {e}")
    
    def can_upload(self):
        """
        Check if we can upload another Short
        
        Returns:
            tuple: (can_upload, reason)
        """
        # Check Shorts limit
        if self.usage['shorts_uploaded'] >= self.max_shorts_per_day:
            return False, f"Daily Shorts limit reached ({self.max_shorts_per_day})"
        
        # Check quota limit
        projected_usage = self.usage['units_used'] + self.TOTAL_COST_PER_SHORT
        if projected_usage > self.max_daily_quota:
            return False, f"Quota limit would be exceeded ({projected_usage}/{self.max_daily_quota} units)"
        
        return True, None
    
    def record_upload(self):
        """Record a successful upload"""
        self.usage['units_used'] += self.TOTAL_COST_PER_SHORT
        self.usage['shorts_uploaded'] += 1
        self.usage['date'] = datetime.now().isoformat()
        self._save_usage()
    
    def get_remaining(self):
        """
        Get remaining quota
        
        Returns:
            dict with remaining units and Shorts
        """
        return {
            'units_remaining': self.max_daily_quota - self.usage['units_used'],
            'shorts_remaining': self.max_shorts_per_day - self.usage['shorts_uploaded'],
            'units_used': self.usage['units_used'],
            'shorts_uploaded': self.usage['shorts_uploaded']
        }
    
    def reset_if_needed(self):
        """Reset quota if it's a new day"""
        usage_date = datetime.fromisoformat(self.usage['date'])
        today = datetime.now().date()
        
        if usage_date.date() != today:
            print("🔄 New day detected - resetting quota")
            self.usage = {
                'date': datetime.now().isoformat(),
                'units_used': 0,
                'shorts_uploaded': 0
            }
            self._save_usage()
