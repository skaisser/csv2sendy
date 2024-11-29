Welcome to CSV2Sendy's documentation!
==================================

CSV2Sendy is a powerful CSV processor for Sendy.co with Brazilian data format support.
It helps you process CSV files containing contact information and format them according
to Sendy.co's requirements.

Features
--------

- Brazilian data format support
- Name processing (handles 'sem nome' case)
- Phone number formatting (+55 prefix)
- Email validation and normalization
- Web interface for CSV transformation
- Custom column mapping
- Tag addition
- Duplicate email removal

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   contributing
   changelog

Installation
------------

You can install CSV2Sendy using pip:

.. code-block:: bash

   pip install csv2sendy

Quick Start
----------

Here's a simple example of how to use CSV2Sendy:

.. code-block:: python

   from csv2sendy.core import CSVProcessor

   # Create a processor instance
   processor = CSVProcessor()

   # Process a CSV file
   with open('contacts.csv', 'r') as f:
       content = f.read()
       df = processor.process_file(content)

   # Save the processed file
   df.to_csv('processed_contacts.csv', index=False)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
