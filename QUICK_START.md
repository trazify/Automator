# 🚀 Quick Start Guide

## Step 1: Rename OAuth File

Your OAuth credentials file needs to be renamed:

```powershell
cd C:\Users\gn17g\OneDrive\Desktop\automator
Rename-Item "client_secret_156776284900.json.json" "client_secret.json"
```

## Step 2: First-Time Authentication

Run the automation system:

```powershell
python main.py
```

**What will happen:**
- 3 browser windows will open (one for each channel)
- You'll be asked to sign in to each YouTube channel
- Grant permissions to the app
- Tokens will be saved automatically

**IMPORTANT**: Sign in to the correct YouTube channel for each prompt:
1. **First browser** → AI Viral Channel
2. **Second browser** → Anime Edits Channel  
3. **Third browser** → Memes Channel

## Step 3: Test with Sample Videos

Drop test videos (<60 seconds) in the queue folders:

```
queue/
├── ai_viral/test1.mp4
├── anime_edits/test2.mp4
└── memes/test3.mp4
```

Run again:
```powershell
python main.py
```

## Step 4: Verify in YouTube Studio

1. Go to YouTube Studio for each channel
2. Check that videos are:
   - ✅ Uploaded as PRIVATE
   - ✅ Scheduled for correct times
   - ✅ Have proper metadata (title, description, tags)

## Step 5: Set Up Daily Automation

### Windows Task Scheduler

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click **"Create Basic Task"**
3. **Name**: YouTube Shorts Automation
4. **Trigger**: Daily at 9:00 AM (or your preferred time)
5. **Action**: Start a program
   - **Program/script**: `python`
   - **Add arguments**: `main.py`
   - **Start in**: `C:\Users\gn17g\OneDrive\Desktop\automator`
6. Click **Finish**

## Daily Workflow

1. **Drop videos** in queue folders throughout the day
2. **Automation runs** daily (via Task Scheduler)
3. **Videos uploaded** and scheduled automatically
4. **Check logs**: `logs/daily_report_YYYY-MM-DD.log`
5. **Processed videos** move to `archive/`

## Troubleshooting

### "Client secret file not found"
- Make sure you renamed the file to exactly `client_secret.json`

### "Access blocked: This app's request is invalid"
- Add your email as a test user in Google Cloud Console
- Go to: APIs & Services → OAuth consent screen → Test users

### Authentication window doesn't open
- Check if browser is blocking popups
- Try running as administrator

## Need Help?

- Check `README.md` for full documentation
- Review `OAUTH_SETUP_GUIDE.md` for OAuth issues
- Check logs in `logs/` folder for errors

---

**You're all set! 🎉**

Once authentication is complete, the system will run automatically every day.
