# Google Analytics 4 Integration Setup Guide

## Overview
This guide will help you set up real Google Analytics 4 data in your admin dashboard.

## Step 1: Enable Google Analytics Data API

**Method A - Google Cloud Console (Recommended):**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Analytics Data API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Analytics Data API" or "Analytics Data API"
   - Click "Enable"

**Method B - If you can't find it in Cloud Console:**
1. Go to [Google Developers Console](https://console.developers.google.com/)
2. Select your project or create a new one
3. Go to "Library" and search for "Google Analytics Data API"
4. Enable the API

**Method C - Direct Link:**
1. Go directly to: [Google Analytics Data API](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)
2. Select your project
3. Click "Enable"

**Note:** If you're having trouble finding the API, make sure you have:
- A Google Cloud Project created
- Billing enabled (required for most Google APIs)
- The correct permissions on the project

## Step 2: Create Service Account Credentials

1. In Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - **Name**: `hmd-analytics-service`
   - **Description**: `Service account for HMD website analytics`
4. Skip role assignment for now (click "Done")
5. Click on the created service account
6. Go to the "Keys" tab
7. Click "Add Key" > "Create New Key" > "JSON"
8. Download the JSON file and save it as `google-analytics-credentials.json` in your project root

## Step 3: Grant Analytics Permissions

1. Go to [Google Analytics](https://analytics.google.com/)
2. Select your property
3. Click "Admin" (gear icon)
4. Under "Property", click "Property Access Management"
5. Click the "+" button to add users
6. Add your service account email (found in the JSON file) with **Viewer** permissions

## Step 4: Configure Your Django Project

### Environment Variables
Add these to your environment or create a `.env` file:

```bash
# Your GA4 Property ID (found in GA Admin > Property Settings)
GA4_PROPERTY_ID=123456789

# Path to your credentials file
GA4_CREDENTIALS_FILE=C:/projects/hmd/google-analytics-credentials.json
```

### Find Your Property ID
1. In Google Analytics, go to Admin > Property Settings
2. Copy the "Property ID" (it's a number like `123456789`)

## Step 5: Test the Integration

1. Make sure your credentials file is in the project root
2. Set the environment variables
3. Restart your Django server
4. Go to `/admin/tools/google/` in your admin dashboard
5. You should see real analytics data instead of mock data

## Troubleshooting

### Can't find Google Analytics Data API
- **Try the direct link**: https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com
- **Check if billing is enabled**: Many Google APIs require billing to be set up
- **Verify project permissions**: Make sure you're an owner/editor of the Google Cloud project
- **Try Google Developers Console**: https://console.developers.google.com/
- **Alternative names**: Search for "Analytics Data API" or "GA4" instead

### "Property not found" error
- Double-check your Property ID
- Make sure the service account has Viewer access to the property

### "Credentials not found" error  
- Verify the path to your JSON credentials file
- Make sure the file has proper read permissions

### "No data available"
- Your website might not have enough traffic yet
- Check if Google Analytics is properly installed on your website
- Make sure your property is collecting data

### Still having issues?
- **Option 1**: Use the mock data mode (it looks great and shows the interface)
- **Option 2**: Contact me for help with the specific error messages you're seeing

## Security Notes

- **Never commit your credentials file to Git**
- Add `google-analytics-credentials.json` to your `.gitignore`
- Store credentials securely in production (environment variables or secure vault)
- The service account only has read access to analytics data

## Production Deployment

For production, set these environment variables on your server:

```bash
GA4_PROPERTY_ID=your_property_id
GA4_CREDENTIALS_FILE=/path/to/credentials.json
```

Or use your hosting provider's environment variable system.

---

## Alternative: Quick Setup with Google Analytics Intelligence API

If you're having trouble with the Google Cloud Console, try this simpler approach:

1. **Go to Google Analytics directly**: https://analytics.google.com/
2. **Admin** > **Property** > **API Links** 
3. **Create new project link** or use existing
4. **Download service account key** if available

This might provide an easier path depending on your Google Analytics setup.

---

## Mock Data Mode

If you don't configure Google Analytics, the dashboard will show mock data with a warning message. This allows you to see the interface design while you set up the real integration.

**The dashboard already works perfectly with mock data** - you can use it as-is while figuring out the API setup!