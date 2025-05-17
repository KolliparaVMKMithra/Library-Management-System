from datetime import datetime
import auth
from models import Book, Loan
from storage import CSVStorage
from models import Book, Member, Loan

def search_catalogue(books_storage: CSVStorage[Book]):
    """Search for books by title or author"""
    print("\n=== Search Catalogue ===")
    
    search_term = input("Enter search term (title/author): ").lower()
    
    books = books_storage.read_all()
    results = [
        book for book in books
        if search_term in book.title.lower() or search_term in book.author.lower()
    ]
    
    if not results:
        print("No books found matching your search.")
        return
    
    print(f"\nFound {len(results)} books:")
    print(f"{'ISBN':<15} {'Title':<30} {'Author':<20} {'Available':<10}")
    print("-" * 75)
    
    for book in results:
        availability = f"{book.copies_available}/{book.copies_total}"
        print(f"{book.isbn:<15} {book.title:<30} {book.author:<20} {availability:<10}")

def borrow_book(books_storage: CSVStorage[Book], members_storage: CSVStorage[Member], loans_storage: CSVStorage[Loan]):
    """Member borrows a book"""
    print("\n=== Borrow Book ===")
    
    # Get current member ID from session
    member_id = auth.get_current_user_id()
    if not member_id:
        print("You must be logged in to borrow books.")
        return
    
    isbn = input("Enter ISBN of book to borrow: ")
    book = books_storage.find_by_field("isbn", isbn)
    
    if not book:
        print(f"Book with ISBN {isbn} not found.")
        return
    
    if book.copies_available <= 0:
        print(f"No copies of '{book.title}' are available.")
        return
    
    # Check if member already has this book
    loans = loans_storage.read_all()
    for loan in loans:
        if (loan.member_id == member_id and 
            loan.isbn == isbn and 
            loan.return_date is None):
            print("You already have this book on loan.")
            return
    
    # Generate loan ID
    loan_id = "1"
    if loans:
        loan_id = str(max(int(loan.loan_id) for loan in loans) + 1)
    
    issue_date = datetime.now().strftime("%Y-%m-%d")
    due_date = Loan.calculate_due_date(issue_date)
    
    # Create new loan
    new_loan = Loan(
        loan_id=loan_id,
        member_id=member_id,
        isbn=isbn,
        issue_date=issue_date,
        due_date=due_date
    )
    
    # Update book availability
    book.copies_available -= 1
    books_storage.update(book, "isbn")
    
    # Save loan
    loans_storage.append(new_loan)
    
    print(f"You've borrowed '{book.title}'. Please return by {due_date}.")

def view_loans(loans_storage: CSVStorage[Loan], books_storage: CSVStorage[Book]):
    """View member's loan history"""
    print("\n=== My Loans ===")
    
    # Get current member ID from session
    member_id = auth.get_current_user_id()
    if not member_id:
        print("You must be logged in to view loans.")
        return
    
    loans = loans_storage.read_all()
    member_loans = [loan for loan in loans if loan.member_id == member_id]
    
    if not member_loans:
        print("You have no loan history.")
        return
    
    print(f"{'Book Title':<30} {'Issue Date':<12} {'Due Date':<12} {'Status':<10}")
    print("-" * 64)
    
    for loan in member_loans:
        book = books_storage.find_by_field("isbn", loan.isbn)
        book_title = book.title if book else "Unknown Book"
        
        status = "Returned" if loan.return_date else "Active"
        
        print(f"{book_title:<30} {loan.issue_date:<12} {loan.due_date:<12} {status:<10}")
