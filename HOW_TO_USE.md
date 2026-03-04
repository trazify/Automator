# 🎬 How to Use YouTube Shorts Automation

## Quick Overview

This system automatically uploads and schedules YouTube Shorts to 3 different channels. Here's how to use it:

---

## 📁 Step 1: Add Videos to Queue Folders

Drop your short videos (<60 seconds) into the appropriate folder:

```
queue/
├── ai_viral/          ← Put AI-related videos here
├── anime_edits/       ← Put anime edit videos here
└── memes/             ← Put meme videos here
```

**Example:**
```powershell
# Copy videos to queue folders
Copy-Item "C:\Downloads\my_ai_video.mp4" "queue\ai_viral\"
Copy-Item "C:\Downloads\anime_clip.mp4" "queue\anime_edits\"
Copy-Item "C:\Downloads\funny_meme.mp4" "queue\memes\"
```

**Or just drag and drop** the videos into the folders using File Explorer!

---

## ▶️ Step 2: Run the Automation

Open PowerShell and run:

```powershell
cd C:\Users\gn17g\OneDrive\Desktop\automator
python main.py
```

---

## 🔐 Step 3: First-Time Authentication (One-Time Only)

**The first time you run with videos**, browser windows will open:

### Browser Window 1 - AI Viral Channel
1. Sign in to your **AI Viral YouTube channel**
2. Click **"Allow"** to grant permissions
3. Close the browser tab

### Browser Window 2 - Anime Edits Channel
1. Sign in to your **Anime Edits YouTube channel**
2. Click **"Allow"** to grant permissions
3. Close the browser tab

### Browser Window 3 - Memes Channel
1. Sign in to your **Memes YouTube channel**
2. Click **"Allow"** to grant permissions
3. Close the browser tab

**After this, you'll never need to authenticate again!** The system saves tokens.

---

## ✅ Step 4: Check the Results

### In PowerShell
You'll see output like:
```
📹 Processing: my_ai_video.mp4
  📝 Title: This AI is Mind-Blowing 🤯 #shorts
  ⬆ Uploading video...
  ✓ Upload complete | Video ID: abc123xyz
  ⏰ Scheduled for: 2026-01-30 10:07:00 IST
  ✓ [AI-Generated Viral Shorts] Video uploaded
```

### In YouTube Studio
1. Go to YouTube Studio for each channel
2. Click **"Content"**
3. You'll see your videos:
   - Status: **Private**
   - Scheduled: **Tomorrow at 10:00 AM** (or configured time)
   - Title, description, tags: **Auto-generated**

### In Archive Folders
Processed videos are moved to:
```
archive/
├── ai_viral/2026-01-29/my_ai_video.mp4
├── anime_edits/2026-01-29/anime_clip.mp4
└── memes/2026-01-29/funny_meme.mp4
```

### In Logs
Check detailed logs:
```powershell
type logs\daily_report_2026-01-29.log
```

---

## 🎨 Optional: Custom Metadata

Want custom titles/descriptions instead of auto-generated ones?

Create a `.json` file with the same name as your video:

**Example:** For `my_video.mp4`, create `my_video.json`:

```json
{
  "title": "My Custom Title 🔥 #shorts",
  "description": "This is my custom description!\n\n#viral #shorts",
  "tags": ["custom", "tag1", "tag2", "shorts"],
  "schedule_time": "14:30"
}
```

Put both files in the queue folder:
```
queue/ai_viral/
├── my_video.mp4
└── my_video.json
```

---

## 🤖 Daily Automation (Optional)

Want videos to upload automatically every day?

### Set Up Windows Task Scheduler

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click **"Create Basic Task"**
3. **Name**: YouTube Shorts Automation
4. **Trigger**: Daily at 9:00 AM (or your preferred time)
5. **Action**: Start a program
   - **Program**: `python`
   - **Arguments**: `main.py`
   - **Start in**: `C:\Users\gn17g\OneDrive\Desktop\automator`
6. Click **Finish**

Now the system runs automatically every day!

---

## 📊 Understanding the Schedule

Videos are scheduled for these times (local time - IST):

| Channel | Default Time | Can Change? |
|---------|-------------|-------------|
| AI Viral | 10:00 AM | Yes* |
| Anime Edits | 2:00 PM | Yes* |
| Memes | 8:00 PM | Yes* |

*To change times, edit `channels_config.json`

Each upload gets a random 5-10 minute jitter to avoid spam detection.

---

## 🚨 Important Limits

- **Maximum**: 6 Shorts per day (across all channels)
- **Reason**: YouTube API quota limit (10,000 units/day)
- **What happens**: System stops automatically when limit reached

---

## 🔄 Daily Workflow

### Morning (or whenever)
1. Drop videos in queue folders
2. (Optional) Run `python main.py` manually
3. Or let Task Scheduler run it automatically

### What Happens
- Videos upload as PRIVATE
- Videos get scheduled for configured times
- Videos move to archive
- Logs are created

### Result
- Videos publish automatically at scheduled times
- You never touch YouTube Studio manually!

---

## 💡 Pro Tips

### Tip 1: Batch Processing
Drop multiple videos at once:
```
queue/ai_viral/
├── video1.mp4
├── video2.mp4
├── video3.mp4
└── video4.mp4
```

All will be processed in one run!

### Tip 2: Check Logs
Always check logs after running:
```powershell
type logs\daily_report_2026-01-29.log
```

### Tip 3: Verify in YouTube Studio
After first upload, verify:
- ✅ Video is PRIVATE
- ✅ Scheduled time is correct
- ✅ Metadata looks good

### Tip 4: Keep Videos Under 60 Seconds
The system validates this automatically and rejects longer videos.

---

## ❓ Common Questions

**Q: Do I need to authenticate every time?**  
A: No! Only the first time. Tokens are saved.

**Q: Can I upload to just one channel?**  
A: Yes! Just put videos in that channel's queue folder.

**Q: What if I exceed the quota?**  
A: System stops automatically and logs a warning.

**Q: Can I change the schedule times?**  
A: Yes! Edit `channels_config.json` and change `schedule_time`.

**Q: Where do videos go after processing?**  
A: They move to `archive/[channel]/[date]/`

---

## 🎯 Summary

1. **Add videos** to `queue/` folders
2. **Run** `python main.py`
3. **Authenticate** (first time only)
4. **Done!** Videos upload and schedule automatically

**That's it! The system handles everything else.** 🚀

---

## 📞 Need Help?

- Check `README.md` for full documentation
- Check `AUTHENTICATION_GUIDE.md` for OAuth help
- Check `logs/` for error messages
- Review `TEST_RESULTS.md` for system status
