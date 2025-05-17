import csv
import os
from typing import List, Dict, Type, TypeVar, Generic, Optional

T = TypeVar('T')

class CSVStorage(Generic[T]):
    def __init__(self, file_path: str, model_class: Type[T]):
        self.file_path = file_path
        self.model_class = model_class
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create the file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as f:
                pass  # Create empty file
    
    def read_all(self) -> List[T]:
        """Read all records from CSV file"""
        records = []
        try:
            with open(self.file_path, 'r', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:  # Skip empty rows
                        records.append(self.model_class.from_csv_row(row))
        except FileNotFoundError:
            pass  # Return empty list if file doesn't exist
        return records
    
    def write_all(self, records: List[T]):
        """Write all records to CSV file"""
        with open(self.file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for record in records:
                writer.writerow(record.to_csv_row())
    
    def append(self, record: T):
        """Append a single record to CSV file"""
        with open(self.file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(record.to_csv_row())
    
    def find_by_field(self, field_name: str, value) -> Optional[T]:
        """Find a record by field value"""
        records = self.read_all()
        for record in records:
            if getattr(record, field_name) == value:
                return record
        return None
    
    def update(self, updated_record: T, id_field: str):
        """Update a record by ID field"""
        records = self.read_all()
        id_value = getattr(updated_record, id_field)
        
        for i, record in enumerate(records):
            if getattr(record, id_field) == id_value:
                records[i] = updated_record
                break
        
        self.write_all(records)
    
    def delete(self, id_field: str, id_value):
        """Delete a record by ID field"""
        records = self.read_all()
        records = [r for r in records if getattr(r, id_field) != id_value]
        self.write_all(records)
