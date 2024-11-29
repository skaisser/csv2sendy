"""Web application module for CSV2Sendy.

This module provides a Flask-based web interface for processing CSV files for Sendy.co.
It includes routes for file upload, processing, and download with custom column mapping.

Key Features:
    - File upload with multiple encoding support
    - CSV processing with Brazilian data format support
    - Custom column mapping
    - Tag addition
    - Duplicate email removal
"""

import os
import tempfile
from typing import Tuple, Union
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
from csv2sendy.core.processor import CSVProcessor


TEMP_DIR = tempfile.gettempdir()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit
app.config['UPLOAD_FOLDER'] = TEMP_DIR
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'txt'}


def cleanup_temp_files() -> None:
    """Clean up temporary files."""
    for filename in os.listdir(TEMP_DIR):
        if filename.endswith('.csv'):
            os.remove(os.path.join(TEMP_DIR, filename))


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home() -> str:
    """Render home page."""
    return '''
    <html>
        <head>
            <title>CSV2Sendy - Brazilian CSV Processor</title>
        </head>
        <body>
            <h1>CSV2Sendy</h1>
            <form method="post" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload_file() -> Tuple[Response, int]:
    """Handle file upload."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        processor = CSVProcessor()
        df = processor.process_csv(content)

        # Save processed file
        output_filename = 'processed_' + filename
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        df.to_csv(output_path, index=False)

        return jsonify({
            'message': 'File processed successfully',
            'download_url': f'/download/{output_filename}'
        }), 200

    except UnicodeDecodeError:
        return jsonify({'error': 'Invalid file encoding'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_file(filename: str) -> Union[Response, Tuple[Response, int]]:
    """Download processed file."""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            attachment_filename=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
