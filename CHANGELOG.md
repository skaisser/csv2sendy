# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2024-03-23

### Fixed
- Added missing CLI module for command-line interface
- Fixed command-line entry point

## [1.0.2] - 2024-03-23

### Fixed
- Fixed email validation to handle and remove 'mailto:' prefix from email addresses
- Added comprehensive test coverage for email validation including mailto handling

## [1.0.1] - 2024-03-22

### Fixed
- Fixed email validation to properly handle string conversion and normalization
- Improved file type validation in web interface
- Enhanced error handling with proper JSON responses
- Fixed file encoding detection and handling
- Added better test coverage for edge cases

### Changed
- Updated test suite to use isolated temporary directories
- Improved code organization and error handling
- Enhanced documentation and type hints

## [1.0.0] - 2024-03-21

### Added
- Initial release
- CSV processing with Brazilian data format support
- Web interface for file upload and processing
- Email validation and normalization
- Phone number formatting for Brazilian numbers
- Name splitting into first and last name
- Support for multiple CSV delimiters
- Comprehensive test suite
- Documentation
