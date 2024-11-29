import os
import pytest
from csv2sendy.web.app import app, TEMP_DIR
import tempfile
import shutil
from io import BytesIO

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
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

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

def test_download_no_data(client):
    """Test download route with no data."""
    response = client.post('/download')
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
