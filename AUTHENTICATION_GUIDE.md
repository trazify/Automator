# 🔐 Manual Authentication Guide

## Why Manual Authentication is Needed

OAuth 2.0 authentication requires **interactive browser windows** to open where you'll:
1. Sign in to each YouTube channel
2. Grant permissions to the app
3. Allow the system to save tokens

This process **cannot be automated** - you need to run it manually in your terminal.

---

## Step-by-Step Authentication Process

### Step 1: Open PowerShell/Terminal

Open a new PowerShell window (not through VS Code or any IDE).

### Step 2: Navigate to Project Directory

```powershell
cd C:\Users\gn17g\OneDrive\Desktop\automator
```

### Step 3: Run the Authentication Script

```powershell
python main.py
```

---

## What Will Happen

### For Each Channel (3 times total):

1. **Console Message Appears**:
   ```
   ============================================================
   First-time authentication required for: tokens/token_ai.pickle
   A browser window will open. Please:
   1. Sign in to the YouTube channel
   2. Grant permissions to the app
   3. This only happens once per channel
   ============================================================
   ```

2. **Browser Window Opens**:
   - A new browser tab/window will open automatically
   - You'll see a Google sign-in page

3. **Sign In**:
   - **IMPORTANT**: Sign in to the CORRECT YouTube channel for each token:
     - **First browser** → AI Viral Channel
     - **Second browser** → Anime Edits Channel
     - **Third browser** → Memes Channel

4. **Grant Permissions**:
   - You'll see a permissions screen asking to allow the app to:
     - Upload videos
     - Manage your YouTube account
   - Click **"Allow"** or **"Continue"**

5. **Success Message**:
   ```
   ✓ Token saved to tokens/token_ai.pickle
   ✓ Authenticated as: [Your Channel Name] ([Channel ID])
   ```

6. **Repeat for Next Channel**:
   - The process repeats automatically for the next channel
   - Total: 3 browser windows (one per channel)

---

## After Authentication

Once all 3 channels are authenticated, you'll see:

```
================================================================================
YouTube Shorts Automation - Session Started
================================================================================
📊 Quota Status: 0/6 Shorts | 0/10000 units
[AI-Generated Viral Shorts] No videos in queue
[Anime Edit Shorts] No videos in queue
[Meme Shorts] No videos in queue
================================================================================
Session Complete | Uploaded: 0 | Failed: 0
================================================================================
```

This is **normal** - there are no videos in the queue yet!

---

## Verify Authentication Worked

Check that token files were created:

```powershell
dir tokens
```

You should see:
```
token_ai.pickle
token_anime.pickle
token_memes.pickle
```

---

## Test with Sample Videos

After authentication, test the system:

### 1. Create test videos (<60 seconds each)

Place them in queue folders:
```
queue/ai_viral/test1.mp4
queue/anime_edits/test2.mp4
queue/memes/test3.mp4
```

### 2. Run the automation

```powershell
python main.py
```

### 3. Check YouTube Studio

Go to YouTube Studio for each channel and verify:
- ✅ Videos uploaded as PRIVATE
- ✅ Scheduled for correct times (AI: 10 AM, Anime: 2 PM, Memes: 8 PM)
- ✅ Metadata applied (title, description, tags)

---

## Troubleshooting

### Browser doesn't open
- Make sure you're running in a regular PowerShell window (not VS Code terminal)
- Check if your default browser is set correctly
- Try running as administrator

### "Access blocked: This app's request is invalid"
- Make sure you added your email as a test user in Google Cloud Console
- Go to: APIs & Services → OAuth consent screen → Test users
- Add all three YouTube channel emails

### Wrong channel signed in
- Delete the token file: `del tokens\token_*.pickle`
- Run `python main.py` again
- Sign in to the correct channel this time

### Authentication hangs
- Press Ctrl+C to cancel
- Check your internet connection
- Make sure `client_secret.json` is valid

---

## Ready to Authenticate?

Open a **new PowerShell window** and run:

```powershell
cd C:\Users\gn17g\OneDrive\Desktop\automator
python main.py
```

Follow the browser prompts for each of the 3 channels!

---

**After authentication is complete, the system will be fully automated and ready for daily use!** 🚀
