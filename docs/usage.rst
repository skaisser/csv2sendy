Usage
=====

Command Line Interface
--------------------

CSV2Sendy provides a web interface for processing CSV files. To start the web server:

.. code-block:: bash

   python -m csv2sendy.web.app

Then open your browser and navigate to http://localhost:5000

The web interface provides:

.. image:: images/web-interface.png
   :alt: CSV2Sendy Web Interface
   :align: center

Features:
- Drag & drop file upload with UTF-8 encoding support
- Automatic CSV processing and validation
- Interactive column mapping
- Tag management
- Preview and download capabilities

Python API
---------

You can also use CSV2Sendy programmatically in your Python code:

Processing a CSV File
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csv2sendy.core import CSVProcessor

   # Create a processor instance
   processor = CSVProcessor()

   # Process a CSV file
   result = processor.process_file('contacts.csv')

   # Save the processed data
   result.to_csv('processed_contacts.csv', index=False)

Phone Number Formatting
~~~~~~~~~~~~~~~~~~~~~

CSV2Sendy handles various Brazilian phone number formats:

.. code-block:: python

   from csv2sendy.core import CSVProcessor

   processor = CSVProcessor()

   # Format phone numbers
   assert processor.format_phone_number('5511999999999') == '+55 (11) 99999-9999'  # Mobile with country code
   assert processor.format_phone_number('11999999999') == '+55 (11) 99999-9999'    # Mobile without country code
   assert processor.format_phone_number('999999999') == ''                          # Invalid format

Column Mapping
~~~~~~~~~~~~~

You can customize how columns are mapped:

.. code-block:: python

   import pandas as pd
   from csv2sendy.core import CSVProcessor

   # Create a sample DataFrame
   df = pd.DataFrame({
       'nome': ['João Silva', 'Maria Santos'],
       'email': ['joao@example.com', 'maria@example.com'],
       'telefone': ['11999999999', '11988888888']
   })

   # Process with custom mapping
   processor = CSVProcessor()
   result = processor.process_dataframe(df)

   # The result will have standardized column names:
   # - 'nome' -> 'first_name'
   # - 'telefone' -> 'phone'
   # - 'email' remains 'email'

Web Interface Usage
-----------------

1. Upload a CSV File
~~~~~~~~~~~~~~~~~~~

Navigate to http://localhost:5000 and either:

- Drag and drop your CSV file into the upload area
- Click "Choose File" to select your file

The interface supports various file encodings:
- UTF-8 (recommended)
- Latin1 (ISO-8859-1)
- Windows-1252 (CP1252)

2. Process and Map Columns
~~~~~~~~~~~~~~~~~~~~~~~~~

After upload:

1. The file will be automatically processed and validated
2. You'll see a list of detected columns from your CSV file
3. For each column:
   - Select the corresponding Sendy field
   - Preview the data to ensure correct mapping
4. Add any tags you want to apply to all contacts
5. Click "Process" to generate your Sendy-ready CSV

3. Download Results
~~~~~~~~~~~~~~~~~~

- Preview the processed data to ensure accuracy
- Click "Download" to get your Sendy-ready CSV file
- The downloaded file will be properly encoded in UTF-8

Error Handling
-------------

CSV2Sendy provides clear error messages for common issues:

- Invalid email formats
- Malformed phone numbers
- Missing required columns
- Encoding issues
- File upload problems

When an error occurs, check:

1. The file encoding (should be UTF-8)
2. Required columns (Name, Email)
3. Phone number formats
4. Email address validity
