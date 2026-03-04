# 🤖 Auto-Upload Feature Guide

## Overview

The system now includes **Smart Queue Management** that automatically selects and uploads a limited number of videos per day from a large pool of videos. Perfect for managing thousands of videos without manual intervention!

---

## ✨ How It Works

### 1. **Add Thousands of Videos**
Drop as many videos as you want into the queue folders:
```
queue/
├── ai_viral/          ← 1000+ videos
├── anime_edits/       ← 1000+ videos
└── memes/             ← 1000+ videos
```

### 2. **Set Daily Limit**
The system will automatically select **2 videos per day** (configurable) from your queue.

### 3. **Run Daily**
Set up Task Scheduler to run `python main.py` once per day (e.g., 9:00 AM).

### 4. **Automatic Selection**
- System randomly selects 2 unprocessed videos
- Uploads them as PRIVATE
- Schedules them for configured times
- Marks them as processed (won't upload again)
- Resets counter at midnight

---

## ⚙️ Configuration

### Change Daily Video Limit

Edit `.env` file:
```
DAILY_VIDEO_LIMIT=2    # Change to 3, 4, 5, etc.
```

**Important Limits:**
- **Maximum**: 6 videos/day (YouTube API quota limit)
- **Recommended**: 2-3 videos/day for sustainable growth

### Per-Channel Distribution

The system processes channels in order:
1. AI Viral Channel (gets first slot)
2. Anime Edits Channel (gets second slot)
3. Memes Channel (gets third slot if limit allows)

If you want 2 videos/day and have 3 channels, it will rotate through them.

---

## 📊 What You'll See

When you run `python main.py`, you'll see:

```
================================================================================
YouTube Shorts Automation - Session Started
================================================================================
📊 Quota Status: 0/6 Shorts | 0/10000 units
🎬 Daily Video Limit: 0/2 videos processed today

📁 Queue Statistics:
  ai_viral: 1523 total videos | 1523 unprocessed
  anime_edits: 2104 total videos | 2104 unprocessed
  memes: 987 total videos | 987 unprocessed

▶ Processing up to 2 video(s) today...

📹 Processing: video_001.mp4
  📝 Title: This AI is Incredible 🤯 #shorts
  ⬆ Uploading video...
  ✓ Upload complete | Video ID: abc123
  ⏰ Scheduled for: 2026-01-30 10:07:00 IST
  ✓ [AI-Generated Viral Shorts] Video uploaded

📹 Processing: video_045.mp4
  📝 Title: Epic Anime Moment 💫 #shorts
  ⬆ Uploading video...
  ✓ Upload complete | Video ID: xyz789
  ⏰ Scheduled for: 2026-01-30 14:12:00 IST
  ✓ [Anime Edit Shorts] Video uploaded

================================================================================
Session Complete | Uploaded: 2 | Failed: 0
================================================================================
```

---

## 🔄 Daily Workflow

### Day 1
- Run: `python main.py`
- Uploads: 2 videos (randomly selected)
- Remaining: 1521 unprocessed in ai_viral, 2103 in anime_edits, 987 in memes

### Day 2
- Run: `python main.py` (via Task Scheduler)
- Uploads: 2 different videos
- Remaining: 1519 unprocessed...

### Day 750+
- Still uploading 2 videos/day
- Never uploads the same video twice
- Fully automated!

---

## 🎯 Smart Features

### 1. **No Duplicates**
The system tracks which videos have been processed in `logs/queue_state.json`:
```json
{
  "date": "2026-01-29T09:00:00",
  "videos_processed_today": 2,
  "processed_videos": [
    "queue/ai_viral/video_001.mp4",
    "queue/anime_edits/video_045.mp4"
  ]
}
```

### 2. **Daily Reset**
At midnight, the counter resets:
- `videos_processed_today` → 0
- Ready to process 2 more videos

### 3. **Random Selection**
Videos are selected randomly for variety, not sequentially.

### 4. **Graceful Limits**
If daily limit is reached:
```
⚠ Daily video limit reached (2 videos/day)
Next upload window: Tomorrow
```

---

## 📅 Task Scheduler Setup

### Windows Task Scheduler

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task
3. **Name**: YouTube Shorts Auto-Upload
4. **Trigger**: Daily at 9:00 AM
5. **Action**: Start a program
   - **Program**: `python`
   - **Arguments**: `main.py`
   - **Start in**: `C:\Users\gn17g\OneDrive\Desktop\automator`
6. **Settings**:
   - ✅ Run whether user is logged on or not
   - ✅ Run with highest privileges
   - ✅ If task fails, restart every 1 hour (max 3 attempts)

### Result
- System runs automatically at 9:00 AM every day
- Selects 2 videos
- Uploads and schedules them
- You wake up to new videos scheduled!

---

## 💡 Pro Tips

### Tip 1: Organize by Batches
```
queue/ai_viral/
├── batch_001/
│   ├── video_001.mp4
│   ├── video_002.mp4
│   └── ...
├── batch_002/
│   └── ...
```

### Tip 2: Monitor Queue State
Check processed videos:
```powershell
type logs\queue_state.json
```

### Tip 3: Reset if Needed
To start fresh (re-upload all videos):
```powershell
del logs\queue_state.json
```

### Tip 4: Adjust Based on Growth
- Starting out: 2 videos/day
- Growing channel: 3-4 videos/day
- Established: 5-6 videos/day (max)

---

## 🔧 Advanced Configuration

### Different Limits Per Channel

Currently, the limit is global (2 videos/day total). If you want different limits per channel, you can modify `channels_config.json`:

```json
{
  "channels": [
    {
      "name": "ai_viral",
      "daily_limit": 1
    },
    {
      "name": "anime_edits",
      "daily_limit": 1
    }
  ]
}
```

(This would require code modification - let me know if you need this!)

---

## 📈 Example: 1 Year of Automation

**Starting Point:**
- 3,000 videos in queue folders
- Daily limit: 2 videos/day

**After 1 Year:**
- Videos uploaded: 730 (2 × 365 days)
- Videos remaining: 2,270
- Manual work: 0 hours
- Time saved: ~365 hours (1 hour/day)

---

## ✅ Summary

✅ **Drop thousands of videos** in queue folders  
✅ **Set daily limit** (default: 2 videos/day)  
✅ **Set up Task Scheduler** to run daily  
✅ **System automatically**:
   - Selects 2 random unprocessed videos
   - Uploads as PRIVATE
   - Schedules for configured times
   - Marks as processed
   - Resets daily

**Result**: Fully automated YouTube Shorts channel with zero manual work! 🎉

---

## 🚀 Ready to Use

Your system is already configured for 2 videos/day. Just:

1. Add your thousands of videos to queue folders
2. Run `python main.py` to test
3. Set up Task Scheduler for daily automation
4. Enjoy automated uploads!
