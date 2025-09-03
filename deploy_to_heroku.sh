#!/bin/bash
# 🚀 Easy Heroku Deployment Script for Bengali Audiobook Converter

echo "🚀 Bengali PDF to Audiobook - Heroku Deployment"
echo "==============================================="
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the simple_web_app directory."
    exit 1
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed."
    echo "📥 Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    echo "🍺 On macOS: brew install heroku/brew/heroku"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Bengali PDF to Audiobook Web App"
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Create Heroku app
echo ""
echo "📱 Creating Heroku app..."
read -p "Enter your app name (or press Enter for random name): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "🎲 Creating app with random name..."
    heroku create
else
    echo "🏷️ Creating app with name: $APP_NAME"
    heroku create "$APP_NAME"
fi

# Set environment variables
echo ""
echo "⚙️ Setting environment variables..."

# Generate a random secret key
SECRET_KEY=$(openssl rand -hex 32)
heroku config:set SECRET_KEY="$SECRET_KEY"

# Set file size limit (50MB)
heroku config:set MAX_FILE_SIZE=52428800

echo "✅ Environment variables set!"

# Deploy to Heroku
echo ""
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku" --allow-empty
git push heroku main || git push heroku master

# Check deployment status
echo ""
echo "📊 Checking deployment status..."
heroku ps

# Open the app
echo ""
echo "🎉 Deployment complete!"
echo ""
heroku info
echo ""
echo "🌐 Opening your app in the browser..."
heroku open

echo ""
echo "✅ Your Bengali PDF to Audiobook converter is now live!"
echo "📱 You can now share the URL with others to use your app!"
echo ""
echo "🔧 Useful commands:"
echo "   heroku logs --tail    # View logs"
echo "   heroku restart        # Restart app"
echo "   heroku ps             # Check status"
echo "   heroku open           # Open in browser"