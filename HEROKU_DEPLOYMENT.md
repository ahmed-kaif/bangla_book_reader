# 🚀 Bengali PDF to Audiobook - Heroku Deployment Guide

## 📋 Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Make sure you have git installed

## 🛠️ Deployment Steps

### 1. Prepare Your Project

```bash
cd /Volumes/Dev/bangla_book_reader/simple_web_app

# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit: Bengali PDF to Audiobook Web App"
```

### 2. Login to Heroku

```bash
heroku login
```

### 3. Create Heroku App

```bash
# Create a new Heroku app (replace 'your-app-name' with desired name)
heroku create bengali-audiobook-converter

# Or let Heroku generate a random name
heroku create
```

### 4. Set Environment Variables

```bash
# Set secret key for security
heroku config:set SECRET_KEY="your-super-secret-key-here-make-it-long-and-random"

# Optional: Set file size limits
heroku config:set MAX_FILE_SIZE=52428800  # 50MB in bytes
```

### 5. Deploy to Heroku

```bash
# Push to Heroku
git push heroku main

# If your branch is named 'master':
git push heroku master
```

### 6. Open Your App

```bash
# Open the deployed app in browser
heroku open

# Or get the URL
heroku info
```

## 🔧 Configuration Files Explained

### `Procfile`
```
web: gunicorn app:app
```
Tells Heroku to run your Flask app using Gunicorn web server.

### `requirements.txt`
Contains all Python dependencies needed for production.

### `runtime.txt`
```
python-3.9.19
```
Specifies Python version for Heroku to use.

## 🌍 App URLs

After deployment, your app will be available at:
- **Main App**: `https://your-app-name.herokuapp.com`
- **Upload Page**: `https://your-app-name.herokuapp.com/upload`
- **Jobs List**: `https://your-app-name.herokuapp.com/jobs`

## 📊 Monitoring and Logs

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Open Heroku dashboard
heroku addons:open
```

## ⚙️ Important Notes

### 🔒 **Security**
- Change the `SECRET_KEY` to a strong, random value
- Never commit secrets to git

### 💾 **File Storage**
- Heroku has **ephemeral filesystem** - uploaded files are temporary
- Files are deleted when the app restarts (daily)
- For permanent storage, consider adding AWS S3 or similar

### ⏱️ **Performance**
- Free tier sleeps after 30 minutes of inactivity
- First request after sleep takes ~10-30 seconds
- Consider upgrading to Hobby tier ($7/month) for always-on

### 🚀 **Scaling**
```bash
# Scale to multiple dynos (requires paid plan)
heroku ps:scale web=2

# Check current scaling
heroku ps
```

## 🔄 Updates and Maintenance

### Deploy Updates
```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push heroku main
```

### Environment Variables
```bash
# View all config vars
heroku config

# Set new variable
heroku config:set NEW_VAR=value

# Remove variable
heroku config:unset VAR_NAME
```

## 🎯 Production Optimizations

### 1. Add Database (Optional)
For job persistence across restarts:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 2. Add Redis (Optional)
For better job queue management:
```bash
heroku addons:create heroku-redis:hobby-dev
```

### 3. Add File Storage
For permanent file storage:
```bash
# This would require code changes to use AWS S3
heroku addons:create bucketeer:hobby
```

## 🔍 Troubleshooting

### Common Issues

1. **Build Failed**
   ```bash
   heroku logs --tail
   # Check for missing dependencies or Python version issues
   ```

2. **App Crashes**
   ```bash
   heroku restart
   heroku logs --tail
   ```

3. **Memory Issues**
   - Consider upgrading to Standard-1X dyno
   - Optimize PDF processing for large files

4. **Timeout Issues**
   - Heroku has 30-second request timeout
   - Large PDF conversions might timeout
   - Consider implementing async processing

## 📈 Monitoring

### Add New Relic (Optional)
```bash
heroku addons:create newrelic:wayne
```

### Check Performance
```bash
heroku logs --tail | grep "response_time"
```

## 💰 Cost Estimation

- **Free Tier**: 
  - 550-1000 dyno hours/month
  - Sleeps after 30 min inactivity
  - Perfect for testing/demo

- **Hobby ($7/month)**:
  - Always-on
  - Custom domains
  - SSL included

- **Standard-1X ($25/month)**:
  - More memory/CPU
  - Better for heavy PDF processing

Your Bengali audiobook converter should work great on the free tier for personal use! 🎉