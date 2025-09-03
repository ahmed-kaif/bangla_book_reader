#!/bin/bash
echo "🌐 Starting Bengali PDF to Audiobook Web App"
echo "============================================"

cd "$(dirname "$0")"
source web_env/bin/activate

echo "✅ Environment activated"
echo "📱 Starting web server on http://127.0.0.1:5000"
echo "🔄 Upload PDFs and convert them to audiobooks!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
