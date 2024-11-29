import re
from email_validator import validate_email, EmailNotValidError
import pandas as pd
from io import StringIO
import logging
from typing import List, Optional, Union, Dict, Any, Tuple

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CSVProcessor:
    def __init__(self) -> None:
        self.encodings: List[str] = ['utf-8-sig', 'latin1', 'iso-8859-1', 'cp1252']

    def process_file(self, file_content: str, delimiter: Optional[str] = None) -> pd.DataFrame:
        """Process a CSV file content and return normalized DataFrame.
        
        Args:
            file_content (str): Content of the CSV file
            delimiter (str, optional): CSV delimiter. If None, will be auto-detected
            
        Returns:
            pd.DataFrame: Processed and normalized DataFrame
        """
        if delimiter is None:
            delimiter = self.detect_delimiter(file_content)

        df = pd.read_csv(StringIO(file_content), delimiter=delimiter)
        logger.debug(f"Initial columns: {df.columns.tolist()}")
        return self.process_dataframe(df)
    
    def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process a pandas DataFrame with normalization rules.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            
        Returns:
            pd.DataFrame: Processed and normalized DataFrame
        """
        # Remove rows where all fields are empty
        df = df.dropna(how='all')
        
        # Get column mapping
        column_mapping = self._get_column_mapping(df.columns.tolist())
        
        # Rename columns based on mapping
        df = df.rename(columns=column_mapping)
        
        # Process name column
        if 'name' in df.columns:
            df[['first_name', 'last_name']] = df.apply(
                lambda row: pd.Series(self.process_name(str(row['name']))), axis=1)
            df = df.drop('name', axis=1)
        
        # Process phone column
        if 'phone' in df.columns:
            df['phone_number'] = df['phone'].apply(lambda x: self.format_phone_number(str(x)))
            df = df.drop('phone', axis=1)
        
        # Process email column
        if 'email' in df.columns:
            df['email'] = df['email'].apply(lambda x: self.validate_email_address(str(x)))
            df = df[df['email'] != '']  # Remove rows with invalid emails
        
        # Define final column order
        final_column_order = [
            'first_name', 'last_name', 'email', 'phone_number',
            *[col for col in df.columns if col not in ['first_name', 'last_name', 'email', 'phone_number']]
        ]
        
        # Select only columns that exist in the DataFrame
        final_column_order = [col for col in final_column_order if col in df.columns]
        
        # Create processed DataFrame with desired column order
        processed_df = df[final_column_order]
        
        return processed_df[final_column_order]
    
    @staticmethod
    def detect_delimiter(content: str) -> str:
        """Detect the delimiter used in a CSV content.
        
        Args:
            content (str): CSV content
            
        Returns:
            str: Detected delimiter
        """
        first_line = content.split('\n')[0]
        delimiter = ',' if first_line.count(',') > first_line.count(';') else ';'
        logger.debug(f"Detected delimiter: {delimiter}")
        return delimiter
    
    @staticmethod
    def process_name(name: str) -> Tuple[str, str]:
        """Process a name into first and last name components.
        
        Args:
            name (str): Full name
            
        Returns:
            Tuple[str, str]: First name and last name
        """
        # Remove extra spaces and normalize case
        name = ' '.join(name.split()).lower()
        
        if not name or name == 'sem nome':
            return ('', '')
        
        # Split into parts
        parts = name.split()
        
        # If only one part, use it as first name
        if len(parts) == 1:
            return (parts[0].title(), '')
        
        # Otherwise, first part is first name, rest is last name
        return (parts[0].title(), ' '.join(parts[1:]).title())
    
    @staticmethod
    def format_phone_number(phone: str) -> str:
        """Format a phone number to Brazilian standard.
        
        Args:
            phone (str): Input phone number
            
        Returns:
            str: Formatted phone number or empty string if invalid
        """
        # Remove all non-numeric characters
        numbers = re.sub(r'\D', '', phone)
        
        # Check if empty
        if not numbers:
            return ''
        
        # Remove leading zeros
        numbers = numbers.lstrip('0')
        
        # Check length and add country code if needed
        if len(numbers) == 13 and numbers.startswith('55'):  # Full international format
            numbers = numbers[2:]  # Remove country code
        elif len(numbers) == 12 and numbers.startswith('55'):  # Full international format without 9
            numbers = numbers[2:]  # Remove country code
            
        # Handle different formats
        if len(numbers) == 11:  # Mobile with DDD
            return f'+55 ({numbers[:2]}) {numbers[2:7]}-{numbers[7:]}'
        elif len(numbers) == 10:  # Landline with DDD
            return f'+55 ({numbers[:2]}) {numbers[2:6]}-{numbers[6:]}'
        
        return ''  # Invalid format
    
    @staticmethod
    def validate_email_address(email: str) -> str:
        """Validate and normalize an email address.
        
        Args:
            email (str): Input email address
            
        Returns:
            str: Normalized email address or empty string if invalid
        """
        try:
            if not email:
                return ''
            
            # Clean up and normalize email
            email = email.strip().lower()
            
            # Validate email
            validation = validate_email(email, check_deliverability=False)
            return str(validation.email).lower()  # Ensure lowercase
            
        except EmailNotValidError:
            return ''
    
    @staticmethod
    def _get_column_mapping(columns: List[str]) -> Dict[str, str]:
        """Get mapping of original column names to normalized names.
        
        Args:
            columns (List[str]): List of original column names
            
        Returns:
            Dict[str, str]: Mapping of original to normalized names
        """
        mapping = {}
        
        for col in columns:
            normalized = col.lower().strip()
            
            # Name variations
            if any(name in normalized for name in ['nome', 'name']):
                mapping[col] = 'name'
            
            # Email variations
            elif any(email in normalized for email in ['email', 'e-mail']):
                mapping[col] = 'email'
            
            # Phone variations
            elif any(phone in normalized for phone in ['phone', 'telefone', 'celular', 'tel', 'fone']):
                mapping[col] = 'phone'
            
            # Keep original if no mapping found
            else:
                mapping[col] = col
        
        return mapping
