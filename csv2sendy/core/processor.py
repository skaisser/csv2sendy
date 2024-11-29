import re
from email_validator import validate_email, EmailNotValidError
import pandas as pd
from io import StringIO
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CSVProcessor:
    def __init__(self):
        self.encodings = ['utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']

    def process_file(self, file_content, delimiter=None):
        """Process a CSV file content and return normalized DataFrame.
        
        Args:
            file_content (str): Content of the CSV file
            delimiter (str, optional): CSV delimiter. If None, will be auto-detected
            
        Returns:
            pandas.DataFrame: Processed and normalized data
        """
        if delimiter is None:
            delimiter = self.detect_delimiter(file_content)
        
        logger.debug(f"Reading CSV with delimiter: {delimiter}")
        df = pd.read_csv(StringIO(file_content), delimiter=delimiter)
        logger.debug(f"Initial columns: {df.columns.tolist()}")
        return self.process_dataframe(df)
    
    def process_dataframe(self, df):
        """Process a pandas DataFrame with normalization rules.
        
        Args:
            df (pandas.DataFrame): Input DataFrame
            
        Returns:
            pandas.DataFrame: Processed and normalized DataFrame
        """
        # Remove rows where all fields are empty
        df = df.dropna(how='all')
        
        # Normalize column names
        column_mapping = self._get_column_mapping(df.columns)
        logger.debug(f"Column mapping: {column_mapping}")
        processed_df = df.rename(columns=column_mapping)
        logger.debug(f"After renaming columns: {processed_df.columns.tolist()}")
        
        # Process name fields
        if 'name' in processed_df.columns:
            logger.debug("Processing name field")
            names_processed = processed_df['name'].apply(self.process_name)
            processed_df['first_name'] = [x[0] for x in names_processed]
            processed_df['last_name'] = [x[1] for x in names_processed]
            processed_df.drop('name', axis=1, inplace=True)
        
        # Process phone numbers
        if 'phone_number' in processed_df.columns:
            logger.debug("Processing phone numbers")
            processed_df['phone_number'] = processed_df['phone_number'].apply(self.format_phone_number)
        
        # Process emails
        if 'email' in processed_df.columns:
            logger.debug("Processing emails")
            processed_df['email'] = processed_df['email'].apply(self.validate_email_address)
            # Remove rows with invalid emails
            processed_df = processed_df[processed_df['email'].astype(str).str.len() > 0]
            logger.debug(f"After email validation, rows: {len(processed_df)}")
        
        # Clean up
        processed_df = processed_df.fillna('')
        
        # Reorder columns
        preferred_order = ['first_name', 'email', 'phone_number', 'last_name']
        available_columns = [col for col in preferred_order if col in processed_df.columns]
        other_columns = [col for col in processed_df.columns if col not in preferred_order]
        final_column_order = available_columns + other_columns
        
        logger.debug(f"Final columns: {final_column_order}")
        logger.debug(f"Final DataFrame:\n{processed_df}")
        return processed_df[final_column_order]
    
    @staticmethod
    def detect_delimiter(content):
        """Detect the delimiter used in a CSV content.
        
        Args:
            content (str): CSV content
            
        Returns:
            str: Detected delimiter
        """
        first_line = content.split('\n')[0]
        semicolons = first_line.count(';')
        commas = first_line.count(',')
        delimiter = ';' if semicolons >= commas else ','
        logger.debug(f"Detected delimiter: {delimiter} (semicolons: {semicolons}, commas: {commas})")
        return delimiter
    
    @staticmethod
    def process_name(name):
        """Process a name into first and last name components.
        
        Args:
            name (str): Full name
            
        Returns:
            tuple: (first_name, last_name)
        """
        if pd.isna(name) or str(name).lower().strip() == 'sem nome':
            return ('', '')
            
        parts = str(name).strip().split()
        if len(parts) == 0:
            return ('', '')
        elif len(parts) == 1:
            return (parts[0].title(), '')
        else:
            return (parts[0].title(), ' '.join(parts[1:]).title())
    
    @staticmethod
    def format_phone_number(phone):
        """Format a phone number to Brazilian standard.
        
        Args:
            phone (str): Input phone number
            
        Returns:
            str: Formatted phone number
        """
        if pd.isna(phone):
            return ''
            
        # Remove non-numeric characters
        numbers = re.sub(r'\D', '', str(phone))
        
        # Handle empty or invalid
        if len(numbers) < 8:
            return ''
            
        # Add country code if missing
        if len(numbers) < 12 and len(numbers) >= 10:
            numbers = '55' + numbers
            
        # Format to standard
        if len(numbers) == 13 and numbers.startswith('55'):
            return f'+{numbers[:2]} ({numbers[2:4]}) {numbers[4:9]}-{numbers[9:]}'
            
        return ''
    
    @staticmethod
    def validate_email_address(email):
        """Validate and normalize an email address.
        
        Args:
            email (str): Input email address
            
        Returns:
            str: Normalized email address or empty string if invalid
        """
        if pd.isna(email):
            return ''
        
        email_str = str(email).strip()
        if not email_str:
            return ''
        
        try:
            # Normalize email to lowercase before validation
            email_str = email_str.lower()
            valid = validate_email(email_str, check_deliverability=False)
            return valid.normalized
        except EmailNotValidError:
            return ''
    
    @staticmethod
    def _get_column_mapping(columns):
        """Get mapping of original column names to normalized names.
        
        Args:
            columns (list): List of original column names
            
        Returns:
            dict: Mapping of original to normalized names
        """
        mapping = {}
        for col in columns:
            col_lower = str(col).lower().strip()
            if any(name in col_lower for name in ['name', 'nome']):
                mapping[col] = 'name'
            elif any(email in col_lower for email in ['email', 'e-mail', 'e_mail']):
                mapping[col] = 'email'
            elif any(phone in col_lower for phone in ['phone', 'telefone', 'whatsapp']):
                mapping[col] = 'phone_number'
        return mapping
