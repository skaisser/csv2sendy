import pytest
from csv2sendy.core import CSVProcessor

def test_process_name():
    processor = CSVProcessor()
    
    # Test various name formats
    assert processor.process_name('John Doe') == ('John', 'Doe')
    assert processor.process_name('mary jane wilson') == ('Mary', 'Jane Wilson')
    assert processor.process_name('PETER') == ('Peter', '')
    assert processor.process_name('') == ('', '')
    assert processor.process_name('sem nome') == ('', '')

def test_format_phone_number():
    processor = CSVProcessor()
    
    # Test various phone number formats
    assert processor.format_phone_number('5511999999999') == '+55 (11) 99999-9999'
    assert processor.format_phone_number('11999999999') == '+55 (11) 99999-9999'
    assert processor.format_phone_number('999999999') == ''
    assert processor.format_phone_number('') == ''

def test_validate_email_address():
    processor = CSVProcessor()
    
    # Test various email formats
    assert processor.validate_email_address('test@example.com') == 'test@example.com'
    assert processor.validate_email_address('TEST@EXAMPLE.COM') == 'test@example.com'
    assert processor.validate_email_address('invalid.email') == ''
    assert processor.validate_email_address('') == ''

def test_detect_delimiter():
    processor = CSVProcessor()
    
    # Test delimiter detection
    assert processor.detect_delimiter('a,b,c\n1,2,3') == ','
    assert processor.detect_delimiter('a;b;c\n1;2;3') == ';'
    assert processor.detect_delimiter('a,b;c\n1,2;3') == ';'  # More semicolons than commas

def test_process_file():
    processor = CSVProcessor()
    
    # Test complete file processing
    content = 'Name,Email,Phone\nJohn Doe,john@example.com,5511999999999\n'
    df = processor.process_file(content)
    
    assert 'first_name' in df.columns
    assert 'last_name' in df.columns
    assert 'email' in df.columns
    assert 'phone_number' in df.columns
    
    assert df.iloc[0]['first_name'] == 'John'
    assert df.iloc[0]['last_name'] == 'Doe'
    assert df.iloc[0]['email'] == 'john@example.com'
    assert df.iloc[0]['phone_number'] == '+55 (11) 99999-9999'
