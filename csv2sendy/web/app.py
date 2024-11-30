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
import time
import json
from typing import Tuple, Union, cast
from flask import Flask, request, send_file, jsonify, render_template, Response, url_for
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response as WerkzeugResponse
from csv2sendy.core.processor import CSVProcessor
import pandas as pd


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
    return render_template('index.html')


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
        app.logger.info(f'File saved to {filepath}')

        # Process the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        processor = CSVProcessor()
        df = processor.process_csv(content)

        # Convert DataFrame to dictionary, replacing NaN with empty string
        df = df.fillna('')
        data = df.to_dict('records')
        headers = df.columns.tolist()
        app.logger.info(f'Processed headers: {headers}')

        # Save processed file with timestamp to avoid conflicts
        timestamp = int(time.time())
        output_filename = f'processed_{timestamp}_{filename}'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        df.to_csv(output_path, index=False)
        app.logger.info(f'Processed file saved to {output_path}')

        download_url = url_for('download_file', filename=output_filename)
        app.logger.info(f'Download URL: {download_url}')

        return jsonify({
            'message': 'File processed successfully',
            'download_url': download_url,
            'data': data,
            'headers': headers
        }), 200

    except UnicodeDecodeError:
        app.logger.error('Invalid file encoding')
        return jsonify({'error': 'Invalid file encoding'}), 500
    except Exception as e:
        app.logger.error(f'Error processing file: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['POST'])
def download_file() -> Union[Response, Tuple[Response, int]]:
    """Download processed file with column configuration."""
    try:
        app.logger.info('Processing download request')
        
        # Get request data
        columns = request.form.get('columns')
        if not columns:
            return jsonify({'error': 'No column configuration provided'}), 400
            
        columns = json.loads(columns)
        tag = request.form.get('tag', '')
        remove_duplicates = request.form.get('remove_duplicates', 'false').lower() == 'true'
        remove_empty = request.form.get('remove_empty', 'false').lower() == 'true'
        
        # Find the most recent uploaded file
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) 
                if f.endswith('.csv')]
        if not files:
            return jsonify({'error': 'No uploaded file found'}), 404
            
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], latest_file)
        
        # Create output filename
        timestamp = int(time.time())
        output_filename = f'processed_{timestamp}.csv'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Read and process the file
        df = pd.read_csv(input_path)
        
        # Apply filters
        if remove_duplicates:
            original_len = len(df)
            df = df.drop_duplicates(subset=['email'], keep='first')
            app.logger.info(f'Removed {original_len - len(df)} duplicate emails')
            
        if remove_empty:
            original_len = len(df)
            df = df.dropna(subset=['email'])
            app.logger.info(f'Removed {original_len - len(df)} empty emails')
            
        # Add tag if provided
        if tag:
            df['tag'] = tag
            
        # Reorder and filter columns
        column_order = [col['originalName'] for col in columns]
        df = df[column_order]
        
        # Save to temporary file
        df.to_csv(output_path, index=False)
        
        # Send file
        response = send_file(
            output_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='processed.csv'
        )
        
        # Add headers to force download
        response.headers['Content-Disposition'] = 'attachment; filename="processed.csv"'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        app.logger.info('File processed and ready for download')
        return response
        
    except Exception as e:
        app.logger.error(f'Error processing download request: {str(e)}')
        return jsonify({'error': str(e)}), 500


@app.after_request
def add_header(response: Response) -> Response:
    """Add headers to prevent caching."""
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.run(debug=True)
