import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from main import analyze_pdf
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB limit

# Initialize Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_pdf_header(file_stream):
    """
    Check if the file starts with %PDF- to verify it's a real PDF.
    Resets the stream position after checking.
    """
    header = file_stream.read(5)
    file_stream.seek(0)
    return header.startswith(b'%PDF-')

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute") # Limit analysis requests
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Strict validation: Check magic numbers
            if not validate_pdf_header(file.stream):
               return render_template('index.html', error="Invalid PDF file. Header signature mismatch/File might be corrupted or renamed.")

            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Get options
            selected_levels = request.form.getlist('levels')
            if not selected_levels:
                selected_levels = ["A1", "A2", "B1", "B2", "C1", "C2"] # Default all if none selected
                
            include_definitions = 'include_definitions' in request.form
            estimate = 'estimate' in request.form
            
            # Generate unique output filename
            timestamp = int(time.time())
            output_filename = f"analyzed_{timestamp}_{filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            # Run analysis
            try:
                # Convert levels from form to uppercase just in case
                levels_set = set([l.upper() for l in selected_levels])
                
                success = analyze_pdf(
                    input_path, 
                    output_path, 
                    levels_set, 
                    include_definitions, 
                    estimate
                )
                
                if success:
                    return render_template('index.html', download_link=output_filename)
                else:
                    return render_template('index.html', error="Analysis failed.")
                    
            except Exception as e:
                return render_template('index.html', error=f"An error occurred: {str(e)}")
                
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('index.html', error="File too large. Maximum size is 16MB."), 413

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('index.html', error=f"Rate limit exceeded: {e.description}"), 429

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
