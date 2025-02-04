from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from pdf_handler import extract_text_from_pdf
from summarizer import Summarizer
import re


app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 16MB limit

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    try:
        # Process PDF file
        file.stream.seek(0)  # Reset file pointer
        text = extract_text_from_pdf(file.stream)
        
        if not text.strip():
            return jsonify({'error': 'No text found in PDF'}), 400

        # Generate summary
        summarizer = Summarizer()
        summary = summarizer.summarize(text)
        
        return jsonify({
            'summary': summary,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)