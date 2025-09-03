# 🚀 Bengali PDF to Audiobook - Vercel Deployment Guide

## ⚠️ Important Limitations on Vercel

**Vercel has limitations for this type of application:**
- **10-second timeout** on free tier (30s on Pro)
- **No persistent file storage**
- **Limited memory** for PDF processing
- **Not ideal for file upload/processing apps**

**Recommendation: Use Heroku for this project instead.**

## 📋 Prerequisites (If you still want to try Vercel)

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **GitHub Account**: For easy deployment

## 🛠️ Deployment Steps

### Method 1: GitHub Integration (Recommended)

1. **Push to GitHub**
   ```bash
   cd /Volumes/Dev/bangla_book_reader/simple_web_app
   
   # Initialize git if not done
   git init
   git add .
   git commit -m "Initial commit"
   
   # Create GitHub repo and push
   git remote add origin https://github.com/yourusername/bengali-audiobook.git
   git push -u origin main
   ```

2. **Deploy via Vercel Dashboard**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Import Project"
   - Select your GitHub repository
   - Vercel will automatically detect it's a Python project
   - Click "Deploy"

### Method 2: CLI Deployment

```bash
cd /Volumes/Dev/bangla_book_reader/simple_web_app

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# ? Set up and deploy "~/simple_web_app"? [Y/n] y
# ? Which scope do you want to deploy to? Your account
# ? Link to existing project? [y/N] n
# ? What's your project's name? bengali-audiobook-converter
# ? In which directory is your code located? ./
```

## 📁 Required Files for Vercel

### `vercel.json` (Already created)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "functions": {
    "app.py": {
      "maxDuration": 60
    }
  }
}
```

### Modified `app.py` for Vercel
You need to modify your Flask app for Vercel compatibility:

```python
# Add this at the end of app.py for Vercel
# Export the Flask app for Vercel
if __name__ != '__main__':
    # This is for Vercel serverless
    import atexit
    atexit.register(lambda: None)
```

## 🚨 Critical Limitations on Vercel

### 1. **Function Timeout**
- **Free**: 10 seconds maximum
- **Pro**: 60 seconds maximum
- **Problem**: PDF processing + TTS can take minutes

### 2. **No Persistent Storage**
- Files uploaded are lost between requests
- No way to store generated audio files
- Each function execution is isolated

### 3. **Memory Limits**
- Limited memory for PDF processing
- Large PDFs may cause out-of-memory errors

### 4. **Cold Starts**
- Functions sleep when not used
- First request after sleep is slow

## 🔧 Workarounds (Not Recommended)

If you insist on using Vercel, you'd need to:

1. **Implement External Storage**
   ```python
   # Use AWS S3, Google Cloud Storage, or similar
   import boto3
   # Store files in cloud storage instead of local filesystem
   ```

2. **Use Background Jobs**
   ```python
   # Use services like:
   # - Celery + Redis
   # - AWS SQS
   # - Google Cloud Tasks
   ```

3. **Streaming Processing**
   ```python
   # Process PDFs in smaller chunks
   # Stream audio generation
   ```

## 🎯 Better Alternatives for This Project

### **Option 1: Heroku (Recommended)**
- ✅ File uploads work perfectly
- ✅ Longer request timeouts
- ✅ Persistent storage options
- ✅ Better for processing-heavy apps

### **Option 2: Railway**
- ✅ Similar to Heroku but newer
- ✅ Good for Python apps
- ✅ Reasonable pricing

### **Option 3: DigitalOcean App Platform**
- ✅ Good performance
- ✅ Predictable pricing
- ✅ Good for file processing

### **Option 4: Render**
- ✅ Good Heroku alternative
- ✅ Free tier available
- ✅ Good for Python apps

## 💡 Recommendation

**For your Bengali PDF to Audiobook converter, stick with Heroku deployment. Vercel is excellent for static sites and simple APIs, but your app needs:**

- File upload/processing capabilities
- Longer execution times
- Persistent storage
- Better memory allocation

These are all better supported on Heroku! 🚀

## 🔄 If You Still Want to Try Vercel

Despite the limitations, here's what would work:

1. **Text-only conversion** (no file uploads)
2. **Very short text snippets**
3. **External storage integration**
4. **Async processing with webhooks**

But honestly, **Heroku is the way to go** for this project! 💪