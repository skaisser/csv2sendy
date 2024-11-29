import os
from flask import Flask, request, jsonify, send_file, make_response, render_template
import tempfile
import atexit
import shutil
from ..core import CSVProcessor

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create a temporary directory for file storage
TEMP_DIR = tempfile.mkdtemp()

# Cleanup function to remove temporary directory on app shutdown
def cleanup_temp_files():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

atexit.register(cleanup_temp_files)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Try different encodings
        processor = CSVProcessor()
        file_content = None
        
        for encoding in processor.encodings:
            try:
                file_content = file.read().decode(encoding)
                file.seek(0)
                break
            except UnicodeDecodeError:
                file.seek(0)
                continue
        
        if file_content is None:
            return jsonify({'error': 'Unable to decode file. Please ensure it is properly encoded.'}), 400
        
        # Process the file
        processed_df = processor.process_file(file_content)
        
        # Store processed data in a temporary file
        temp_file = os.path.join(TEMP_DIR, 'data.csv')
        processed_df.to_csv(temp_file, index=False)
        
        # Convert to records for JSON response
        processed_data = processed_df.to_dict('records')
        processed_headers = processed_df.columns.tolist()
        
        return jsonify({
            'data': processed_data,
            'headers': processed_headers,
            'original_headers': processed_df.columns.tolist()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        temp_file = os.path.join(TEMP_DIR, 'data.csv')
        
        if not os.path.exists(temp_file):
            return jsonify({'error': 'No data found. Please upload a file first.'}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        columns = data.get('columns', [])
        tag_name = data.get('tagName')
        tag_value = data.get('tagValue')
        remove_duplicates = data.get('removeDuplicates', True)
        
        # Read the stored CSV
        import pandas as pd
        df = pd.read_csv(temp_file)
        
        # Process the data based on selected columns
        selected_columns = [col['originalName'] for col in columns]
        df = df[selected_columns]
        
        # Rename columns based on user input
        rename_dict = {col['originalName']: col['displayName'] for col in columns}
        df = df.rename(columns=rename_dict)
        
        # Add tag column if specified
        if tag_name and tag_value:
            df[tag_name] = tag_value
        
        # Remove duplicate emails if requested
        if remove_duplicates:
            email_column = next((col['displayName'] for col in columns if col['originalName'] == 'email'), 'Email')
            if email_column in df.columns:
                df = df.drop_duplicates(subset=[email_column], keep='first')
        
        # Create the CSV content
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        
        # Create the response
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=processed_data.csv'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Entry point for the application."""
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
