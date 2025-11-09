"""
Books View - Main book management interface
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, Dict
from ..models.database import Database


class BooksView:
    """Books management view with add, edit, delete, search functionality"""

    def __init__(self, parent, db: Database):
        self.parent = parent
        self.db = db
        self.selected_book_id: Optional[int] = None
        self.current_books = []

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container with two columns
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True)

        # Left panel - Book list and search
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Search section
        search_frame = ctk.CTkFrame(left_panel)
        search_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            search_frame,
            text="🔍 Search Books",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(5, 10))

        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.search_entry = ctk.CTkEntry(
            search_input_frame,
            placeholder_text="Search by title, author, ISBN...",
            height=35
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_books())

        ctk.CTkButton(
            search_input_frame,
            text="🔍",
            width=40,
            command=self.search_books
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            search_input_frame,
            text="Clear",
            width=60,
            command=self.clear_search
        ).pack(side="left")

        # Category filter
        filter_frame = ctk.CTkFrame(search_frame)
        filter_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(filter_frame, text="Category:").pack(side="left", padx=(0, 5))

        self.category_filter = ctk.CTkComboBox(
            filter_frame,
            values=["All Categories"],
            command=self.filter_by_category,
            width=200
        )
        self.category_filter.pack(side="left")

        # Books list
        list_frame = ctk.CTkFrame(left_panel)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(
            list_frame,
            text="📚 Book Collection",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(5, 10))

        # Create scrollable frame for books
        self.books_scroll = ctk.CTkScrollableFrame(list_frame, height=400)
        self.books_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Action buttons
        action_frame = ctk.CTkFrame(left_panel)
        action_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            action_frame,
            text="➕ Add New Book",
            command=self.show_add_dialog,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill="x", pady=5)

        # Right panel - Book details
        right_panel = ctk.CTkFrame(main_container, width=400)
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        right_panel.pack_propagate(False)

        self.details_container = ctk.CTkScrollableFrame(right_panel)
        self.details_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.show_no_selection()

    def show_no_selection(self):
        """Show message when no book is selected"""
        for widget in self.details_container.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.details_container,
            text="📖",
            font=ctk.CTkFont(size=60)
        ).pack(pady=50)

        ctk.CTkLabel(
            self.details_container,
            text="Select a book to view details",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        ).pack()

    def refresh(self):
        """Refresh the books list"""
        self.current_books = self.db.get_all_books()
        self.update_books_display()
        self.update_category_filter()

    def update_category_filter(self):
        """Update category filter dropdown"""
        categories = self.db.get_all_categories()
        category_names = ["All Categories"] + [cat['name'] for cat in categories]
        self.category_filter.configure(values=category_names)

    def update_books_display(self):
        """Update the books display"""
        # Clear current display
        for widget in self.books_scroll.winfo_children():
            widget.destroy()

        if not self.current_books:
            ctk.CTkLabel(
                self.books_scroll,
                text="No books found. Add your first book!",
                text_color="gray"
            ).pack(pady=20)
            return

        # Display books
        for book in self.current_books:
            self.create_book_card(book)

    def create_book_card(self, book: Dict):
        """Create a card for displaying a book"""
        card = ctk.CTkFrame(self.books_scroll, fg_color="#2b2b2b")
        card.pack(fill="x", pady=5, padx=5)

        # Book info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=10)

        # Title and rating
        title_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_frame.pack(fill="x")

        title_label = ctk.CTkLabel(
            title_frame,
            text=book['title'],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)

        if book['rating'] and book['rating'] > 0:
            rating_text = "⭐" * int(book['rating'])
            rating_label = ctk.CTkLabel(
                title_frame,
                text=rating_text,
                font=ctk.CTkFont(size=12)
            )
            rating_label.pack(side="right")

        # Author
        ctk.CTkLabel(
            info_frame,
            text=f"by {book['author']}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x")

        # Category badge
        if book['category_name']:
            badge = ctk.CTkLabel(
                info_frame,
                text=book['category_name'],
                font=ctk.CTkFont(size=10),
                fg_color=book.get('category_color', '#3498db'),
                corner_radius=5,
                padx=8,
                pady=2
            )
            badge.pack(anchor="w", pady=(5, 0))

        # Action buttons
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="View",
            width=70,
            height=25,
            command=lambda b=book: self.show_book_details(b)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame,
            text="Edit",
            width=70,
            height=25,
            command=lambda b=book: self.show_edit_dialog(b),
            fg_color="#f39c12",
            hover_color="#e67e22"
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=70,
            height=25,
            command=lambda b=book: self.delete_book(b['id']),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", padx=2)

    def show_book_details(self, book: Dict):
        """Show detailed information about a book"""
        self.selected_book_id = book['id']

        # Clear details panel
        for widget in self.details_container.winfo_children():
            widget.destroy()

        # Title
        ctk.CTkLabel(
            self.details_container,
            text=book['title'],
            font=ctk.CTkFont(size=20, weight="bold"),
            wraplength=350
        ).pack(pady=(10, 5))

        # Author
        ctk.CTkLabel(
            self.details_container,
            text=f"by {book['author']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 10))

        # Rating
        if book['rating'] and book['rating'] > 0:
            rating_text = "⭐" * int(book['rating'])
            ctk.CTkLabel(
                self.details_container,
                text=rating_text,
                font=ctk.CTkFont(size=16)
            ).pack(pady=5)

        # Details frame
        details_frame = ctk.CTkFrame(self.details_container)
        details_frame.pack(fill="x", pady=10)

        details = [
            ("ISBN", book.get('isbn', 'N/A')),
            ("Year", book.get('year', 'N/A')),
            ("Publisher", book.get('publisher', 'N/A')),
            ("Pages", book.get('pages', 'N/A')),
            ("Language", book.get('language', 'N/A')),
            ("Category", book.get('category_name', 'N/A')),
        ]

        for label, value in details:
            if value and value != 'N/A':
                row = ctk.CTkFrame(details_frame, fg_color="transparent")
                row.pack(fill="x", padx=10, pady=2)

                ctk.CTkLabel(
                    row,
                    text=f"{label}:",
                    font=ctk.CTkFont(weight="bold"),
                    width=100,
                    anchor="w"
                ).pack(side="left")

                ctk.CTkLabel(
                    row,
                    text=str(value),
                    anchor="w"
                ).pack(side="left", fill="x", expand=True)

        # Description
        if book.get('description'):
            desc_frame = ctk.CTkFrame(self.details_container)
            desc_frame.pack(fill="x", pady=10)

            ctk.CTkLabel(
                desc_frame,
                text="Description:",
                font=ctk.CTkFont(weight="bold"),
                anchor="w"
            ).pack(padx=10, pady=(10, 5), anchor="w")

            ctk.CTkLabel(
                desc_frame,
                text=book['description'],
                wraplength=350,
                justify="left",
                anchor="w"
            ).pack(padx=10, pady=(0, 10), anchor="w")

        # Purchase info
        if book.get('purchase_price') or book.get('purchase_date'):
            purchase_frame = ctk.CTkFrame(self.details_container)
            purchase_frame.pack(fill="x", pady=10)

            ctk.CTkLabel(
                purchase_frame,
                text="Purchase Information:",
                font=ctk.CTkFont(weight="bold"),
                anchor="w"
            ).pack(padx=10, pady=(10, 5), anchor="w")

            if book.get('purchase_price'):
                ctk.CTkLabel(
                    purchase_frame,
                    text=f"Price: ${book['purchase_price']}",
                    anchor="w"
                ).pack(padx=20, anchor="w")

            if book.get('purchase_date'):
                ctk.CTkLabel(
                    purchase_frame,
                    text=f"Date: {book['purchase_date']}",
                    anchor="w"
                ).pack(padx=20, anchor="w")

            if book.get('purchase_store'):
                ctk.CTkLabel(
                    purchase_frame,
                    text=f"Store: {book['purchase_store']}",
                    anchor="w"
                ).pack(padx=20, pady=(0, 10), anchor="w")

    def show_add_dialog(self):
        """Show dialog to add a new book"""
        self.show_book_dialog()

    def show_edit_dialog(self, book: Dict):
        """Show dialog to edit a book"""
        self.show_book_dialog(book)

    def show_book_dialog(self, book: Optional[Dict] = None):
        """Show dialog for adding or editing a book"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Edit Book" if book else "Add New Book")
        dialog.geometry("600x800")  # Made taller to show all fields

        # Make it modal (after window is visible)
        dialog.transient(self.parent)
        dialog.update_idletasks()  # Ensure window is created
        dialog.after(10, dialog.grab_set)  # Delay grab_set until window is visible

        # Scrollable form
        form_scroll = ctk.CTkScrollableFrame(dialog)
        form_scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # Form fields
        fields = {}

        # Title
        ctk.CTkLabel(form_scroll, text="Title *", anchor="w").pack(fill="x", pady=(0, 5))
        fields['title'] = ctk.CTkEntry(form_scroll, height=35)
        fields['title'].pack(fill="x", pady=(0, 10))

        # Author
        ctk.CTkLabel(form_scroll, text="Author *", anchor="w").pack(fill="x", pady=(0, 5))
        fields['author'] = ctk.CTkEntry(form_scroll, height=35)
        fields['author'].pack(fill="x", pady=(0, 10))

        # ISBN
        ctk.CTkLabel(form_scroll, text="ISBN", anchor="w").pack(fill="x", pady=(0, 5))
        fields['isbn'] = ctk.CTkEntry(form_scroll, height=35)
        fields['isbn'].pack(fill="x", pady=(0, 10))

        # Year
        ctk.CTkLabel(form_scroll, text="Year", anchor="w").pack(fill="x", pady=(0, 5))
        fields['year'] = ctk.CTkEntry(form_scroll, height=35)
        fields['year'].pack(fill="x", pady=(0, 10))

        # Publisher
        ctk.CTkLabel(form_scroll, text="Publisher", anchor="w").pack(fill="x", pady=(0, 5))
        fields['publisher'] = ctk.CTkEntry(form_scroll, height=35)
        fields['publisher'].pack(fill="x", pady=(0, 10))

        # Pages
        ctk.CTkLabel(form_scroll, text="Pages", anchor="w").pack(fill="x", pady=(0, 5))
        fields['pages'] = ctk.CTkEntry(form_scroll, height=35)
        fields['pages'].pack(fill="x", pady=(0, 10))

        # Language
        ctk.CTkLabel(form_scroll, text="Language", anchor="w").pack(fill="x", pady=(0, 5))
        fields['language'] = ctk.CTkEntry(form_scroll, height=35)
        fields['language'].insert(0, "English")
        fields['language'].pack(fill="x", pady=(0, 10))

        # Category
        ctk.CTkLabel(form_scroll, text="Category", anchor="w").pack(fill="x", pady=(0, 5))
        categories = self.db.get_all_categories()
        category_names = [cat['name'] for cat in categories]
        fields['category'] = ctk.CTkComboBox(form_scroll, values=category_names, height=35)
        fields['category'].pack(fill="x", pady=(0, 10))

        # Rating
        ctk.CTkLabel(form_scroll, text="Rating (0-5)", anchor="w").pack(fill="x", pady=(0, 5))
        fields['rating'] = ctk.CTkSlider(form_scroll, from_=0, to=5, number_of_steps=5)
        fields['rating'].set(0)
        fields['rating'].pack(fill="x", pady=(0, 10))

        rating_label = ctk.CTkLabel(form_scroll, text="0")
        rating_label.pack()

        def update_rating_label(value):
            rating_label.configure(text=f"{int(value)}")

        fields['rating'].configure(command=update_rating_label)

        # Description
        ctk.CTkLabel(form_scroll, text="Description", anchor="w").pack(fill="x", pady=(0, 5))
        fields['description'] = ctk.CTkTextbox(form_scroll, height=100)
        fields['description'].pack(fill="x", pady=(0, 10))

        # Purchase price
        ctk.CTkLabel(form_scroll, text="Purchase Price ($)", anchor="w").pack(fill="x", pady=(0, 5))
        fields['purchase_price'] = ctk.CTkEntry(form_scroll, height=35)
        fields['purchase_price'].pack(fill="x", pady=(0, 10))

        # Purchase store
        ctk.CTkLabel(form_scroll, text="Purchase Store", anchor="w").pack(fill="x", pady=(0, 5))
        fields['purchase_store'] = ctk.CTkEntry(form_scroll, height=35)
        fields['purchase_store'].pack(fill="x", pady=(0, 10))

        # If editing, populate fields
        if book:
            fields['title'].insert(0, book['title'])
            fields['author'].insert(0, book['author'])
            if book.get('isbn'):
                fields['isbn'].insert(0, book['isbn'])
            if book.get('year'):
                fields['year'].insert(0, str(book['year']))
            if book.get('publisher'):
                fields['publisher'].insert(0, book['publisher'])
            if book.get('pages'):
                fields['pages'].insert(0, str(book['pages']))
            if book.get('language'):
                fields['language'].delete(0, 'end')
                fields['language'].insert(0, book['language'])
            if book.get('category_name'):
                fields['category'].set(book['category_name'])
            if book.get('rating'):
                fields['rating'].set(book['rating'])
                update_rating_label(book['rating'])
            if book.get('description'):
                fields['description'].insert("1.0", book['description'])
            if book.get('purchase_price'):
                fields['purchase_price'].insert(0, str(book['purchase_price']))
            if book.get('purchase_store'):
                fields['purchase_store'].insert(0, book['purchase_store'])

        # Buttons
        btn_frame = ctk.CTkFrame(dialog)
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        def save_book():
            # Validate required fields
            if not fields['title'].get() or not fields['author'].get():
                messagebox.showerror("Error", "Title and Author are required!")
                return

            # Get category ID
            category_name = fields['category'].get()
            category_id = None
            for cat in categories:
                if cat['name'] == category_name:
                    category_id = cat['id']
                    break

            # Prepare book data
            book_data = {
                'title': fields['title'].get(),
                'author': fields['author'].get(),
                'isbn': fields['isbn'].get() or None,
                'year': int(fields['year'].get()) if fields['year'].get() else None,
                'publisher': fields['publisher'].get() or None,
                'pages': int(fields['pages'].get()) if fields['pages'].get() else None,
                'language': fields['language'].get() or 'English',
                'category_id': category_id,
                'rating': fields['rating'].get(),
                'description': fields['description'].get("1.0", "end-1c") or None,
                'purchase_price': float(fields['purchase_price'].get()) if fields['purchase_price'].get() else None,
                'purchase_store': fields['purchase_store'].get() or None,
            }

            try:
                if book:
                    # Update existing book
                    self.db.update_book(book['id'], **book_data)
                else:
                    # Add new book
                    self.db.add_book(**book_data)

                self.refresh()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save book: {str(e)}")

        ctk.CTkButton(
            btn_frame,
            text="Save",
            command=save_book,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            height=40
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            height=40
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def delete_book(self, book_id: int):
        """Delete a book"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
            try:
                self.db.delete_book(book_id)
                self.refresh()
                self.show_no_selection()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

    def search_books(self):
        """Search books"""
        query = self.search_entry.get()
        if query:
            self.current_books = self.db.search_books(query)
        else:
            self.current_books = self.db.get_all_books()
        self.update_books_display()

    def clear_search(self):
        """Clear search and show all books"""
        self.search_entry.delete(0, 'end')
        self.category_filter.set("All Categories")
        self.refresh()

    def filter_by_category(self, category_name: str):
        """Filter books by category"""
        if category_name == "All Categories":
            self.current_books = self.db.get_all_books()
        else:
            categories = self.db.get_all_categories()
            category_id = None
            for cat in categories:
                if cat['name'] == category_name:
                    category_id = cat['id']
                    break

            if category_id:
                query = self.search_entry.get()
                self.current_books = self.db.search_books(query if query else "", category_id)

        self.update_books_display()
