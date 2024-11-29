# Contributing to CSV2Sendy

First off, thank you for considering contributing to CSV2Sendy! It's people like you that make CSV2Sendy such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python style guide
* Include tests when adding features
* End files with a newline

## Development Process

1. Fork the repo
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone your fork
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Create a branch:
   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```
5. Make your changes
6. Run tests:
   ```bash
   pytest
   ```

## Testing

We use pytest for our test suite. To run tests:

```bash
pytest
```

## Style Guide

We follow PEP 8 with some modifications. Please install and use:
- black for code formatting
- isort for import sorting
- flake8 for style guide enforcement

## Documentation

We use Google-style docstrings for Python code. Please document all functions, classes, and modules.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
