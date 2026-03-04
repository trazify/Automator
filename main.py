"""
YouTube Shorts Automation - Main Orchestrator
Manages three YouTube channels with automated upload and scheduling
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from modules.logger import get_logger
from modules.auth import authenticate_channel
from modules.validator import ShortsValidator
from modules.metadata import MetadataGenerator
from modules.uploader import YouTubeUploader
from modules.scheduler import VideoScheduler
from modules.quota import QuotaManager
from modules.smart_queue import SmartQueueManager


class YouTubeShortsAutomation:
    """Main automation orchestrator"""
    
    def __init__(self, config_file='channels_config.json', daily_video_limit=2):
        """Initialize automation system"""
        # Load environment variables
        load_dotenv()
        
        # Initialize logger
        self.logger = get_logger()
        
        # Load channel configuration
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.channels = config['channels']
        
        # Initialize quota manager
        max_quota = int(os.getenv('MAX_DAILY_QUOTA', 10000))
        max_shorts = int(os.getenv('MAX_SHORTS_PER_DAY', 6))
        self.quota_manager = QuotaManager(max_quota, max_shorts)
        
        # Initialize smart queue manager
        self.smart_queue = SmartQueueManager(daily_limit=daily_video_limit)
        
        # Get timezone
        self.timezone = os.getenv('TIMEZONE', 'Asia/Kolkata')
        
        # Get client secret file
        self.client_secret = os.getenv('CLIENT_SECRET_FILE', 'client_secret.json')
        
        # Statistics
        self.total_uploaded = 0
        self.total_failed = 0
    
    def process_channel(self, channel_config):
        """
        Process all videos for a single channel
        
        Args:
            channel_config: Channel configuration dict
        
        Returns:
            tuple: (success_count, fail_count)
        """
        channel_name = channel_config['display_name']
        queue_folder = Path(channel_config['queue_folder'])
        archive_folder = Path(channel_config['archive_folder'])
        
        # Use smart queue to select videos for today
        video_files = self.smart_queue.select_videos(queue_folder)
        
        if not video_files:
            # Check if there are any videos at all
            all_videos = list(queue_folder.glob('*.mp4')) if queue_folder.exists() else []
            if all_videos:
                can_process, remaining = self.smart_queue.can_process_more()
                if not can_process:
                    self.logger.info(f"[{channel_name}] Daily limit reached - videos available but not processing")
                else:
                    self.logger.info(f"[{channel_name}] All videos already processed")
            else:
                self.logger.info(f"[{channel_name}] No videos in queue")
            return 0, 0
        
        self.logger.channel_start(channel_name, len(video_files))
        
        # Authenticate channel
        try:
            youtube = authenticate_channel(channel_config, self.client_secret)
        except Exception as e:
            self.logger.error(f"[{channel_name}] Authentication failed: {e}")
            return 0, len(video_files)
        
        # Initialize uploader and scheduler
        uploader = YouTubeUploader(youtube)
        scheduler = VideoScheduler(youtube, self.timezone)
        
        success_count = 0
        fail_count = 0
        
        # Process each video
        for video_path in video_files:
            # Check quota before processing
            can_upload, reason = self.quota_manager.can_upload()
            if not can_upload:
                self.logger.quota_exhausted(
                    self.quota_manager.usage['units_used'],
                    self.quota_manager.max_daily_quota
                )
                # Mark remaining videos as failed
                fail_count += len(video_files) - (success_count + fail_count)
                break
            
            self.logger.info(f"\n Processing: {video_path.name}")
            
            # Validate video
            is_valid, error_msg = ShortsValidator.validate(video_path)
            if not is_valid:
                self.logger.validation_failed(channel_name, video_path.name, error_msg)
                fail_count += 1
                continue
            
            # Get metadata
            metadata = MetadataGenerator.get_metadata(video_path, channel_config['niche'])
            self.logger.info(f"   Title: {metadata['title']}")
            
            # Upload video
            video_id = uploader.upload_video(str(video_path), metadata)
            if not video_id:
                self.logger.upload_failed(channel_name, video_path.name, "Upload failed")
                fail_count += 1
                continue
            
            # Schedule video
            publish_at = scheduler.schedule_video(video_id, channel_config['schedule_time'])
            if not publish_at:
                self.logger.error(f"   Scheduling failed for video {video_id}")
                fail_count += 1
                continue
            
            # Record quota usage
            self.quota_manager.record_upload()
            
            # Mark video as processed in smart queue
            self.smart_queue.mark_processed(video_path)
            
            # Archive video
            self._archive_video(video_path, archive_folder)
            
            # Log success
            self.logger.success(channel_name, video_id, publish_at, video_path.name)
            success_count += 1
        
        self.logger.channel_complete(channel_name, success_count, fail_count)
        return success_count, fail_count
    
    def _archive_video(self, video_path, archive_folder):
        """
        Move video to archive folder
        
        Args:
            video_path: Path to video file
            archive_folder: Archive folder path
        """
        # Create dated subfolder
        today = datetime.now().strftime("%Y-%m-%d")
        dated_folder = Path(archive_folder) / today
        dated_folder.mkdir(parents=True, exist_ok=True)
        
        # Move video file
        dest_path = dated_folder / video_path.name
        shutil.move(str(video_path), str(dest_path))
        
        # Move metadata file if it exists
        json_path = video_path.with_suffix('.json')
        if json_path.exists():
            json_dest = dated_folder / json_path.name
            shutil.move(str(json_path), str(json_dest))
    
    def run(self):
        """Run the automation for all channels"""
        self.logger.session_start()
        
        # Reset quota if new day
        self.quota_manager.reset_if_needed()
        
        # Reset smart queue if new day
        self.smart_queue.reset_if_new_day()
        
        # Show quota status
        remaining = self.quota_manager.get_remaining()
        self.logger.info(f" Quota Status: {remaining['shorts_uploaded']}/{self.quota_manager.max_shorts_per_day} Shorts | "
                        f"{remaining['units_used']}/{self.quota_manager.max_daily_quota} units")
        
        # Show smart queue status
        queue_status = self.smart_queue.get_status()
        self.logger.info(f" Daily Video Limit: {queue_status['processed_today']}/{queue_status['daily_limit']} videos processed today")
        
        # Show queue statistics
        queue_folders = [ch['queue_folder'] for ch in self.channels]
        queue_stats = self.smart_queue.get_queue_stats(queue_folders)
        
        self.logger.info(f"\n Queue Statistics:")
        for folder, stats in queue_stats.items():
            folder_name = Path(folder).name
            self.logger.info(f"  {folder_name}: {stats['total']} total videos | {stats['unprocessed']} unprocessed")
        
        if queue_status['remaining_slots'] == 0:
            self.logger.warning(f"\n Daily video limit reached ({queue_status['daily_limit']} videos/day)")
            self.logger.info(f"Next upload window: Tomorrow")
            self.logger.session_end(0, 0)
            return
        
        self.logger.info(f"\n Processing up to {queue_status['remaining_slots']} video(s) today...\n")
        
        # Process each channel
        for channel_config in self.channels:
            try:
                success, failed = self.process_channel(channel_config)
                self.total_uploaded += success
                self.total_failed += failed
            except Exception as e:
                self.logger.error(f"Error processing channel {channel_config['display_name']}: {e}")
                continue
        
        # Show final quota status
        remaining = self.quota_manager.get_remaining()
        self.logger.info(f"\n Final Quota: {remaining['shorts_uploaded']}/{self.quota_manager.max_shorts_per_day} Shorts | "
                        f"{remaining['units_used']}/{self.quota_manager.max_daily_quota} units")
        
        self.logger.session_end(self.total_uploaded, self.total_failed)


def main():
    """Main entry point"""
    try:
        automation = YouTubeShortsAutomation()
        automation.run()
    except KeyboardInterrupt:
        print("\n\n Automation interrupted by user")
    except Exception as e:
        print(f"\n\n Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
