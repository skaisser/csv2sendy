import os
import pytest
from csv2sendy.web.app import app, TEMP_DIR, cleanup_temp_files
import tempfile
import shutil
from io import BytesIO
from flask import Flask

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    # Ensure temp directory is empty
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)
    with app.test_client() as client:
        yield client
    # Clean up after tests
    cleanup_temp_files()

def test_cleanup_temp_files():
    """Test cleanup of temporary files."""
    # Create a test file in TEMP_DIR
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    test_file = os.path.join(TEMP_DIR, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    
    # Run cleanup
    cleanup_temp_files()
    
    # Verify directory is removed
    assert not os.path.exists(TEMP_DIR)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for file uploads."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data

def test_upload_no_file(client):
    """Test upload route with no file."""
    response = client.post('/upload')
    assert response.status_code == 400
    assert b'No file uploaded' in response.data

def test_upload_empty_filename(client):
    """Test upload route with empty filename."""
    response = client.post('/upload', data={
        'file': (BytesIO(), '')
    })
    assert response.status_code == 400
    assert b'No file selected' in response.data

def test_upload_invalid_extension(client):
    """Test upload route with invalid file extension."""
    response = client.post('/upload', data={
        'file': (BytesIO(b'test'), 'test.txt')
    })
    assert response.status_code == 400
    assert b'Please upload a CSV file' in response.data

def test_upload_valid_csv(client):
    """Test upload route with valid CSV file."""
    csv_content = 'Name,Email,Phone\nJohn Doe,john@example.com,5511999999999\n'
    response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert response.status_code == 200
    assert b'data' in response.data
    assert b'headers' in response.data

def test_upload_utf8_encoding(client):
    """Test upload route with UTF-8 encoded CSV."""
    csv_content = 'Name,Email,Phone\nJoão Silva,joao@example.com,5511999999999\n'
    response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode('utf-8')), 'test.csv')
    })
    assert response.status_code == 200
    assert b'data' in response.data
    assert b'headers' in response.data

def test_upload_invalid_encoding(client):
    """Test upload route with invalid encoding."""
    # Create a CSV file with invalid UTF-8 sequences
    invalid_content = b'Name,Email\n\xFF\xFF,test@example.com'
    response = client.post('/upload', data={
        'file': (BytesIO(invalid_content), 'test.csv')
    })
    assert response.status_code == 400
    assert b'UTF-8' in response.data

def test_download_no_data(client):
    """Test download route with no data."""
    response = client.post('/download')
    assert response.status_code == 400
    assert b'No data found' in response.data

def test_download_no_json(client):
    """Test download route with non-JSON request."""
    response = client.post('/download', data='not json')
    assert response.status_code == 400
    assert b'No data found' in response.data

def test_download_no_file(client):
    """Test download route with no processed file."""
    response = client.post('/download', json={
        'columns': [],
        'tagName': 'tag',
        'tagValue': 'value'
    })
    assert response.status_code == 400
    assert b'No data found' in response.data

def test_download_invalid_columns(client):
    """Test download route with invalid column names."""
    # First upload a file
    csv_content = 'Name,Email,Phone\nJohn Doe,john@example.com,5511999999999\n'
    upload_response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert upload_response.status_code == 200

    # Then try to download with invalid column
    download_response = client.post('/download', json={
        'columns': [
            {'originalName': 'nonexistent', 'displayName': 'Invalid'}
        ]
    })
    assert download_response.status_code == 400
    assert b'Invalid column name' in download_response.data

def test_download_with_tags(client):
    """Test download route with tag addition."""
    # First upload a file
    csv_content = 'Name,Email,Phone\nJohn Doe,john@example.com,5511999999999\n'
    upload_response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert upload_response.status_code == 200

    # Then download with tags
    download_response = client.post('/download', json={
        'columns': [
            {'originalName': 'first_name', 'displayName': 'Name'},
            {'originalName': 'email', 'displayName': 'Email'}
        ],
        'tagName': 'Source',
        'tagValue': 'Test'
    })
    assert download_response.status_code == 200
    response_data = download_response.data.decode()
    assert 'Source' in response_data
    assert 'Test' in response_data

def test_download_remove_duplicates(client):
    """Test download route with duplicate removal."""
    # First upload a file with duplicate emails
    csv_content = '''Name,Email,Phone
John Doe,john@example.com,5511999999999
Jane Doe,john@example.com,5511999999998
'''
    upload_response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert upload_response.status_code == 200

    # Then download with duplicate removal
    download_response = client.post('/download', json={
        'columns': [
            {'originalName': 'first_name', 'displayName': 'Name'},
            {'originalName': 'email', 'displayName': 'Email'}
        ],
        'removeDuplicates': True
    })
    assert download_response.status_code == 200
    response_lines = download_response.data.decode().split('\n')
    # Should only have header and one data line (plus empty line)
    assert len(response_lines) == 3

def test_download_valid_data(client, temp_dir):
    """Test download route with valid data."""
    # First upload a file
    csv_content = 'Name,Email,Phone\nJohn Doe,john@example.com,5511999999999\n'
    upload_response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert upload_response.status_code == 200

    # Then try to download it
    download_response = client.post('/download', json={
        'columns': [
            {'originalName': 'first_name', 'displayName': 'Name'},
            {'originalName': 'email', 'displayName': 'Email'},
            {'originalName': 'phone_number', 'displayName': 'Phone'}
        ],
        'tagName': 'Source',
        'tagValue': 'Test',
        'removeDuplicates': True
    })
    assert download_response.status_code == 200
    assert download_response.headers['Content-Type'] == 'text/csv'
    assert b'Name,Email,Phone,Source' in download_response.data

def test_download_read_error(client):
    """Test download with file read error."""
    # First upload a file
    csv_content = 'Name,Email,Phone\nJohn Doe,john@example.com,5511999999999\n'
    upload_response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert upload_response.status_code == 200
    
    # Remove the temporary file
    temp_file = os.path.join(TEMP_DIR, 'data.csv')
    os.remove(temp_file)
    
    # Try to download
    download_response = client.post('/download', json={
        'columns': [
            {'originalName': 'nonexistent', 'displayName': 'Invalid'}
        ]
    })
    assert download_response.status_code == 400
    assert b'No data found' in download_response.data

def test_download_empty_json(client):
    """Test download with empty JSON data."""
    response = client.post('/download', json={})
    assert response.status_code == 400
    assert b'No data found' in response.data

def test_download_error_handling(client):
    """Test error handling in download endpoint."""
    # Test with invalid JSON
    response = client.post('/download', data='invalid')
    assert response.status_code == 400
    assert b'No data found' in response.data
    
    # Test with empty JSON
    response = client.post('/download', json={})
    assert response.status_code == 400
    assert b'No data found' in response.data
    
    # Test with missing file
    response = client.post('/download', json={'columns': []})
    assert response.status_code == 400
    assert b'No data found' in response.data

def test_upload_file_error(client):
    """Test file upload with server error."""
    # Create a file that will cause an error
    csv_content = 'Name,Email\nJohn Doe,john@example.com\n'
    response = client.post('/upload', data={
        'file': None  # This will cause a bad request error
    })
    
    # Check response
    assert response.status_code == 400
    assert b'No file uploaded' in response.data

def test_download_processing_error(client):
    """Test download with processing error."""
    # First upload a file
    csv_content = 'Name,Email\nJohn Doe,john@example.com\n'
    upload_response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode()), 'test.csv')
    })
    assert upload_response.status_code == 200
    
    # Try to download with invalid column mapping
    download_response = client.post('/download', json={
        'columns': [{'originalName': 'Invalid', 'displayName': 'Invalid'}],
        'tagName': 'Source',
        'tagValue': 'Test'
    })
    assert download_response.status_code == 400
    assert b'error' in download_response.data

def test_main_execution():
    """Test main execution block."""
    # This is just for coverage, as we don't actually run the server
    from csv2sendy.web import app
    assert isinstance(app, Flask)

def test_cleanup_temp_files():
    """Test cleanup of temporary files."""
    # Create temp directory and file
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    test_file = os.path.join(TEMP_DIR, 'test.csv')
    with open(test_file, 'w') as f:
        f.write('test')
    
    # Run cleanup
    cleanup_temp_files()
    
    # Verify directory is removed
    assert not os.path.exists(TEMP_DIR)
