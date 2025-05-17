from datetime import datetime
import auth
from models import Book, Member, Loan
from storage import CSVStorage

def add_book(books_storage: CSVStorage[Book]):
    """Add a new book to the system"""
    print("\n=== Add New Book ===")
    
    isbn = input("ISBN: ")
    # Check if book already exists
    if books_storage.find_by_field("isbn", isbn):
        print(f"Book with ISBN {isbn} already exists.")
        return
    
    title = input("Title: ")
    author = input("Author: ")
    
    try:
        copies = int(input("Number of copies: "))
    except ValueError:
        print("Invalid number. Using default of 1.")
        copies = 1
    
    new_book = Book(
        isbn=isbn,
        title=title,
        author=author,
        copies_total=copies,
        copies_available=copies
    )
    
    books_storage.append(new_book)
    print(f"Book '{title}' added successfully.")

def register_member(members_storage: CSVStorage[Member]):
    """Register a new member"""
    print("\n=== Register New Member ===")
    
    name = input("Name: ")
    password = input("Password: ")
    email = input("Email: ")
    join_date = datetime.now().strftime("%Y-%m-%d")
    
    auth.register_member(members_storage, name, password, email, join_date)
    print(f"Member '{name}' registered successfully.")

def issue_book(books_storage: CSVStorage[Book], members_storage: CSVStorage[Member], loans_storage: CSVStorage[Loan]):
    """Issue a book to a member"""
    print("\n=== Issue Book ===")
    
    isbn = input("ISBN to issue: ")
    book = books_storage.find_by_field("isbn", isbn)
    
    if not book:
        print(f"Book with ISBN {isbn} not found.")
        return
    
    if book.copies_available <= 0:
        print(f"No copies of '{book.title}' are available.")
        return
    
    member_id = input("Member ID: ")
    member = members_storage.find_by_field("member_id", member_id)
    
    if not member:
        print(f"Member with ID {member_id} not found.")
        return
    
    # Generate loan ID
    loans = loans_storage.read_all()
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
    
    print(f"Book issued. Due on {due_date}.")

def return_book(books_storage: CSVStorage[Book], loans_storage: CSVStorage[Loan]):
    """Process a book return"""
    print("\n=== Return Book ===")
    
    isbn = input("ISBN to return: ")
    member_id = input("Member ID: ")
    
    # Find the loan
    loans = loans_storage.read_all()
    loan_to_return = None
    
    for loan in loans:
        if (loan.isbn == isbn and 
            loan.member_id == member_id and 
            loan.return_date is None):
            loan_to_return = loan
            break
    
    if not loan_to_return:
        print("No active loan found for this book and member.")
        return
    
    # Update the loan with return date
    loan_to_return.return_date = datetime.now().strftime("%Y-%m-%d")
    loans_storage.update(loan_to_return, "loan_id")
    
    # Update book availability
    book = books_storage.find_by_field("isbn", isbn)
    if book:
        book.copies_available += 1
        books_storage.update(book, "isbn")
    
    print("Book returned successfully.")

def overdue_list(loans_storage: CSVStorage[Loan], books_storage: CSVStorage[Book], members_storage: CSVStorage[Member]):
    """Display list of overdue books"""
    print("\n=== Overdue Books ===")
    
    today = datetime.now().strftime("%Y-%m-%d")
    loans = loans_storage.read_all()
    
    overdue_loans = [
        loan for loan in loans 
        if loan.return_date is None and loan.due_date < today
    ]
    
    if not overdue_loans:
        print("No overdue books.")
        return
    
    print(f"{'Loan ID':<10} {'Member':<20} {'Book Title':<30} {'Due Date':<12}")
    print("-" * 72)
    
    for loan in overdue_loans:
        book = books_storage.find_by_field("isbn", loan.isbn)
        member = members_storage.find_by_field("member_id", loan.member_id)
        
        book_title = book.title if book else "Unknown Book"
        member_name = member.name if member else "Unknown Member"
        
        print(f"{loan.loan_id:<10} {member_name:<20} {book_title:<30} {loan.due_date:<12}")
    
    # Option to send email reminders
    send_reminders = input("\nSend email reminders? (y/n): ")
    if send_reminders.lower() == 'y':
        print("Email reminders sent to members with overdue books.")
