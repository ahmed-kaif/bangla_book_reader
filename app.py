import os
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, session
import uuid
import threading
import tempfile
from pathlib import Path
import fitz  # PyMuPDF
from gtts import gTTS
import time
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Configuration for production
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
AUDIO_FOLDER = os.environ.get('AUDIO_FOLDER', 'audio')
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 50 * 1024 * 1024))  # 50MB

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# In-memory job storage (in production, use a database)
jobs = {}

class ConversionJob:
    def __init__(self, job_id, filename, filepath):
        self.id = job_id
        self.filename = filename
        self.filepath = filepath
        self.status = 'pending'  # pending, processing, completed, failed
        self.progress = 0
        self.audio_path = None
        self.error_message = None
        self.created_at = time.time()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def process_pdf_to_audio(job_id):
    """Background processing function"""
    try:
        job = jobs[job_id]
        job.status = 'processing'
        job.progress = 10
        
        # Extract text from PDF
        doc = fitz.open(job.filepath)
        text = ""
        total_pages = len(doc)
        
        for i, page in enumerate(doc):
            page_text = page.get_text()
            text += page_text + "\n\n"
            job.progress = 10 + int((i / total_pages) * 40)
        
        doc.close()
        
        if not text.strip():
            raise ValueError("No text found in PDF")
        
        job.progress = 50
        
        # Limit text for demo (gTTS has limits)
        text = text[:5000] if len(text) > 5000 else text
        
        # Convert to audio using gTTS
        audio_filename = f"{Path(job.filename).stem}_{job.id}.mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
        
        tts = gTTS(text=text, lang='bn', slow=False)
        tts.save(audio_path)
        
        job.audio_path = audio_path
        job.status = 'completed'
        job.progress = 100
        
    except Exception as e:
        job = jobs[job_id]
        job.status = 'failed'
        job.error_message = str(e)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return render_template('upload.html', error='Please select a valid PDF file')
        
        if len(file.read()) > MAX_FILE_SIZE:
            return render_template('upload.html', error='File size exceeds 50MB limit')
        file.seek(0)  # Reset file pointer
        
        # Save file
        job_id = str(uuid.uuid4())
        filename = f"{job_id}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Create job
        job = ConversionJob(job_id, file.filename, filepath)
        jobs[job_id] = job
        
        # Start processing in background
        thread = threading.Thread(target=process_pdf_to_audio, args=(job_id,))
        thread.daemon = True
        thread.start()
        
        return redirect(url_for('job_status', job_id=job_id))
    
    return render_template('upload.html')

@app.route('/job/<job_id>')
def job_status(job_id):
    if job_id not in jobs:
        return "Job not found", 404
    
    job = jobs[job_id]
    return render_template('status.html', job=job)
    
#### [NEW] Added code to solve timestamp issue in job_list.html template
@app.template_filter("timestamp_to_date")
def timestamp_to_date_filter(value):
    """Convert UNIX timestamp (int/float) into a human-readable date."""
    try:
        return datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return value

@app.route('/api/job/<job_id>/progress')
def job_progress(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'completed': job.status == 'completed',
        'failed': job.status == 'failed',
        'error_message': job.error_message
    })

@app.route('/download/<job_id>')
def download_audio(job_id):
    if job_id not in jobs:
        return "Job not found", 404
    
    job = jobs[job_id]
    if job.status != 'completed' or not job.audio_path:
        return "Audio not available", 404
    
    return send_file(job.audio_path, as_attachment=True, 
                    download_name=f"{Path(job.filename).stem}.mp3")

@app.route('/jobs')
def job_list():
    user_jobs = list(jobs.values())
    user_jobs.sort(key=lambda x: x.created_at, reverse=True)
    return render_template('job_list.html', jobs=user_jobs)

if __name__ == '__main__':
    # For local development
    print("🌐 Bengali PDF to Audiobook Web App")
    print("==================================")
    print("📱 Open your browser to: http://127.0.0.1:5000")
    print("🔄 Upload PDFs and convert them to audiobooks!")
    print("⏹️  Press Ctrl+C to stop")
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
