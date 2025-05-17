from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Book:
    isbn: str
    title: str
    author: str
    copies_total: int
    copies_available: int
    
    @classmethod
    def from_csv_row(cls, row):
        return cls(
            isbn=row[0],
            title=row[1],
            author=row[2],
            copies_total=int(row[3]),
            copies_available=int(row[4])
        )
    
    def to_csv_row(self):
        return [
            self.isbn,
            self.title,
            self.author,
            str(self.copies_total),
            str(self.copies_available)
        ]

@dataclass
class Member:
    member_id: str
    name: str
    password_hash: str
    email: str
    join_date: str
    
    @classmethod
    def from_csv_row(cls, row):
        return cls(
            member_id=row[0],
            name=row[1],
            password_hash=row[2],
            email=row[3],
            join_date=row[4]
        )
    
    def to_csv_row(self):
        return [
            self.member_id,
            self.name,
            self.password_hash,
            self.email,
            self.join_date
        ]

@dataclass
class Loan:
    loan_id: str
    member_id: str
    isbn: str
    issue_date: str
    due_date: str
    return_date: Optional[str] = None
    
    @classmethod
    def from_csv_row(cls, row):
        return cls(
            loan_id=row[0],
            member_id=row[1],
            isbn=row[2],
            issue_date=row[3],
            due_date=row[4],
            return_date=row[5] if len(row) > 5 and row[5] else None
        )
    
    def to_csv_row(self):
        return [
            self.loan_id,
            self.member_id,
            self.isbn,
            self.issue_date,
            self.due_date,
            self.return_date if self.return_date else ""
        ]
    
    @staticmethod
    def calculate_due_date(issue_date, days=14):
        """Calculate due date (default 14 days from issue)"""
        issue_dt = datetime.strptime(issue_date, "%Y-%m-%d")
        due_dt = issue_dt + timedelta(days=days)
        return due_dt.strftime("%Y-%m-%d")
