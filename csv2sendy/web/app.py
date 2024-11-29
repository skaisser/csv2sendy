import os
from typing import Dict, Any, Optional, Union, Tuple, List, cast
from flask import Flask, request, jsonify, send_file, make_response, render_template, Response
import tempfile
import atexit
import shutil
from csv2sendy.core import CSVProcessor
import pandas as pd

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create a temporary directory for file storage
TEMP_DIR = tempfile.mkdtemp()

def cleanup_temp_files() -> None:
    """Clean up temporary files when the application exits."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

atexit.register(cleanup_temp_files)

@app.route('/')
def index() -> str:
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file() -> Union[Response, Tuple[Response, int]]:
    """Handle file upload and processing."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename or not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400

        # Try different encodings
        file_content: Optional[str] = None
        encodings = ['utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                file_content = file.read().decode(encoding)
                file.seek(0)  # Reset file pointer for next iteration if needed
                break
            except UnicodeDecodeError:
                file.seek(0)
                continue
        
        if file_content is None:
            return jsonify({'error': 'Unable to decode file. Please ensure it is properly encoded.'}), 400

        processor = CSVProcessor()
        processed_df = processor.process_file(file_content)

        # Store processed data in a temporary file
        temp_file = os.path.join(TEMP_DIR, 'data.csv')
        processed_df.to_csv(temp_file, index=False)

        # Convert to records for JSON response
        raw_data = processed_df.to_dict('records')
        processed_data: List[Dict[str, Any]] = cast(List[Dict[str, Any]], raw_data)
        processed_headers: List[str] = processed_df.columns.tolist()
        
        response: Response = jsonify({
            'data': processed_data,
            'headers': processed_headers,
        })
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download() -> Union[Response, Tuple[Response, int]]:
    """Handle file download with custom column mapping."""
    try:
        if not request.is_json:
            return jsonify({'error': 'No data found'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data found'}), 400

        temp_file = os.path.join(TEMP_DIR, 'data.csv')
        if not os.path.exists(temp_file):
            return jsonify({'error': 'No data found. Please upload a file first.'}), 400

        # Read the stored CSV
        try:
            df = pd.read_csv(temp_file)
        except Exception as e:
            return jsonify({'error': f'Failed to read data: {str(e)}'}), 500

        columns = data.get('columns', [])
        tag_name = data.get('tagName')
        tag_value = data.get('tagValue')
        remove_duplicates = data.get('removeDuplicates', True)

        # Process the data based on selected columns
        if columns:
            try:
                selected_columns = [col['originalName'] for col in columns]
                df = df[selected_columns]

                # Rename columns based on user input
                rename_dict = {col['originalName']: col['displayName'] for col in columns}
                df = df.rename(columns=rename_dict)
            except KeyError as e:
                return jsonify({'error': f'Invalid column name: {str(e)}'}), 400

        # Add tag column if specified
        if tag_name and tag_value:
            df[tag_name] = tag_value

        # Remove duplicate emails if requested
        if remove_duplicates and columns:
            email_column = next((col['displayName'] for col in columns if col['originalName'] == 'email'), 'Email')
            if email_column in df.columns:
                df = df.drop_duplicates(subset=[email_column], keep='first')

        # Create the CSV content
        output = df.to_csv(index=False, encoding='utf-8')
        
        # Create the response
        response: Response = make_response(output)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=processed_data.csv'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
