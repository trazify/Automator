"""
Validator Module - Validate videos meet YouTube Shorts requirements
"""

from pathlib import Path

try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip


class ShortsValidator:
    """Validates videos for YouTube Shorts requirements"""
    
    MAX_DURATION = 60  # seconds
    
    @staticmethod
    def validate(video_path):
        """
        Validate video meets Shorts requirements
        
        Args:
            video_path: Path to video file
        
        Returns:
            tuple: (is_valid, error_message)
        """
        video_path = Path(video_path)
        
        # Check if file exists
        if not video_path.exists():
            return False, "File does not exist"
        
        # Check file extension
        valid_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        if video_path.suffix.lower() not in valid_extensions:
            return False, f"Invalid file format. Must be one of: {', '.join(valid_extensions)}"
        
        try:
            # Load video and check duration
            with VideoFileClip(str(video_path)) as clip:
                duration = clip.duration
                
                if duration > ShortsValidator.MAX_DURATION:
                    return False, f"Video too long: {duration:.1f}s (max {ShortsValidator.MAX_DURATION}s)"
                
                if duration < 1:
                    return False, "Video too short (minimum 1 second)"
                
                # Note: We assume vertical format (9:16) - no strict validation
                # YouTube will handle aspect ratio automatically
                
                return True, None
        
        except Exception as e:
            return False, f"Error reading video: {str(e)}"
    
    @staticmethod
    def get_video_info(video_path):
        """
        Get video information
        
        Args:
            video_path: Path to video file
        
        Returns:
            dict with video info or None if error
        """
        try:
            with VideoFileClip(str(video_path)) as clip:
                return {
                    'duration': clip.duration,
                    'fps': clip.fps,
                    'size': (clip.w, clip.h),
                    'aspect_ratio': clip.w / clip.h if clip.h > 0 else 0
                }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
