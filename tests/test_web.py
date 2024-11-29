"""Test web application module."""

import os
import pytest
import tempfile
import shutil
from io import BytesIO
from csv2sendy.web.app import app, TEMP_DIR, cleanup_temp_files


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    # Create a custom temp directory for tests
    test_temp_dir = tempfile.mkdtemp()
    app.config['UPLOAD_FOLDER'] = test_temp_dir

    with app.test_client() as client:
        yield client

    # Clean up after tests
    shutil.rmtree(test_temp_dir)


def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data


def test_upload_no_file(client):
    """Test upload endpoint without file."""
    response = client.post('/upload')
    assert response.status_code == 400
    assert b'No file part' in response.data


def test_upload_empty_file(client):
    """Test upload endpoint with empty file."""
    response = client.post('/upload', data={'file': (None, '')})
    assert response.status_code == 400
    assert b'No selected file' in response.data


def test_upload_invalid_file_type(client):
    """Test upload endpoint with invalid file type."""
    data = {'file': (BytesIO(b'test'), 'test.txt')}
    response = client.post('/upload', data=data)
    assert response.status_code == 400
    assert b'Invalid file type' in response.data


def test_upload_valid_csv(client):
    """Test upload endpoint with valid CSV file."""
    csv_content = 'name,email,phone\nJohn Doe,john@example.com,11999999999'
    data = {'file': (BytesIO(csv_content.encode('utf-8')), 'test.csv')}
    response = client.post('/upload', data=data)
    assert response.status_code == 200
    assert b'File processed successfully' in response.data
    assert b'download_url' in response.data


def test_upload_utf8_encoding(client):
    """Test upload route with UTF-8 encoded CSV."""
    csv_content = 'Name,Email,Phone\nJoão Silva,joao@example.com,5511999999999\n'
    response = client.post('/upload', data={
        'file': (BytesIO(csv_content.encode('utf-8')), 'test.csv')
    })
    assert response.status_code == 200
    assert b'download_url' in response.data
    assert b'File processed successfully' in response.data


def test_upload_invalid_encoding(client):
    """Test upload route with invalid encoding."""
    csv_content = b'Name,Email,Phone\n\xff\xff,test@example.com,5511999999999\n'
    response = client.post('/upload', data={
        'file': (BytesIO(csv_content), 'test.csv')
    })
    assert response.status_code == 500
    assert b'Invalid file encoding' in response.data


def test_download_missing_file(client):
    """Test download endpoint with missing file."""
    response = client.get('/download/nonexistent.csv')
    assert response.status_code == 500


def test_download_valid_file(client):
    """Test download endpoint with valid file."""
    filename = 'test.csv'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'w') as f:
        f.write('test content')
    response = client.get(f'/download/{filename}')
    assert response.status_code == 200
