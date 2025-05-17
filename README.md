# Library-Management-System

Overview
A comprehensive Library Management System built with Python that uses CSV files as a mini-database. This system manages books, members, and loans with role-based access control and secure authentication.

Features
Role-Based Access
Librarian: Add/delete books, register members, issue/return books, view overdue loans

Member: Search catalogue, check book availability, view personal loan history

Core Functionality
Authentication: Secure login with bcrypt password hashing

Book Management: Track total and available copies

Member Registration: Store member information securely

Loan Processing: Issue books with automatic due date calculation

Overdue Tracking: Identify and manage overdue books

Technical Implementation
CSV Database: Lightweight data storage using CSV files

Password Security: Bcrypt hashing for secure password storage

Many-to-Many Relationships: Modeling between members and loans

CRUD Operations: Complete Create, Read, Update, Delete functionality

Due Date Logic: Automatic calculation and enforcement
