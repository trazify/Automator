# Google Cloud Project & OAuth Setup Guide

This guide will walk you through setting up a Google Cloud Project, enabling the YouTube Data API v3, and downloading the `client_secret.json` file needed for the YouTube Shorts automation system.

---

## Prerequisites

- A Google account (the same one you'll use to manage your YouTube channels)
- Access to [Google Cloud Console](https://console.cloud.google.com/)

---

## Step 1: Create a Google Cloud Project

1. **Navigate to Google Cloud Console**
   - Open your browser and go to: https://console.cloud.google.com/
   - Sign in with your Google account if prompted

2. **Create a New Project**
   - Click on the project dropdown at the top of the page (next to "Google Cloud")
   - Click **"NEW PROJECT"** button in the top right
   - Enter project details:
     - **Project name**: `YouTube Shorts Automator` (or any name you prefer)
     - **Organization**: Leave as default (No organization)
     - **Location**: Leave as default
   - Click **"CREATE"**
   - Wait for the project to be created (this takes a few seconds)

3. **Select Your New Project**
   - Click on the project dropdown again
   - Select your newly created project from the list

---

## Step 2: Enable YouTube Data API v3

1. **Navigate to APIs & Services**
   - In the left sidebar, click on **"APIs & Services"** → **"Library"**
   - Or use this direct link: https://console.cloud.google.com/apis/library

2. **Search for YouTube Data API**
   - In the search bar, type: `YouTube Data API v3`
   - Click on **"YouTube Data API v3"** from the search results

3. **Enable the API**
   - Click the blue **"ENABLE"** button
   - Wait for the API to be enabled (takes a few seconds)
   - You should see a confirmation message

---

## Step 3: Configure OAuth Consent Screen

Before creating credentials, you need to configure the OAuth consent screen.

1. **Navigate to OAuth Consent Screen**
   - In the left sidebar, click **"APIs & Services"** → **"OAuth consent screen"**
   - Or use this direct link: https://console.cloud.google.com/apis/credentials/consent

2. **Choose User Type**
   - Select **"External"** (this allows you to use any Google account)
   - Click **"CREATE"**

3. **Fill in App Information**
   - **App name**: `YouTube Shorts Automator`
   - **User support email**: Select your email from the dropdown
   - **App logo**: Skip (optional)
   - **App domain**: Skip all fields (optional)
   - **Authorized domains**: Skip (optional)
   - **Developer contact information**: Enter your email address
   - Click **"SAVE AND CONTINUE"**

4. **Scopes**
   - Click **"ADD OR REMOVE SCOPES"**
   - In the filter box, search for: `youtube`
   - Select the following scopes:
     - ✅ `https://www.googleapis.com/auth/youtube.upload`
     - ✅ `https://www.googleapis.com/auth/youtube`
   - Click **"UPDATE"**
   - Click **"SAVE AND CONTINUE"**

5. **Test Users**
   - Click **"ADD USERS"**
   - Enter the email addresses for all three YouTube channels you want to automate
   - Click **"ADD"**
   - Click **"SAVE AND CONTINUE"**

6. **Summary**
   - Review your settings
   - Click **"BACK TO DASHBOARD"**

---

## Step 4: Create OAuth 2.0 Credentials

1. **Navigate to Credentials**
   - In the left sidebar, click **"APIs & Services"** → **"Credentials"**
   - Or use this direct link: https://console.cloud.google.com/apis/credentials

2. **Create OAuth Client ID**
   - Click **"+ CREATE CREDENTIALS"** at the top
   - Select **"OAuth client ID"**

3. **Configure OAuth Client**
   - **Application type**: Select **"Desktop app"**
   - **Name**: `YouTube Shorts Automator Desktop Client`
   - Click **"CREATE"**

4. **Download Credentials**
   - A popup will appear with your Client ID and Client Secret
   - Click **"DOWNLOAD JSON"**
   - Save the file to your computer

5. **Rename the File**
   - The downloaded file will have a long name like `client_secret_123456789.apps.googleusercontent.com.json`
   - **Rename it to**: `client_secret.json`

6. **Move to Project Directory**
   - Move `client_secret.json` to: `C:\Users\gn17g\OneDrive\Desktop\automator\`

---

## Step 5: Verify Setup

After completing the above steps, you should have:

- ✅ A Google Cloud Project created
- ✅ YouTube Data API v3 enabled
- ✅ OAuth consent screen configured
- ✅ `client_secret.json` file in your project directory

---

## Important Notes

> [!WARNING]
> **Keep `client_secret.json` Secure**
> This file contains sensitive credentials. Never share it publicly or commit it to version control (Git).

> [!IMPORTANT]
> **API Quota Limits**
> - Free tier: 10,000 units per day
> - Each video upload costs ~1,600 units
> - Maximum 6 uploads per day with this system
> - Quota resets daily at midnight Pacific Time

> [!NOTE]
> **First-Time Authentication**
> When you run the automation script for the first time, it will open a browser window for each channel asking you to:
> 1. Sign in to the YouTube channel
> 2. Grant permissions to the app
> 3. This only happens once per channel - tokens are saved for future use

---

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Make sure you added your email as a test user in Step 3.5
- Verify that the OAuth consent screen is configured correctly

### "The project does not have access to this API"
- Go back to Step 2 and ensure YouTube Data API v3 is enabled

### "Invalid client_secret.json"
- Make sure you downloaded the file from the correct project
- Verify the file is named exactly `client_secret.json`
- Check that it's in the correct directory

---

## Next Steps

Once you have `client_secret.json` in place:

1. I'll create the automation system code
2. Install Python dependencies
3. Run the first-time authentication for all three channels
4. Start uploading Shorts automatically!

---

**Questions?** Let me know if you encounter any issues during this setup process.
