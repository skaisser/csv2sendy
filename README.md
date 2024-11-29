# CSV2Sendy

<div align="center">

[![PyPI version](https://badge.fury.io/py/csv2sendy.svg)](https://badge.fury.io/py/csv2sendy)
[![Python Versions](https://img.shields.io/pypi/pyversions/csv2sendy.svg)](https://pypi.org/project/csv2sendy/)
[![Tests](https://github.com/skaisser/csv2sendy/actions/workflows/tests.yml/badge.svg)](https://github.com/skaisser/csv2sendy/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/skaisser/csv2sendy/badge.svg?branch=main)](https://coveralls.io/github/skaisser/csv2sendy?branch=main)
[![Documentation Status](https://readthedocs.org/projects/csv2sendy/badge/?version=latest)](https://csv2sendy.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/csv2sendy)](https://pepy.tech/project/csv2sendy)

A powerful tool for processing CSV files for Sendy.co email imports with special support for Brazilian data formats.

[Documentation](https://csv2sendy.readthedocs.io) |
[PyPI Package](https://pypi.org/project/csv2sendy/) |
[GitHub Repository](https://github.com/skaisser/csv2sendy)

</div>

## 🌟 Features

- 🔄 **Intelligent CSV Processing**
  - Auto-detection of delimiters and encodings
  - Smart column mapping and normalization
  - Robust error handling and reporting

- 📧 **Email Processing**
  - RFC-compliant email validation
  - Duplicate removal
  - Case normalization
  - Domain validation (optional)

- 📱 **Phone Number Handling**
  - Brazilian format support (+55 format)
  - WhatsApp number validation
  - International format conversion
  - Auto-correction of common format issues

- 👤 **Name Processing**
  - Proper capitalization rules
  - First/last name splitting
  - Special character handling
  - Brazilian name format support

- 🌐 **Web Interface**
  - Modern, responsive design
  - Drag-and-drop file upload
  - Real-time validation
  - Progress tracking
  - Column mapping UI

- 🔒 **Security**
  - Secure file handling
  - Automatic file cleanup
  - Input sanitization
  - Rate limiting

## 📦 Installation

### Using pip (Recommended)

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

### Command Line Interface

```bash
# Start the web interface
csv2sendy --port 8080

# Process a file directly
csv2sendy process input.csv -o output.csv

# Show help
csv2sendy --help
```

### Python API

```python
from csv2sendy.core import CSVProcessor

# Basic usage
processor = CSVProcessor()
df = processor.process_file('input.csv')
df.to_csv('output.csv', index=False)

# Advanced usage with options
processor = CSVProcessor(
    encodings=['utf-8-sig', 'latin1'],
    validate_domains=True,
    remove_duplicates=True
)

# Process from string content
content = '''Name,Email,Phone
John Doe,john@example.com,5511999999999'''
df = processor.process_file(content)

# Process from DataFrame
import pandas as pd
df = pd.read_csv('input.csv')
processed_df = processor.process_dataframe(df)
```

### Web Interface

1. Start the server:
   ```bash
   csv2sendy
   ```

2. Open http://localhost:8080 in your browser
3. Upload your CSV file
4. Configure column mapping (or let auto-detection work)
5. Download the processed file

## 📋 Input Format

CSV2Sendy accepts CSV files with the following columns (case-insensitive):

- **Name/Nome**: Full name of the contact
- **Email/E-mail**: Email address
- **Phone/Telefone/WhatsApp**: Phone number

Example input:
```csv
Name,Email,Phone
John Doe,john@example.com,5511999999999
Maria Silva,maria@example.com,11987654321
```

## 📤 Output Format

The tool produces a CSV file formatted for Sendy with the following columns:

- `first_name`: First name of the contact
- `last_name`: Last name of the contact (if available)
- `email`: Validated and normalized email address
- `phone_number`: Formatted phone number (+55 format)

Example output:
```csv
first_name,last_name,email,phone_number
John,Doe,john@example.com,+55 (11) 99999-9999
Maria,Silva,maria@example.com,+55 (11) 98765-4321
```

## 🛠️ Development Setup

1. Clone and install dependencies:
   ```bash
   git clone https://github.com/skaisser/csv2sendy.git
   cd csv2sendy
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run tests:
   ```bash
   pytest
   pytest --cov=csv2sendy  # With coverage
   ```

4. Format code:
   ```bash
   black csv2sendy tests
   isort csv2sendy tests
   ```

## 🤝 Contributing

We love your input! Check out our [Contributing Guide](CONTRIBUTING.md) for guidelines on how to proceed.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔒 Security

Found a security issue? Please email skaisser@gmail.com instead of using the issue tracker.

## 💬 Community & Support

- 📖 [Documentation](https://csv2sendy.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/skaisser/csv2sendy/issues)
- 💡 [Discussions](https://github.com/skaisser/csv2sendy/discussions)
- 📧 [Email Support](mailto:skaisser@gmail.com)

## 🙏 Acknowledgments

- [Sendy.co](https://sendy.co) for their amazing email marketing platform
- All our [contributors](https://github.com/skaisser/csv2sendy/graphs/contributors)
- The open-source community for the amazing tools we build upon

---

<div align="center">
Made with ❤️ by <a href="https://github.com/skaisser">skaisser</a>
</div>
