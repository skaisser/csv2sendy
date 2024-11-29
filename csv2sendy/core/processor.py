"""Process CSV files for Sendy compatibility."""

import re
from typing import Dict, Optional, Any
import pandas as pd
from io import StringIO
from email_validator import validate_email, EmailNotValidError


class CSVProcessor:
    """Process CSV files for Sendy compatibility."""

    def __init__(self) -> None:
        """Initialize CSVProcessor."""
        self.column_mapping = {
            'nome': 'name',
            'email': 'email',
            'telefone': 'phone',
            'celular': 'phone',
            'telefone celular': 'phone',
            'phone': 'phone',
            'name': 'name',
            'e-mail': 'email'
        }

    def process_name(self, name: Optional[str]) -> Dict[str, str]:
        """Process a name into first and last name components."""
        if not name or name.lower() == 'sem nome':
            return {'first_name': '', 'last_name': ''}
        name = ' '.join(word.capitalize() for word in name.split())
        parts = name.split()
        if len(parts) == 1:
            return {'first_name': parts[0], 'last_name': ''}
        else:
            return {'first_name': parts[0], 'last_name': ' '.join(parts[1:])}

    def format_phone_number(self, phone: Optional[Any]) -> str:
        """Format phone number to Brazilian format."""
        if not phone:
            return ''

        # Convert to string if not already
        phone = str(phone)

        # Remove all non-numeric characters
        numbers = re.sub(r'\D', '', phone)

        # Check if it's a valid Brazilian number
        if len(numbers) < 10 or len(numbers) > 13:
            return ''

        # Add country code if not present
        if len(numbers) == 10 or len(numbers) == 11:
            numbers = '55' + numbers

        # Check if it starts with valid country code
        if not numbers.startswith('55'):
            return ''

        return numbers

    def validate_email_address(self, email: Optional[Any]) -> str:
        """Validate email address format."""
        if not email:
            return ''

        # Convert to string if not already
        email = str(email).strip().lower()
        # Remove mailto: prefix if present
        if email.startswith('mailto:'):
            email = email[7:]  # len('mailto:') == 7

        try:
            valid = validate_email(email, check_deliverability=False)
            return valid.email
        except EmailNotValidError:
            return ''

    def detect_delimiter(self, content: str) -> str:
        """Detect CSV delimiter."""
        delimiters = [',', ';']
        counts = {d: content.count(d) for d in delimiters}
        return max(counts.items(), key=lambda x: x[1])[0]

    def _get_column_mapping(self, columns: pd.Index) -> Dict[str, str]:
        """Get column mapping for standardization."""
        mapping = {}
        for col in columns:
            col_lower = col.lower()
            if col_lower in self.column_mapping:
                mapping[col] = self.column_mapping[col_lower]
            else:
                mapping[col] = col
        return mapping

    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names."""
        mapping = self._get_column_mapping(df.columns)
        return df.rename(columns=mapping)

    def _process_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process names in the dataframe."""
        if 'name' not in df.columns:
            return df
        names_processed = df['name'].apply(self.process_name)
        df['first_name'] = names_processed.apply(lambda x: x['first_name'])
        df['last_name'] = names_processed.apply(lambda x: x['last_name'])
        df = df.drop('name', axis=1)
        return df

    def _process_emails(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process emails in the dataframe."""
        if 'email' not in df.columns:
            return df
        df['email'] = df['email'].astype(str).apply(self.validate_email_address)
        return df

    def _process_phones(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process phone numbers in the dataframe."""
        if 'phone' not in df.columns:
            return df
        df['phone_number'] = df['phone'].astype(str).apply(self.format_phone_number)
        df = df.drop('phone', axis=1)
        return df

    def process_csv(self, content: str) -> pd.DataFrame:
        """Process CSV content."""
        delimiter = self.detect_delimiter(content)
        df = pd.read_csv(StringIO(content), delimiter=delimiter)
        df = self._standardize_columns(df)
        df = self._process_names(df)
        df = self._process_emails(df)
        df = self._process_phones(df)
        return df

    def process_file(self, file_content: str) -> pd.DataFrame:
        """Process a CSV file."""
        try:
            return self.process_csv(file_content)
        except Exception as e:
            raise ValueError(f"Error processing CSV file: {str(e)}")
