import bcrypt
from typing import Dict, Optional
from models import Member
from storage import CSVStorage

# Global session dictionary to store logged-in users
session: Dict[str, str] = {}

def register_member(storage: CSVStorage[Member], name: str, password: str, email: str, join_date: str) -> Member:
    """Register a new member with password hashing"""
    # Get all members to determine next ID
    members = storage.read_all()
    
    # Generate next member ID
    if members:
        numeric_ids = []
        for member in members:
            if member.member_id.isdigit():
                numeric_ids.append(int(member.member_id))
        
        if numeric_ids:
            last_id = max(numeric_ids)
            member_id = str(last_id + 1)
        else:
            member_id = "1001"  # Start with 1001
    else:
        member_id = "1001"  # Start with 1001
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create new member
    new_member = Member(
        member_id=member_id,
        name=name,
        password_hash=password_hash,
        email=email,
        join_date=join_date
    )
    
    # Save to storage
    storage.append(new_member)
    return new_member

def login(storage: CSVStorage[Member], member_id: str, password: str, role: str) -> bool:
    """Authenticate a user and store in session if successful"""
    member = storage.find_by_field("member_id", member_id)
    
    if not member:
        print("Member ID not found.")
        return False
    
    # Check password
    if bcrypt.checkpw(password.encode('utf-8'), member.password_hash.encode('utf-8')):
        # Store in session
        session["user_id"] = member_id
        session["role"] = role
        session["name"] = member.name
        return True
    else:
        print("Incorrect password.")
        return False

def logout():
    """Clear the session"""
    session.clear()

def is_authenticated() -> bool:
    """Check if a user is logged in"""
    return "user_id" in session

def get_current_user_id() -> Optional[str]:
    """Get the current user ID from session"""
    return session.get("user_id")

def get_current_role() -> Optional[str]:
    """Get the current user role from session"""
    return session.get("role")
