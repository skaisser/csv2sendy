Usage
=====

Command Line Interface
--------------------

CSV2Sendy provides a web interface for processing CSV files. To start the web server:

.. code-block:: bash

   python -m csv2sendy.web.app

Then open your browser and navigate to http://localhost:8080

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
   with open('contacts.csv', 'r') as f:
       content = f.read()
       df = processor.process_file(content)

   # Save the processed file
   df.to_csv('processed_contacts.csv', index=False)

Processing Names
~~~~~~~~~~~~~~

.. code-block:: python

   from csv2sendy.core import CSVProcessor

   processor = CSVProcessor()

   # Process a name
   first_name = processor.process_name('John Doe')  # Returns 'John'
   empty_name = processor.process_name('sem nome')  # Returns ''

Formatting Phone Numbers
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csv2sendy.core import CSVProcessor

   processor = CSVProcessor()

   # Format a phone number
   phone = processor.format_phone_number('11999999999')
   # Returns '+55 (11) 99999-9999'

   phone = processor.format_phone_number('5511999999999')
   # Returns '+55 (11) 99999-9999'

Validating Email Addresses
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from csv2sendy.core import CSVProcessor

   processor = CSVProcessor()

   # Validate and normalize an email address
   email = processor.validate_email_address('John@Example.com')
   # Returns 'john@example.com'

   invalid = processor.validate_email_address('invalid')
   # Returns ''
