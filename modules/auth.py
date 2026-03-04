"""
Authentication Module - OAuth 2.0 for YouTube Data API
Handles multi-channel authentication with token persistence
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# YouTube API scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
]


class YouTubeAuthenticator:
    """Handles OAuth authentication for YouTube channels"""
    
    def __init__(self, client_secret_file='client_secret.json'):
        """Initialize authenticator with client secret file"""
        self.client_secret_file = client_secret_file
        
        if not os.path.exists(client_secret_file):
            raise FileNotFoundError(
                f"Client secret file not found: {client_secret_file}\n"
                "Please download it from Google Cloud Console and place it in the project root."
            )
    
    def authenticate(self, token_file):
        """
        Authenticate and return YouTube service object
        
        Args:
            token_file: Path to token pickle file (e.g., 'tokens/token_ai.pickle')
        
        Returns:
            YouTube service object
        """
        creds = None
        token_path = Path(token_file)
        
        # Create tokens directory if it doesn't exist
        token_path.parent.mkdir(exist_ok=True)
        
        # Load existing token if available
        if token_path.exists():
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If credentials are invalid or don't exist, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired token
                print(f"Refreshing token for {token_file}...")
                creds.refresh(Request())
            else:
                # First-time authentication - opens browser
                print(f"\n{'='*60}")
                print(f"First-time authentication required for: {token_file}")
                print(f"A browser window will open. Please:")
                print(f"1. Sign in to the YouTube channel")
                print(f"2. Grant permissions to the app")
                print(f"3. This only happens once per channel")
                print(f"{'='*60}\n")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save token for future use
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            print(f"✓ Token saved to {token_file}")
        
        # Build and return YouTube service
        youtube = build('youtube', 'v3', credentials=creds)
        return youtube
    
    def get_channel_info(self, youtube):
        """
        Get authenticated channel information
        
        Args:
            youtube: YouTube service object
        
        Returns:
            dict with channel ID and title
        """
        try:
            request = youtube.channels().list(
                part='snippet,contentDetails',
                mine=True
            )
            response = request.execute()
            
            if 'items' in response and len(response['items']) > 0:
                channel = response['items'][0]
                return {
                    'id': channel['id'],
                    'title': channel['snippet']['title']
                }
            else:
                return None
        except Exception as e:
            print(f"Error getting channel info: {e}")
            return None


def authenticate_channel(channel_config, client_secret_file='client_secret.json'):
    """
    Convenience function to authenticate a channel
    
    Args:
        channel_config: Channel configuration dict
        client_secret_file: Path to client secret JSON
    
    Returns:
        YouTube service object
    """
    authenticator = YouTubeAuthenticator(client_secret_file)
    youtube = authenticator.authenticate(channel_config['token_file'])
    
    # Verify authentication by getting channel info
    channel_info = authenticator.get_channel_info(youtube)
    if channel_info:
        print(f"✓ Authenticated as: {channel_info['title']} ({channel_info['id']})")
    
    return youtube
