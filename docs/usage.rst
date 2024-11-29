Usage
=====

Command Line Interface
--------------------

CSV2Sendy provides a web interface for processing CSV files. To start the web server:

.. code-block:: bash

   python -m csv2sendy.web.app

Then open your browser and navigate to http://localhost:8080

The web interface provides:
- File upload with UTF-8 encoding support
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

Navigate to http://localhost:8080 and click "Choose File" to upload your CSV file.
The interface supports files with various encodings, including UTF-8.

2. Map Columns
~~~~~~~~~~~~~

After upload, you'll see a list of columns from your CSV file. For each column:

1. Select the corresponding Sendy field
2. Preview the data to ensure correct mapping
3. Click "Continue" when done

3. Add Tags (Optional)
~~~~~~~~~~~~~~~~~~~~~

You can add tags to your contacts:

1. Enter the tag name (e.g., "Source")
2. Enter the tag value (e.g., "Website")
3. All contacts will receive this tag in Sendy

4. Download
~~~~~~~~~~

Click "Download" to get your processed CSV file. The file will be:

- UTF-8 encoded
- Properly formatted for Sendy
- Include any tags you added
- Have duplicates removed (if specified)

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
