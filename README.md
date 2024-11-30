# CSV2Sendy

<div align="center">

[![PyPI version](https://badge.fury.io/py/csv2sendy.svg)](https://badge.fury.io/py/csv2sendy)
[![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Tests](https://github.com/skaisser/csv2sendy/actions/workflows/tests.yml/badge.svg)](https://github.com/skaisser/csv2sendy/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/skaisser/csv2sendy/badge.svg?branch=main)](https://coveralls.io/github/skaisser/csv2sendy?branch=main)
[![Documentation Status](https://readthedocs.org/projects/csv2sendy/badge/?version=latest)](https://csv2sendy.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

A powerful CSV processor for Sendy.co with Brazilian data format support.

[Documentation](https://csv2sendy.readthedocs.io) |
[GitHub Repository](https://github.com/skaisser/csv2sendy)

</div>

## 🌟 Features

- 🔄 **Intelligent CSV Processing**
  - Auto-detection of delimiters (`,` or `;`)
  - Multiple encoding support (utf-8-sig, latin1, iso-8859-1, cp1252)
  - Smart column mapping and normalization
  - Robust error handling

- 📧 **Email Validation**
  - RFC-compliant email validation
  - Case normalization
  - Duplicate removal
  - Invalid email filtering

- 📱 **Phone Number Processing**
  - Brazilian format support
  - Format standardization
  - Invalid number filtering
  - DDD (area code) validation

- 👤 **Name Processing**
  - First/last name splitting
  - Proper capitalization
  - Special character handling
  - Empty name filtering

- 🔒 **Security**
  - Secure file handling
  - Automatic file cleanup
  - Input sanitization
  - File size limits

## 💻 Web Interface

Transform your CSV files into Sendy.co-ready formats with our intuitive web interface:

![CSV2Sendy Web Interface](docs/images/web-interface.png)

The web interface provides:
- 📤 Drag & drop file upload
- 🔄 Automatic CSV processing
- 📋 Column mapping
- ✨ Data validation and cleaning
- ⬇️ Download processed files

## 📦 Installation

### Using pip

```bash
pip install csv2sendy
```

### From source

```bash
git clone https://github.com/skaisser/csv2sendy.git
cd csv2sendy
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Web Interface

```bash
# Start the web server
python -m csv2sendy.web.app
```

Visit http://localhost:5000 in your browser.

### Command Line Interface (CLI)

```bash
# Start the web server on default port (5000)
csv2sendy

# Start the web server on a specific port
csv2sendy 3000

# Get help
csv2sendy --help
```

The CLI provides a convenient way to start the web interface. By default, it starts the server on port 5000, but you can specify a different port as a command-line argument.

### Python API

```python
from csv2sendy.core import CSVProcessor

# Process a CSV file
processor = CSVProcessor()
df = processor.process_file('input.csv')
df.to_csv('output.csv', index=False)

# Process CSV content directly
content = '''name,email,phone
John Doe,john@example.com,(11) 98765-4321'''
df = processor.process_file(content)
```

## 🔧 Dependencies

Core dependencies (automatically installed):
- Python >=3.9
- pandas >=1.3.0
- email-validator >=1.1.0
- flask >=2.0.0
- werkzeug >=2.0.0

Development dependencies (install with `.[dev]`):
- pytest >=7.0.0
- pytest-cov >=4.0.0
- mypy >=1.13.0
- types-flask >=1.1.0
- types-werkzeug >=1.0.0
- pandas-stubs >=2.0.0

Documentation dependencies (install with `.[docs]`):
- sphinx >=7.0.0

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -e ".[dev,test,doc]"`)
4. Make your changes
5. Run tests and type checking (`pytest` and `mypy csv2sendy`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Shirleyson Kaisser**

- GitHub: [@skaisser](https://github.com/skaisser)
- Email: skaisser@gmail.com
