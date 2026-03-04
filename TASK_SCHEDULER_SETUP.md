# Windows Task Scheduler Setup Guide

This guide will help you set up automated daily execution of the YouTube Shorts uploader using Windows Task Scheduler.

---

## 🎯 Goal

Create a scheduled task that runs `main.py` every day at 9:00 AM, automatically uploading and scheduling your YouTube Shorts.

---

## 📋 Prerequisites

Before setting up the scheduled task:

- ✅ Python installed and accessible via `python` command
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ OAuth authentication completed (tokens created)
- ✅ System tested manually (`python main.py` works)

---

## 🔧 Method 1: PowerShell Command (Recommended)

### Quick Setup

Open PowerShell as Administrator and run:

```powershell
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\Users\gn17g\OneDrive\Desktop\automator\main.py" -WorkingDirectory "C:\Users\gn17g\OneDrive\Desktop\automator"
$trigger = New-ScheduledTaskTrigger -Daily -At "09:00AM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" -Action $action -Trigger $trigger -Settings $settings -Description "Automated YouTube Shorts uploader for 3 channels"
```

### Verify Task Created

```powershell
Get-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" | Format-List TaskName, State, Description
```

You should see:
```
TaskName    : YouTube Shorts Auto-Upload
State       : Ready
Description : Automated YouTube Shorts uploader for 3 channels
```

---

## 🖱️ Method 2: Task Scheduler GUI

### Step-by-Step Instructions

#### 1. Open Task Scheduler

- Press `Win + R`
- Type `taskschd.msc`
- Press Enter

#### 2. Create Basic Task

1. In the right panel, click **"Create Basic Task..."**
2. Name: `YouTube Shorts Auto-Upload`
3. Description: `Automated YouTube Shorts uploader for 3 channels`
4. Click **Next**

#### 3. Set Trigger

1. Select **"Daily"**
2. Click **Next**
3. Start date: Today's date
4. Start time: `9:00:00 AM`
5. Recur every: `1 days`
6. Click **Next**

#### 4. Set Action

1. Select **"Start a program"**
2. Click **Next**
3. Program/script: `python`
4. Add arguments: `main.py`
5. Start in: `C:\Users\gn17g\OneDrive\Desktop\automator`
6. Click **Next**

#### 5. Configure Advanced Settings

1. Check **"Open the Properties dialog for this task when I click Finish"**
2. Click **Finish**

#### 6. Advanced Properties (Important!)

In the Properties dialog that opens:

**General Tab**:
- ✅ Check "Run whether user is logged on or not"
- ✅ Check "Run with highest privileges"

**Triggers Tab**:
- Click **Edit**
- ✅ Check "Enabled"
- Click **OK**

**Actions Tab**:
- Verify the action is correct
- Program: `python`
- Arguments: `main.py`
- Start in: `C:\Users\gn17g\OneDrive\Desktop\automator`

**Conditions Tab**:
- ✅ **Uncheck** "Start the task only if the computer is on AC power"
- ✅ Check "Wake the computer to run this task" (optional)

**Settings Tab**:
- ✅ Check "Allow task to be run on demand"
- ✅ Check "Run task as soon as possible after a scheduled start is missed"
- ✅ Check "If the task fails, restart every: 1 minute"
- Attempt to restart up to: `3 times`
- If the running task does not end when requested: "Stop the existing instance"

Click **OK** to save.

---

## ✅ Verify the Task

### Test Manual Run

1. Open Task Scheduler
2. Find "YouTube Shorts Auto-Upload" in the task list
3. Right-click → **Run**
4. Check `logs/` folder for new log file
5. Verify videos were processed

### Check Next Run Time

```powershell
Get-ScheduledTaskInfo -TaskName "YouTube Shorts Auto-Upload" | Select-Object LastRunTime, NextRunTime
```

---

## 🔍 Troubleshooting

### Task Shows "Ready" but Never Runs

**Solution**: Check trigger settings
```powershell
Get-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" | Get-ScheduledTaskInfo
```

### Task Runs but Script Fails

**Check Logs**:
1. Open Task Scheduler
2. Right-click task → **Properties**
3. **History** tab → Enable task history
4. Check for error messages

**Common Issues**:

1. **Python not found**:
   - Use full Python path instead of `python`
   - Find path: `where.exe python`
   - Update action to use full path (e.g., `C:\Python310\python.exe`)

2. **Working directory not set**:
   - Verify "Start in" is set to: `C:\Users\gn17g\OneDrive\Desktop\automator`

3. **Permissions issue**:
   - Run task with highest privileges
   - Ensure user account has permissions

### Task Runs but No Output

**Enable Logging**:

Modify the task action to redirect output:

**Program**: `cmd.exe`
**Arguments**: `/c python main.py > logs\task_output.log 2>&1`
**Start in**: `C:\Users\gn17g\OneDrive\Desktop\automator`

This will capture all output to `logs\task_output.log`.

### Check Task Status

```powershell
# Get task details
Get-ScheduledTask -TaskName "YouTube Shorts Auto-Upload"

# Get last run result
Get-ScheduledTaskInfo -TaskName "YouTube Shorts Auto-Upload"

# View task history (if enabled)
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" | Where-Object {$_.Message -like "*YouTube Shorts*"} | Select-Object -First 10
```

---

## 🔄 Modify Existing Task

### Change Run Time

```powershell
$trigger = New-ScheduledTaskTrigger -Daily -At "10:00AM"
Set-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" -Trigger $trigger
```

### Change to Run Every 12 Hours

```powershell
$trigger1 = New-ScheduledTaskTrigger -Daily -At "09:00AM"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "09:00PM"
Set-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" -Trigger @($trigger1, $trigger2)
```

### Disable Task

```powershell
Disable-ScheduledTask -TaskName "YouTube Shorts Auto-Upload"
```

### Enable Task

```powershell
Enable-ScheduledTask -TaskName "YouTube Shorts Auto-Upload"
```

### Delete Task

```powershell
Unregister-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" -Confirm:$false
```

---

## 📊 Monitoring

### Daily Checks

1. **Check logs**: `logs/daily_report_YYYY-MM-DD.log`
2. **Verify uploads**: YouTube Studio → Content → Scheduled
3. **Monitor quota**: Check log for quota warnings

### Weekly Maintenance

1. Clean old logs (keep last 30 days)
2. Review archived videos
3. Check for failed uploads in logs

### Monthly Review

1. Verify tokens are still valid
2. Check quota usage patterns
3. Review upload success rate

---

## 🎯 Best Practices

### 1. Set Appropriate Run Time

- Choose a time when your computer is typically on
- Avoid peak internet usage times
- Consider your target audience's timezone

### 2. Keep Computer Awake

If using a laptop:
- Adjust power settings to prevent sleep during scheduled time
- Or use "Wake the computer to run this task" option

### 3. Monitor Regularly

- Check logs weekly
- Verify uploads are scheduling correctly
- Watch for quota warnings

### 4. Backup Configuration

Periodically backup:
- `channels_config.json`
- `.env`
- `tokens/` folder (encrypted storage recommended)

---

## 🔐 Security Considerations

### Run as Limited User

For security, consider:
1. Create a dedicated Windows user for automation
2. Grant minimal permissions
3. Run task under that user account

### Protect Tokens

- Keep `tokens/` folder secure
- Don't share or commit to version control
- Use Windows file encryption if needed

---

## 📝 Example Task Export

To export your task configuration:

```powershell
Export-ScheduledTask -TaskName "YouTube Shorts Auto-Upload" | Out-File "task_backup.xml"
```

To import on another computer:

```powershell
Register-ScheduledTask -Xml (Get-Content "task_backup.xml" | Out-String) -TaskName "YouTube Shorts Auto-Upload"
```

---

## 🎉 Success Indicators

Your task is working correctly if:

✅ Task shows "Ready" status in Task Scheduler
✅ "Last Run Time" updates daily
✅ "Last Run Result" shows "The operation completed successfully (0x0)"
✅ New log files appear daily in `logs/`
✅ Videos appear in YouTube Studio as scheduled
✅ Videos move from `queue/` to `archive/`

---

## 📞 Quick Reference

### View Task Status
```powershell
Get-ScheduledTask -TaskName "YouTube Shorts Auto-Upload"
```

### Run Task Manually
```powershell
Start-ScheduledTask -TaskName "YouTube Shorts Auto-Upload"
```

### Check Last Run
```powershell
Get-ScheduledTaskInfo -TaskName "YouTube Shorts Auto-Upload"
```

### View Logs
```powershell
Get-Content "C:\Users\gn17g\OneDrive\Desktop\automator\logs\daily_report_$(Get-Date -Format 'yyyy-MM-dd').log"
```

---

## 🚀 You're All Set!

Your YouTube Shorts automation is now scheduled to run daily. The system will:

1. Wake up at 9:00 AM every day
2. Scan queue folders for new videos
3. Upload and schedule up to 6 Shorts
4. Archive processed videos
5. Generate daily reports

**Just drop videos in the queue folders and let automation handle the rest!** 🎬