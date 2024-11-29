"""Command line interface for CSV2Sendy."""

import sys
from flask import Flask
from csv2sendy.web.app import app

def main() -> None:
    """Start the web application."""
    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(f"Starting CSV2Sendy web interface on http://localhost:{port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
