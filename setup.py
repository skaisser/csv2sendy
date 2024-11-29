from setuptools import setup, find_packages

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csv2sendy",
    version="0.1.0",
    author="Shirleyson Kaisser",
    author_email="skaisser@gmail.com",
    description="A powerful CSV processor for Sendy.co with Brazilian format support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skaisser/csv2sendy",
    project_urls={
        "Bug Tracker": "https://github.com/skaisser/csv2sendy/issues",
        "Documentation": "https://csv2sendy.readthedocs.io",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing :: General",
        "Topic :: Office/Business",
    ],
    packages=find_packages(exclude=["tests*"]),
    package_data={
        "csv2sendy": ["py.typed"],
        "csv2sendy.core": ["py.typed"],
        "csv2sendy.web": ["py.typed"],
    },
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "email-validator>=1.1.0",
        "flask>=2.0.0",
        "werkzeug>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "isort>=5.0",
            "flake8>=3.9",
            "pre-commit>=2.15",
            "twine>=3.4",
            "build>=0.7",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "mypy>=1.0.0",
            "coveralls>=3.3.1",
            "pandas-stubs<2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "csv2sendy=csv2sendy.cli:main",
        ],
    },
)
