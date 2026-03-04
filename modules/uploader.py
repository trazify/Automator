"""
Uploader Module - Upload videos to YouTube
"""

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import os


class YouTubeUploader:
    """Upload videos to YouTube"""
    
    def __init__(self, youtube_service):
        """
        Initialize uploader with YouTube service
        
        Args:
            youtube_service: Authenticated YouTube service object
        """
        self.youtube = youtube_service
    
    def upload_video(self, video_path, metadata):
        """
        Upload video to YouTube as PRIVATE
        
        Args:
            video_path: Path to video file
            metadata: dict with title, description, tags, category_id
        
        Returns:
            Video ID if successful, None otherwise
        """
        try:
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': metadata.get('title', 'Untitled Short'),
                    'description': metadata.get('description', ''),
                    'tags': metadata.get('tags', ['shorts']),
                    'categoryId': metadata.get('category_id', '22')  # People & Blogs
                },
                'status': {
                    'privacyStatus': 'private',  # Upload as private initially
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                video_path,
                chunksize=-1,  # Upload in a single request
                resumable=True,
                mimetype='video/*'
            )
            
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            print(f"  ⬆ Uploading video...")
            
            # Upload with progress
            response = request.execute()
            
            video_id = response['id']
            print(f"  ✓ Upload complete | Video ID: {video_id}")
            
            return video_id
        
        except HttpError as e:
            print(f"  ✗ HTTP Error during upload: {e}")
            return None
        except Exception as e:
            print(f"  ✗ Error during upload: {e}")
            return None
    
    def set_thumbnail(self, video_id, thumbnail_path):
        """
        Set custom thumbnail for video (optional)
        
        Args:
            video_id: YouTube video ID
            thumbnail_path: Path to thumbnail image
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(thumbnail_path):
            return False
        
        try:
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            )
            request.execute()
            print(f"  ✓ Thumbnail set")
            return True
        except Exception as e:
            print(f"  ✗ Error setting thumbnail: {e}")
            return False
