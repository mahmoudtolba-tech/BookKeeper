"""
Enhanced Database Model for BookKeeper
Supports books, categories, lending, and more
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os


class Database:
    """Main database class for BookKeeper application"""

    def __init__(self, db_path: str = "data/bookkeeper.db"):
        """Initialize database connection and create tables if they don't exist"""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Create all necessary database tables"""
        cursor = self.conn.cursor()

        # Books table with extended fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                year INTEGER,
                publisher TEXT,
                pages INTEGER,
                language TEXT DEFAULT 'English',
                description TEXT,
                rating REAL DEFAULT 0,
                category_id INTEGER,
                purchase_date TEXT,
                purchase_price REAL,
                purchase_store TEXT,
                cover_image_path TEXT,
                date_added TEXT DEFAULT CURRENT_TIMESTAMP,
                last_modified TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                color TEXT DEFAULT '#3498db'
            )
        """)

        # Lending table to track who borrowed books
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lending (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                borrower_name TEXT NOT NULL,
                borrower_contact TEXT,
                lend_date TEXT NOT NULL,
                expected_return_date TEXT,
                actual_return_date TEXT,
                notes TEXT,
                status TEXT DEFAULT 'borrowed',
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)

        # Notes/Reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                note_text TEXT NOT NULL,
                date_created TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
            )
        """)

        # Add some default categories
        default_categories = [
            ('Fiction', 'Fictional literature', '#e74c3c'),
            ('Non-Fiction', 'Non-fictional works', '#3498db'),
            ('Science', 'Scientific literature', '#2ecc71'),
            ('Technology', 'Technology and computing', '#9b59b6'),
            ('Biography', 'Biographies and memoirs', '#f39c12'),
            ('History', 'Historical works', '#1abc9c'),
            ('Self-Help', 'Self-improvement books', '#e67e22'),
            ('Children', 'Children literature', '#f1c40f'),
            ('Reference', 'Reference materials', '#34495e'),
            ('Other', 'Miscellaneous', '#95a5a6')
        ]

        for name, desc, color in default_categories:
            cursor.execute(
                "INSERT OR IGNORE INTO categories (name, description, color) VALUES (?, ?, ?)",
                (name, desc, color)
            )

        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    # ==================== BOOK OPERATIONS ====================

    def add_book(self, **kwargs) -> int:
        """Add a new book to the database"""
        fields = []
        values = []

        for key, value in kwargs.items():
            if value is not None and value != '':
                fields.append(key)
                values.append(value)

        if 'date_added' not in fields:
            fields.append('date_added')
            values.append(datetime.now().isoformat())

        query = f"INSERT INTO books ({', '.join(fields)}) VALUES ({', '.join(['?']*len(values))})"
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        return cursor.lastrowid

    def get_all_books(self) -> List[Dict]:
        """Get all books from database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.*, c.name as category_name, c.color as category_color
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            ORDER BY b.title
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        """Get a specific book by ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.*, c.name as category_name
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.id = ?
        """, (book_id,))
        result = cursor.fetchone()
        return dict(result) if result else None

    def update_book(self, book_id: int, **kwargs):
        """Update a book's information"""
        fields = []
        values = []

        for key, value in kwargs.items():
            if key != 'id':
                fields.append(f"{key} = ?")
                values.append(value)

        fields.append("last_modified = ?")
        values.append(datetime.now().isoformat())
        values.append(book_id)

        query = f"UPDATE books SET {', '.join(fields)} WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()

    def delete_book(self, book_id: int):
        """Delete a book from database"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()

    def search_books(self, query: str, category_id: Optional[int] = None) -> List[Dict]:
        """Search books by title, author, ISBN, or description"""
        cursor = self.conn.cursor()
        search_term = f"%{query}%"

        if category_id:
            cursor.execute("""
                SELECT b.*, c.name as category_name, c.color as category_color
                FROM books b
                LEFT JOIN categories c ON b.category_id = c.id
                WHERE (b.title LIKE ? OR b.author LIKE ? OR b.isbn LIKE ? OR b.description LIKE ?)
                AND b.category_id = ?
                ORDER BY b.title
            """, (search_term, search_term, search_term, search_term, category_id))
        else:
            cursor.execute("""
                SELECT b.*, c.name as category_name, c.color as category_color
                FROM books b
                LEFT JOIN categories c ON b.category_id = c.id
                WHERE b.title LIKE ? OR b.author LIKE ? OR b.isbn LIKE ? OR b.description LIKE ?
                ORDER BY b.title
            """, (search_term, search_term, search_term, search_term))

        return [dict(row) for row in cursor.fetchall()]

    # ==================== CATEGORY OPERATIONS ====================

    def get_all_categories(self) -> List[Dict]:
        """Get all categories"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM categories ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]

    def add_category(self, name: str, description: str = '', color: str = '#3498db') -> int:
        """Add a new category"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, description, color) VALUES (?, ?, ?)",
            (name, description, color)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_category_stats(self) -> List[Dict]:
        """Get statistics for each category"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.id, c.name, c.color, COUNT(b.id) as book_count
            FROM categories c
            LEFT JOIN books b ON c.id = b.category_id
            GROUP BY c.id, c.name, c.color
            ORDER BY book_count DESC, c.name
        """)
        return [dict(row) for row in cursor.fetchall()]

    # ==================== LENDING OPERATIONS ====================

    def lend_book(self, book_id: int, borrower_name: str, borrower_contact: str = '',
                  expected_return_date: str = '', notes: str = '') -> int:
        """Record a book being lent out"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO lending (book_id, borrower_name, borrower_contact,
                               lend_date, expected_return_date, notes, status)
            VALUES (?, ?, ?, ?, ?, ?, 'borrowed')
        """, (book_id, borrower_name, borrower_contact, datetime.now().isoformat(),
              expected_return_date, notes))
        self.conn.commit()
        return cursor.lastrowid

    def return_book(self, lending_id: int):
        """Mark a book as returned"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE lending
            SET actual_return_date = ?, status = 'returned'
            WHERE id = ?
        """, (datetime.now().isoformat(), lending_id))
        self.conn.commit()

    def get_borrowed_books(self) -> List[Dict]:
        """Get all currently borrowed books"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT l.*, b.title, b.author
            FROM lending l
            JOIN books b ON l.book_id = b.id
            WHERE l.status = 'borrowed'
            ORDER BY l.lend_date DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_lending_history(self, book_id: Optional[int] = None) -> List[Dict]:
        """Get lending history for all books or a specific book"""
        cursor = self.conn.cursor()
        if book_id:
            cursor.execute("""
                SELECT l.*, b.title, b.author
                FROM lending l
                JOIN books b ON l.book_id = b.id
                WHERE l.book_id = ?
                ORDER BY l.lend_date DESC
            """, (book_id,))
        else:
            cursor.execute("""
                SELECT l.*, b.title, b.author
                FROM lending l
                JOIN books b ON l.book_id = b.id
                ORDER BY l.lend_date DESC
            """)
        return [dict(row) for row in cursor.fetchall()]

    # ==================== NOTES OPERATIONS ====================

    def add_note(self, book_id: int, note_text: str) -> int:
        """Add a note/review for a book"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO notes (book_id, note_text) VALUES (?, ?)",
            (book_id, note_text)
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_book_notes(self, book_id: int) -> List[Dict]:
        """Get all notes for a specific book"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM notes WHERE book_id = ? ORDER BY date_created DESC",
            (book_id,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def delete_note(self, note_id: int):
        """Delete a note"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()

    # ==================== STATISTICS ====================

    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        cursor = self.conn.cursor()

        stats = {}

        # Total books
        cursor.execute("SELECT COUNT(*) as count FROM books")
        stats['total_books'] = cursor.fetchone()['count']

        # Total categories
        cursor.execute("SELECT COUNT(*) as count FROM categories")
        stats['total_categories'] = cursor.fetchone()['count']

        # Currently borrowed
        cursor.execute("SELECT COUNT(*) as count FROM lending WHERE status = 'borrowed'")
        stats['books_borrowed'] = cursor.fetchone()['count']

        # Average rating
        cursor.execute("SELECT AVG(rating) as avg FROM books WHERE rating > 0")
        result = cursor.fetchone()
        stats['average_rating'] = round(result['avg'], 2) if result['avg'] else 0

        # Most read author
        cursor.execute("""
            SELECT author, COUNT(*) as count
            FROM books
            GROUP BY author
            ORDER BY count DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        stats['top_author'] = result['author'] if result else 'N/A'
        stats['top_author_count'] = result['count'] if result else 0

        # Recent additions
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM books
            WHERE date_added >= date('now', '-30 days')
        """)
        stats['recent_additions'] = cursor.fetchone()['count']

        return stats
