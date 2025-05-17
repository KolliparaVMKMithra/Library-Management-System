from datetime import datetime

def validate_isbn(isbn):
    """Validate ISBN format"""
    # Remove hyphens and spaces
    isbn = isbn.replace('-', '').replace(' ', '')
    
    # ISBN-13 validation (simplified)
    if len(isbn) == 13 and isbn.isdigit():
        return True
    
    # ISBN-10 validation (simplified)
    if len(isbn) == 10 and (isbn[:9].isdigit() and (isbn[9].isdigit() or isbn[9] == 'X')):
        return True
    
    return False

def generate_next_id(current_ids, prefix="", start=1):
    """Generate the next ID in sequence"""
    if not current_ids:
        return f"{prefix}{start}"
    
    # Extract numeric parts
    numeric_ids = []
    for id_str in current_ids:
        if prefix:
            id_str = id_str.replace(prefix, "")
        try:
            numeric_ids.append(int(id_str))
        except ValueError:
            continue
    
    if not numeric_ids:
        return f"{prefix}{start}"
    
    next_id = max(numeric_ids) + 1
    return f"{prefix}{next_id}"
