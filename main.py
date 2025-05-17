import os
from datetime import datetime
from models import Book, Member, Loan
from storage import CSVStorage
from auth import login, logout, is_authenticated, get_current_role
import librarian
import member

# Initialize storage with data paths
DATA_DIR = "data"
books_storage = CSVStorage(os.path.join(DATA_DIR, "books.csv"), Book)
members_storage = CSVStorage(os.path.join(DATA_DIR, "members.csv"), Member)
loans_storage = CSVStorage(os.path.join(DATA_DIR, "loans.csv"), Loan)
# Check if admin account exists, if not create it
admin = members_storage.find_by_field("member_id", "admin")
if not admin:
    import bcrypt
    password = "library123"  # Default password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    admin = Member(
        member_id="admin",
        name="Library Administrator",
        password_hash=password_hash,
        email="admin@library.com",
        join_date=datetime.now().strftime("%Y-%m-%d")
    )
    members_storage.append(admin)
    print("Admin account created with password: library123")

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_login_menu():
    """Display the login menu"""
    clear_screen()
    print("=== Library Management System ===")
    print("1. Login as Librarian")
    print("2. Login as Member")
    print("3. Exit")
    choice = input("> ")
    
    if choice == "1":
        # Librarian login (simplified for demo - would use proper auth in production)
        password = input("Enter librarian password: ")
        if login(members_storage, "admin", password, "librarian"):
            librarian_menu()
        else:
            input("Login failed. Press Enter to continue...")
            display_login_menu()
    
    elif choice == "2":
        # Member login
        member_id = input("Enter Member ID: ")
        password = input("Enter Password: ")
        if login(members_storage, member_id, password, "member"):
            member_menu()
        else:
            input("Login failed. Press Enter to continue...")
            display_login_menu()
    
    elif choice == "3":
        print("Goodbye!")
        exit(0)
    
    else:
        print("Invalid choice.")
        input("Press Enter to continue...")
        display_login_menu()

def librarian_menu():
    """Display the librarian menu"""
    while is_authenticated() and get_current_role() == "librarian":
        clear_screen()
        print("=== Librarian Dashboard ===")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Overdue List")
        print("6. Logout")
        
        choice = input("> ")
        
        if choice == "1":
            librarian.add_book(books_storage)
        elif choice == "2":
            librarian.register_member(members_storage)
        elif choice == "3":
            librarian.issue_book(books_storage, members_storage, loans_storage)
        elif choice == "4":
            librarian.return_book(books_storage, loans_storage)
        elif choice == "5":
            librarian.overdue_list(loans_storage, books_storage, members_storage)
        elif choice == "6":
            logout()
            break
        else:
            print("Invalid choice.")
        
        input("Press Enter to continue...")

def member_menu():
    """Display the member menu"""
    while is_authenticated() and get_current_role() == "member":
        clear_screen()
        print("=== Member Dashboard ===")
        print("1. Search Catalogue")
        print("2. Borrow Book")
        print("3. My Loans")
        print("4. Logout")
        
        choice = input("> ")
        
        if choice == "1":
            member.search_catalogue(books_storage)
        elif choice == "2":
            member.borrow_book(books_storage, members_storage, loans_storage)
        elif choice == "3":
            member.view_loans(loans_storage, books_storage)
        elif choice == "4":
            logout()
            break
        else:
            print("Invalid choice.")
        
        input("Press Enter to continue...")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Start the application
    display_login_menu()
