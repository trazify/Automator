"""
Metadata Module - Parse and generate metadata for YouTube Shorts
"""

import json
from pathlib import Path
from datetime import datetime
import random


class MetadataGenerator:
    """Generate or parse metadata for YouTube Shorts"""
    
    # Niche-specific templates
    TEMPLATES = {
        'cute_memes': {
            'title_templates': [
                "This Cat is TOO Cute 🥺 #shorts",
                "Funny Dog Moment 😂 #shorts",
                "When Your Pet Does This... 💀 #shorts",
                "Cutest Animal Reaction Ever! 😍 #shorts",
                "You Won't Believe This {animal} 😱 #shorts",
                "POV: Being a Pet Owner 🐶 #shorts"
            ],
            'animals': ['Cat', 'Dog', 'Bunny', 'Hamster', 'Corgi', 'Kitten', 'Puppy'],
            'situations': ['Sleeps Like This', 'Asks for Food', 'Gets Caught', 'Meets a New Friend'],
            'tags': ['cute', 'cat', 'dog', 'funny', 'pet', 'animals', 'shorts', 'wholesome'],
            'description_template': "The cutest animal moment you'll see today! 🥺\n\nLike and subscribe for more daily cuteness! ❤️\n\n#cute #animals #shorts"
        },
        'anime_edits': {
            'title_templates': [
                "{character} {emotion} Edit 🔥 #shorts",
                "{emotion} Anime Moment 💫 #shorts",
                "This {emotion} Scene... 😭 #shorts",
                "{character} Edit | {emotion} #shorts",
                "POV: {emotion} Anime Scene #shorts",
                "{emotion} AMV Edit 🎵 #shorts"
            ],
            'characters': ['Naruto', 'Goku', 'Luffy', 'Eren', 'Tanjiro', 'Itachi', 'Sasuke', 'Zoro'],
            'emotions': ['Epic', 'Emotional', 'Badass', 'Legendary', 'Heartbreaking', 'Powerful', 'Insane'],
            'tags': ['anime', 'animeedit', 'amv', 'animetiktok', 'animemoments', 'otaku', 'shorts'],
            'description_template': "{emotion} anime edit 🔥\n\nLike and follow for more! 💫\n\n#anime #animeedit #shorts"
        },
        'luxury': {
            'title_templates': [
                "{item} Luxury Lifestyle 💎 #shorts",
                "This is {adjective} 🔥 #shorts",
                "{adjective} Aesthetic Vibes ✨ #shorts",
                "Living the {adjective} Life 💫 #shorts",
                "{item} Goals 🎯 #shorts",
                "Pure {adjective} Energy 🌟 #shorts"
            ],
            'items': ['Millionaire', 'Billionaire', 'Luxury', 'Success', 'Dream', 'Elite'],
            'adjectives': ['Elegant', 'Sophisticated', 'Premium', 'Exclusive', 'Timeless', 'Refined'],
            'tags': ['luxury', 'lifestyle', 'aesthetic', 'motivation', 'success', 'millionaire', 'shorts'],
            'description_template': "{adjective} lifestyle aesthetic 💎\n\nFollow for daily motivation! ✨\n\n#luxury #lifestyle #aesthetic #shorts"
        }
    }
    
    @staticmethod
    def load_metadata(video_path):
        """
        Load metadata from JSON file if it exists
        
        Args:
            video_path: Path to video file
        
        Returns:
            dict with metadata or None if not found
        """
        video_path = Path(video_path)
        json_path = video_path.with_suffix('.json')
        
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Ensure #shorts tag is present
                if 'tags' in metadata:
                    if 'shorts' not in [tag.lower() for tag in metadata['tags']]:
                        metadata['tags'].append('shorts')
                
                return metadata
            except Exception as e:
                print(f"Error loading metadata from {json_path}: {e}")
                return None
        
        return None
    
    @staticmethod
    def generate_metadata(niche, video_filename):
        """
        Auto-generate metadata based on channel niche
        
        Args:
            niche: Channel niche (ai_viral, anime_edits, memes)
            video_filename: Name of video file (for logging)
        
        Returns:
            dict with generated metadata
        """
        if niche not in MetadataGenerator.TEMPLATES:
            raise ValueError(f"Unknown niche: {niche}")
        
        template = MetadataGenerator.TEMPLATES[niche]
        
        # Generate title
        title_template = random.choice(template['title_templates'])
        
        # Replace placeholders
        title = title_template
        if '{adjective}' in title:
            title = title.replace('{adjective}', random.choice(template.get('adjectives', [''])))
        if '{animal}' in title:
            title = title.replace('{animal}', random.choice(template.get('animals', ['Animal'])))
        if '{action}' in title:
            title = title.replace('{action}', random.choice(template.get('actions', [''])))
        if '{character}' in title:
            title = title.replace('{character}', random.choice(template.get('characters', [''])))
        if '{emotion}' in title:
            title = title.replace('{emotion}', random.choice(template.get('emotions', [''])))
        if '{situation}' in title:
            situation = random.choice(template.get('situations', ['']))
            title = title.replace('{situation}', situation)
        
        # Generate description
        description = template['description_template']
        if '{action}' in description:
            description = description.replace('{action}', random.choice(template.get('actions', ['something amazing'])))
        if '{emotion}' in description:
            description = description.replace('{emotion}', random.choice(template.get('emotions', ['Epic'])))
        if '{situation}' in description:
            description = description.replace('{situation}', random.choice(template.get('situations', ['this'])))
        
        # Ensure title is not too long (YouTube limit is 100 chars)
        if len(title) > 100:
            title = title[:97] + "..."
        
        metadata = {
            'title': title,
            'description': description,
            'tags': template['tags'].copy(),
            'category_id': '22'  # People & Blogs
        }
        
        return metadata
    
    @staticmethod
    def get_metadata(video_path, niche):
        """
        Get metadata for video - load from JSON or auto-generate
        
        Args:
            video_path: Path to video file
            niche: Channel niche
        
        Returns:
            dict with metadata
        """
        # Try to load from JSON first
        metadata = MetadataGenerator.load_metadata(video_path)
        
        if metadata:
            print(f"  ✓ Loaded metadata from JSON")
            return metadata
        
        # Auto-generate if not found
        print(f"  ⚡ Auto-generating metadata for {niche}")
        metadata = MetadataGenerator.generate_metadata(niche, Path(video_path).name)
        
        return metadata
