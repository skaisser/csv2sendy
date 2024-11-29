from csv2sendy.core.processor import CSVProcessor


def test_process_name():
    """Test name processing with various formats."""
    processor = CSVProcessor()
    assert processor.process_name('John Doe') == {'first_name': 'John', 'last_name': 'Doe'}
    assert processor.process_name('mary jane wilson') == {'first_name': 'Mary', 'last_name': 'Jane Wilson'}
    assert processor.process_name('PETER') == {'first_name': 'Peter', 'last_name': ''}
    assert processor.process_name('') == {'first_name': '', 'last_name': ''}
    assert processor.process_name('sem nome') == {'first_name': '', 'last_name': ''}


def test_process_name_empty():
    """Test processing empty name."""
    processor = CSVProcessor()
    result = processor.process_name('')
    assert result == {'first_name': '', 'last_name': ''}


def test_process_name_single():
    """Test processing single name."""
    processor = CSVProcessor()
    result = processor.process_name('John')
    assert result == {'first_name': 'John', 'last_name': ''}


def test_process_name_full():
    """Test processing full name."""
    processor = CSVProcessor()
    result = processor.process_name('John Doe')
    assert result == {'first_name': 'John', 'last_name': 'Doe'}


def test_process_name_multiple():
    """Test processing name with multiple parts."""
    processor = CSVProcessor()
    result = processor.process_name('John Middle Doe')
    assert result == {'first_name': 'John', 'last_name': 'Middle Doe'}


def test_format_phone_empty():
    """Test formatting empty phone number."""
    processor = CSVProcessor()
    result = processor.format_phone_number('')
    assert result == ''


def test_format_phone_invalid():
    """Test formatting invalid phone number."""
    processor = CSVProcessor()
    result = processor.format_phone_number('abc')
    assert result == ''


def test_format_phone_brazilian():
    """Test formatting Brazilian phone number."""
    processor = CSVProcessor()
    test_cases = [
        ('11999999999', '5511999999999'),
        ('11 99999-9999', '5511999999999'),
        ('(11) 99999-9999', '5511999999999'),
        ('55 11 99999-9999', '5511999999999'),
        ('+55 11 99999-9999', '5511999999999'),
    ]
    for input_phone, expected in test_cases:
        assert processor.format_phone_number(input_phone) == expected


def test_detect_delimiter():
    """Test delimiter detection."""
    processor = CSVProcessor()
    assert processor.detect_delimiter('a,b,c') == ','
    assert processor.detect_delimiter('a;b;c') == ';'


def test_process_file():
    """Test CSV file processing."""
    processor = CSVProcessor()
    csv_content = 'Name,Email,Phone\nJohn Doe,john@example.com,11999999999'
    df = processor.process_csv(csv_content)
    assert not df.empty
    assert 'first_name' in df.columns
    assert 'last_name' in df.columns
    assert 'email' in df.columns
    assert 'phone_number' in df.columns
    assert df.iloc[0]['first_name'] == 'John'
    assert df.iloc[0]['last_name'] == 'Doe'
    assert df.iloc[0]['email'] == 'john@example.com'
    assert df.iloc[0]['phone_number'] == '5511999999999'


def test_column_mapping_variations():
    """Test column name mapping with various formats."""
    processor = CSVProcessor()
    csv_content = 'nome,e-mail,telefone\nJohn Doe,john@example.com,11999999999'
    df = processor.process_csv(csv_content)
    assert not df.empty
    assert 'first_name' in df.columns
    assert 'last_name' in df.columns
    assert 'email' in df.columns
    assert 'phone_number' in df.columns


def test_validate_email_address():
    """Test email validation with various formats."""
    processor = CSVProcessor()
    
    # Test valid email addresses
    assert processor.validate_email_address('user@example.com') == 'user@example.com'
    assert processor.validate_email_address('mailto:user@example.com') == 'user@example.com'
    
    # Test invalid email addresses
    assert processor.validate_email_address('') == ''
    assert processor.validate_email_address('invalid-email') == ''
    assert processor.validate_email_address('mailto:invalid-email') == ''
    
    # Test case sensitivity and whitespace
    assert processor.validate_email_address('  mailto:User@Example.COM  ') == 'user@example.com'
    assert processor.validate_email_address('MAILTO:user@example.com') == 'user@example.com'
