"""
Export and Import utilities for BookKeeper
"""

import csv
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from ..models.database import Database


def export_books_to_csv(db: Database, filepath: str = None) -> str:
    """Export all books to CSV file"""
    if not filepath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"exports/books_export_{timestamp}.csv"

    # Create exports directory if it doesn't exist
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    books = db.get_all_books()

    # Define CSV columns
    fieldnames = [
        'id', 'title', 'author', 'isbn', 'year', 'publisher', 'pages',
        'language', 'description', 'rating', 'category_name',
        'purchase_date', 'purchase_price', 'purchase_store', 'date_added'
    ]

    if not books:
        # Create empty file with headers only
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return filepath

    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for book in books:
            # Only write fields that are in fieldnames
            row = {key: book.get(key, '') for key in fieldnames}
            writer.writerow(row)

    return filepath


def import_books_from_csv(db: Database, filepath: str) -> int:
    """Import books from CSV file"""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    imported_count = 0

    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Skip if title or author is missing
            if not row.get('title') or not row.get('author'):
                continue

            # Get category ID from category name
            category_id = None
            if row.get('category_name'):
                categories = db.get_all_categories()
                for cat in categories:
                    if cat['name'] == row['category_name']:
                        category_id = cat['id']
                        break

            # Prepare book data
            book_data = {
                'title': row['title'],
                'author': row['author'],
                'isbn': row.get('isbn') or None,
                'year': int(row['year']) if row.get('year') and row['year'].isdigit() else None,
                'publisher': row.get('publisher') or None,
                'pages': int(row['pages']) if row.get('pages') and row['pages'].isdigit() else None,
                'language': row.get('language') or 'English',
                'description': row.get('description') or None,
                'rating': float(row['rating']) if row.get('rating') else 0,
                'category_id': category_id,
                'purchase_date': row.get('purchase_date') or None,
                'purchase_price': float(row['purchase_price']) if row.get('purchase_price') else None,
                'purchase_store': row.get('purchase_store') or None,
            }

            try:
                db.add_book(**book_data)
                imported_count += 1
            except Exception as e:
                print(f"Error importing book '{row.get('title', 'Unknown')}': {e}")
                continue

    return imported_count


def export_books_to_json(db: Database, filepath: str = None) -> str:
    """Export all books to JSON file"""
    if not filepath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"exports/books_export_{timestamp}.json"

    # Create exports directory if it doesn't exist
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    books = db.get_all_books()

    if not books:
        books = []  # Export empty array instead of raising error

    # Convert to JSON-serializable format
    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_books': len(books),
        'books': books
    }

    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)

    return filepath


def import_books_from_json(db: Database, filepath: str) -> int:
    """Import books from JSON file"""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)

    books = data.get('books', [])
    imported_count = 0

    for book in books:
        # Skip if title or author is missing
        if not book.get('title') or not book.get('author'):
            continue

        # Get category ID from category name
        category_id = None
        if book.get('category_name'):
            categories = db.get_all_categories()
            for cat in categories:
                if cat['name'] == book['category_name']:
                    category_id = cat['id']
                    break

        # Prepare book data (excluding ID and timestamps)
        book_data = {
            'title': book['title'],
            'author': book['author'],
            'isbn': book.get('isbn'),
            'year': book.get('year'),
            'publisher': book.get('publisher'),
            'pages': book.get('pages'),
            'language': book.get('language', 'English'),
            'description': book.get('description'),
            'rating': book.get('rating', 0),
            'category_id': category_id,
            'purchase_date': book.get('purchase_date'),
            'purchase_price': book.get('purchase_price'),
            'purchase_store': book.get('purchase_store'),
        }

        try:
            db.add_book(**book_data)
            imported_count += 1
        except Exception as e:
            print(f"Error importing book '{book.get('title', 'Unknown')}': {e}")
            continue

    return imported_count


def backup_database(db: Database, backup_dir: str = "backups") -> str:
    """Create a backup of the database"""
    # Create backups directory if it doesn't exist
    Path(backup_dir).mkdir(parents=True, exist_ok=True)

    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(backup_dir) / f"bookkeeper_backup_{timestamp}.db"

    # Copy the database file
    shutil.copy2(db.db_path, backup_path)

    return str(backup_path)


def restore_database(backup_path: str, db_path: str = "data/bookkeeper.db") -> bool:
    """Restore database from a backup"""
    if not Path(backup_path).exists():
        raise FileNotFoundError(f"Backup file not found: {backup_path}")

    # Create a backup of current database before restoring
    if Path(db_path).exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safety_backup = f"{db_path}.before_restore_{timestamp}.bak"
        shutil.copy2(db_path, safety_backup)

    # Restore from backup
    shutil.copy2(backup_path, db_path)

    return True
