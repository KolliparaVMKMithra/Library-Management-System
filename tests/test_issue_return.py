import os
import sys
import pytest
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Book, Member, Loan
from storage import CSVStorage

# Test data paths
TEST_DATA_DIR = "test_data"
os.makedirs(TEST_DATA_DIR, exist_ok=True)

@pytest.fixture
def setup_test_data():
    """Setup test data and storage"""
    # Create test storage
    books_storage = CSVStorage(os.path.join(TEST_DATA_DIR, "books.csv"), Book)
    members_storage = CSVStorage(os.path.join(TEST_DATA_DIR, "members.csv"), Member)
    loans_storage = CSVStorage(os.path.join(TEST_DATA_DIR, "loans.csv"), Loan)
    
    # Add test book
    test_book = Book(
        isbn="9780132350884",
        title="Clean Code",
        author="Robert C. Martin",
        copies_total=5,
        copies_available=5
    )
    books_storage.write_all([test_book])
    
    # Add test member
    test_member = Member(
        member_id="1001",
        name="Test User",
        password_hash="$2b$12$test_hash",
        email="test@example.com",
        join_date="2025-05-10"
    )
    members_storage.write_all([test_member])
    
    # Clear loans
    loans_storage.write_all([])
    
    return books_storage, members_storage, loans_storage

def test_issue_return(setup_test_data):
    """Test issuing and returning a book"""
    books_storage, members_storage, loans_storage = setup_test_data
    
    # Initial state
    book = books_storage.find_by_field("isbn", "9780132350884")
    assert book.copies_available == 5
    
    # Issue book
    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    
    new_loan = Loan(
        loan_id="1",
        member_id="1001",
        isbn="9780132350884",
        issue_date=issue_date,
        due_date=due_date
    )
    loans_storage.append(new_loan)
    
    # Update book availability
    book.copies_available -= 1
    books_storage.update(book, "isbn")
    
    # Check state after issue
    book = books_storage.find_by_field("isbn", "9780132350884")
    assert book.copies_available == 4
    
    loans = loans_storage.read_all()
    assert len(loans) == 1
    assert loans[0].return_date is None
    
    # Return book
    loans[0].return_date = datetime.now().strftime("%Y-%m-%d")
    loans_storage.update(loans[0], "loan_id")
    
    # Update book availability
    book.copies_available += 1
    books_storage.update(book, "isbn")
    
    # Check state after return
    book = books_storage.find_by_field("isbn", "9780132350884")
    assert book.copies_available == 5
    
    loans = loans_storage.read_all()
    assert loans[0].return_date is not None
