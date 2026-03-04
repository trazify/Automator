# 🚀 YouTube Shorts Automation System

A fully automated, zero-touch YouTube Shorts uploader and scheduler that manages three different YouTube channels with intelligent metadata generation, smart scheduling, and quota management.

## 📋 Features

- ✅ **Multi-Channel Management**: Automate 3 channels (AI Viral, Anime Edits, Memes)
- ✅ **OAuth Token Persistence**: One-time authentication per channel
- ✅ **Smart Metadata Generation**: Auto-generate titles, descriptions, and tags based on niche
- ✅ **Intelligent Scheduling**: Automatic scheduling with anti-spam jitter
- ✅ **Quota Management**: Respects YouTube API limits (10,000 units/day, 6 Shorts max)
- ✅ **Shorts Validation**: Ensures videos meet YouTube Shorts requirements (<60s)
- ✅ **Error Isolation**: One channel failure doesn't affect others
- ✅ **Comprehensive Logging**: Detailed logs with timestamps and status tracking
- ✅ **Automatic Archiving**: Moves processed videos to dated archive folders

## 🏗️ Project Structure

```
automator/
├── main.py                    # Main orchestrator
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
├── channels_config.json       # Channel settings
├── client_secret.json         # OAuth credentials (you provide)
├── modules/
│   ├── auth.py               # OAuth authentication
│   ├── metadata.py           # Metadata generation
│   ├── uploader.py           # YouTube upload
│   ├── scheduler.py          # Smart scheduling
│   ├── validator.py          # Shorts validation
│   ├── quota.py              # Quota management
│   └── logger.py             # Logging utilities
├── queue/                    # Drop videos here
│   ├── ai_viral/
│   ├── anime_edits/
│   └── memes/
├── archive/                  # Processed videos
├── logs/                     # Daily logs
└── tokens/                   # OAuth tokens (auto-generated)
```

## 🔧 Prerequisites

- **Python 3.10+**
- **Google Cloud Project** with YouTube Data API v3 enabled
- **client_secret.json** from Google Cloud Console

## 📦 Installation

### Step 1: Install Dependencies

```powershell
cd C:\Users\gn17g\OneDrive\Desktop\automator
pip install -r requirements.txt
```

### Step 2: Configure OAuth Credentials

Follow the guide in `OAUTH_SETUP_GUIDE.md` to:
1. Create a Google Cloud Project
2. Enable YouTube Data API v3
3. Download `client_secret.json`
4. Place it in the `automator` folder

### Step 3: First-Time Authentication

Run the script for the first time:

```powershell
python main.py
```

The script will:
- Open a browser window for each channel (3 times total)
- Ask you to sign in to each YouTube channel
- Grant permissions to the app
- Save tokens for future use (no re-login needed)

**Important**: Make sure you sign in to the correct YouTube channel for each token:
- Token 1 → AI Viral Channel
- Token 2 → Anime Edits Channel  
- Token 3 → Memes Channel

## 🎬 Usage

### Basic Workflow

1. **Drop videos** into the appropriate queue folder:
   - `queue/ai_viral/` → AI-generated content
   - `queue/anime_edits/` → Anime edits
   - `queue/memes/` → Meme videos

2. **Run the automation**:
   ```powershell
   python main.py
   ```

3. **Check logs** for status:
   ```powershell
   type logs\daily_report_2026-01-29.log
   ```

### Optional: Custom Metadata

Create a `.json` file with the same name as your video:

**Example**: `video1.mp4` + `video1.json`

```json
{
  "title": "This AI is Terrifying 😱 #shorts",
  "description": "Watch what happens when AI goes too far...\n\n#AI #shorts",
  "tags": ["AI", "AIVideo", "viral", "shorts"],
  "schedule_time": "10:00"
}
```

If no `.json` file exists, metadata will be auto-generated based on the channel's niche.

## ⏰ Scheduling

Default upload times (local timezone - IST):
- **AI Channel**: 10:00 AM
- **Anime Channel**: 2:00 PM
- **Meme Channel**: 8:00 PM

Each upload gets a random 5-10 minute jitter to avoid spam detection.

To change schedule times, edit `channels_config.json`:

```json
{
  "schedule_time": "14:30"  // 2:30 PM
}
```

## 🤖 Automation Setup

### Windows Task Scheduler

1. Open **Task Scheduler**
2. Click **Create Basic Task**
3. Name: `YouTube Shorts Automation`
4. Trigger: **Daily** at your preferred time (e.g., 9:00 AM)
5. Action: **Start a program**
   - Program: `python`
   - Arguments: `main.py`
   - Start in: `C:\Users\gn17g\OneDrive\Desktop\automator`
6. Click **Finish**

### Alternative: Manual Run

Run manually whenever you want to upload:

```powershell
cd C:\Users\gn17g\OneDrive\Desktop\automator
python main.py
```

## 📊 Quota Limits

YouTube API has strict quota limits:

- **Daily Quota**: 10,000 units
- **Upload Cost**: ~1,600 units per video
- **Schedule Cost**: ~50 units per video
- **Total Cost**: ~1,650 units per Short
- **Maximum**: 6 Shorts per day (across all channels)

The system automatically tracks quota and stops when limits are reached.

## 🎨 Metadata Templates

### AI Viral Channel
- **Title Style**: Curiosity-driven, mysterious
- **Examples**: 
  - "This AI is Terrifying 😱 #shorts"
  - "Mind-Blowing AI Discovery! 🤖 #shorts"
- **Tags**: `#AI #AIVideo #AIGenerated #shorts`

### Anime Edits Channel
- **Title Style**: Hype, emotional, character-focused
- **Examples**:
  - "Naruto Epic Edit 🔥 #shorts"
  - "Emotional Anime Moment 💫 #shorts"
- **Tags**: `#anime #animeedit #amv #shorts`

### Memes Channel
- **Title Style**: Funny, ironic, relatable
- **Examples**:
  - "POV: Monday morning hits 😂 #shorts"
  - "When the WiFi stops working 💀 #shorts"
- **Tags**: `#memes #funny #relatable #shorts`

## 📝 Logs

Logs are saved in `logs/daily_report_YYYY-MM-DD.log`:

```
2026-01-29 10:15:32 - INFO - ================================================================================
2026-01-29 10:15:32 - INFO - YouTube Shorts Automation - Session Started
2026-01-29 10:15:32 - INFO - ================================================================================
2026-01-29 10:15:33 - INFO - 📊 Quota Status: 0/6 Shorts | 0/10000 units
2026-01-29 10:15:35 - INFO - ▶ [AI-Generated Viral Shorts] Processing 2 video(s)
2026-01-29 10:15:40 - INFO - ✓ [AI-Generated Viral Shorts] Video uploaded | ID: abc123 | Scheduled: 2026-01-30T10:07:00+05:30 | File: video1.mp4
```

## 🔒 Security

- **Never commit** `client_secret.json` or `tokens/*.pickle` to Git
- `.gitignore` is already configured to protect sensitive files
- Keep your OAuth credentials secure

## ❓ Troubleshooting

### "Client secret file not found"
- Make sure `client_secret.json` is in the `automator` folder
- Check the filename is exactly `client_secret.json`

### "Access blocked: This app's request is invalid"
- Add your email as a test user in Google Cloud Console
- Go to: APIs & Services → OAuth consent screen → Test users

### "Quota exceeded"
- Wait until midnight Pacific Time for quota reset
- Reduce videos in queue to stay under 6 Shorts/day

### "Video too long"
- Ensure videos are under 60 seconds
- Use video editing software to trim

### Authentication fails
- Delete the token file: `tokens/token_*.pickle`
- Run `python main.py` again to re-authenticate

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Set up OAuth credentials
3. ✅ Run first-time authentication
4. ✅ Drop test videos in queue folders
5. ✅ Run `python main.py`
6. ✅ Verify uploads in YouTube Studio
7. ✅ Set up Task Scheduler for daily automation

## 📞 Support

For issues or questions:
- Check `logs/` for error messages
- Review `OAUTH_SETUP_GUIDE.md` for authentication help
- Verify quota limits in `logs/quota.json`

---

**Built with ❤️ for zero-touch YouTube Shorts automation**
