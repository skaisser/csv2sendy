"""Setup script for csv2sendy."""
from setuptools import setup, find_packages

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='csv2sendy',
    version='0.1.0',
    description='A powerful CSV processor for Sendy.co with Brazilian data format support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shirleyson Kaisser',
    author_email='skaisser@gmail.com',
    url='https://github.com/skaisser/csv2sendy',
    project_urls={
        "Bug Tracker": "https://github.com/skaisser/csv2sendy/issues",
        "Documentation": "https://csv2sendy.readthedocs.io",
    },
    packages=find_packages(exclude=["tests*"]),
    package_data={
        "csv2sendy": ["py.typed"],
        "csv2sendy.core": ["py.typed"],
        "csv2sendy.web": ["py.typed"],
    },
    python_requires='>=3.9',
    install_requires=[
        'pandas>=1.3.0',
        'email-validator>=1.1.0',
        'flask>=2.0.0',
        'werkzeug>=2.0.0',
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'mypy>=1.13.0',
            'types-all',
        ],
        'docs': [
            'sphinx>=7.0.0',
            'sphinx-rtd-theme>=3.0.0',
            'myst-parser>=3.0.0',
            'furo>=2024.0.0',
        ],
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "isort>=5.0",
            "flake8>=3.9",
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
    ],
    keywords='csv, sendy, email, contacts, brazil',
    entry_points={
        "console_scripts": [
            "csv2sendy=csv2sendy.cli:main",
        ],
    },
)
