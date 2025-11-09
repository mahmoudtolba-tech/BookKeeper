"""
Lending View - Track borrowed books
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from typing import Optional, Dict
from ..models.database import Database


class LendingView:
    """View for managing book lending"""

    def __init__(self, parent, db: Database, books_view):
        self.parent = parent
        self.db = db
        self.books_view = books_view
        self.current_lendings = []

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ctk.CTkFrame(self.parent)
        main_container.pack(fill="both", expand=True)

        # Left panel - Currently borrowed books
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Header
        header_frame = ctk.CTkFrame(left_panel)
        header_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            header_frame,
            text="📚 Currently Borrowed Books",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            header_frame,
            text="➕ Lend a Book",
            command=self.show_lend_dialog,
            height=35,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="right", padx=10)

        # Borrowed books list
        self.borrowed_scroll = ctk.CTkScrollableFrame(left_panel, height=500)
        self.borrowed_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Right panel - Lending history
        right_panel = ctk.CTkFrame(main_container, width=400)
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        right_panel.pack_propagate(False)

        # History header
        history_header = ctk.CTkFrame(right_panel)
        history_header.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            history_header,
            text="📜 Lending History",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10)

        # History list
        self.history_scroll = ctk.CTkScrollableFrame(right_panel)
        self.history_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def refresh(self):
        """Refresh the lending lists"""
        self.current_lendings = self.db.get_borrowed_books()
        self.update_borrowed_display()
        self.update_history_display()

    def update_borrowed_display(self):
        """Update the borrowed books display"""
        # Clear current display
        for widget in self.borrowed_scroll.winfo_children():
            widget.destroy()

        if not self.current_lendings:
            ctk.CTkLabel(
                self.borrowed_scroll,
                text="No books currently borrowed",
                text_color="gray",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return

        # Display borrowed books
        for lending in self.current_lendings:
            self.create_lending_card(lending)

    def create_lending_card(self, lending: Dict):
        """Create a card for a borrowed book"""
        card = ctk.CTkFrame(self.borrowed_scroll, fg_color="#2b2b2b")
        card.pack(fill="x", pady=5, padx=5)

        # Content frame
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=15)

        # Book title
        ctk.CTkLabel(
            content,
            text=lending['title'],
            font=ctk.CTkFont(size=15, weight="bold"),
            anchor="w"
        ).pack(fill="x")

        # Author
        ctk.CTkLabel(
            content,
            text=f"by {lending['author']}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        ).pack(fill="x", pady=(2, 10))

        # Borrower info
        borrower_frame = ctk.CTkFrame(content, fg_color="#1e1e1e", corner_radius=8)
        borrower_frame.pack(fill="x", pady=(0, 10))

        borrower_content = ctk.CTkFrame(borrower_frame, fg_color="transparent")
        borrower_content.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            borrower_content,
            text=f"👤 Borrower: {lending['borrower_name']}",
            font=ctk.CTkFont(size=12),
            anchor="w"
        ).pack(fill="x")

        if lending.get('borrower_contact'):
            ctk.CTkLabel(
                borrower_content,
                text=f"📞 Contact: {lending['borrower_contact']}",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            ).pack(fill="x")

        # Dates
        date_frame = ctk.CTkFrame(content, fg_color="transparent")
        date_frame.pack(fill="x")

        lend_date = datetime.fromisoformat(lending['lend_date'])
        ctk.CTkLabel(
            date_frame,
            text=f"📅 Lent: {lend_date.strftime('%Y-%m-%d')}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="left")

        # Check if overdue
        if lending.get('expected_return_date'):
            expected_date = datetime.fromisoformat(lending['expected_return_date'])
            days_diff = (expected_date - datetime.now()).days

            if days_diff < 0:
                status_text = f"⚠️ Overdue by {abs(days_diff)} days"
                status_color = "#e74c3c"
            elif days_diff == 0:
                status_text = "⏰ Due today"
                status_color = "#f39c12"
            else:
                status_text = f"✓ Due in {days_diff} days"
                status_color = "#2ecc71"

            ctk.CTkLabel(
                date_frame,
                text=status_text,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=status_color
            ).pack(side="right")

        # Notes
        if lending.get('notes'):
            notes_frame = ctk.CTkFrame(content, fg_color="#1e1e1e", corner_radius=8)
            notes_frame.pack(fill="x", pady=(10, 0))

            ctk.CTkLabel(
                notes_frame,
                text=f"📝 {lending['notes']}",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                wraplength=350,
                justify="left"
            ).pack(padx=10, pady=8, anchor="w")

        # Action button
        ctk.CTkButton(
            content,
            text="✓ Mark as Returned",
            command=lambda l=lending: self.return_book(l['id']),
            height=35,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill="x", pady=(10, 0))

    def update_history_display(self):
        """Update the lending history display"""
        # Clear current display
        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        history = self.db.get_lending_history()

        if not history:
            ctk.CTkLabel(
                self.history_scroll,
                text="No lending history",
                text_color="gray"
            ).pack(pady=20)
            return

        # Display only returned books (last 20)
        returned_books = [h for h in history if h['status'] == 'returned'][:20]

        for lending in returned_books:
            self.create_history_card(lending)

    def create_history_card(self, lending: Dict):
        """Create a card for lending history"""
        card = ctk.CTkFrame(self.history_scroll, fg_color="#2b2b2b")
        card.pack(fill="x", pady=3, padx=5)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=10, pady=8)

        # Book title (smaller)
        ctk.CTkLabel(
            content,
            text=lending['title'],
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).pack(fill="x")

        # Borrower and dates
        info_text = f"👤 {lending['borrower_name']}"
        if lending.get('actual_return_date'):
            return_date = datetime.fromisoformat(lending['actual_return_date'])
            info_text += f"\n✓ Returned: {return_date.strftime('%Y-%m-%d')}"

        ctk.CTkLabel(
            content,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w",
            justify="left"
        ).pack(fill="x")

    def show_lend_dialog(self):
        """Show dialog to lend a book"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Lend a Book")
        dialog.geometry("550x750")  # Made taller to show all fields and buttons

        dialog.transient(self.parent)
        dialog.update_idletasks()  # Ensure window is created
        dialog.after(10, dialog.grab_set)  # Delay grab_set until window is visible

        # Scrollable form container
        form = ctk.CTkScrollableFrame(dialog)
        form.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            form,
            text="📚 Lend a Book",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(0, 20))

        # Book selection
        ctk.CTkLabel(form, text="Select Book *", anchor="w").pack(fill="x", pady=(0, 5))

        books = self.db.get_all_books()
        book_options = [f"{book['title']} - {book['author']}" for book in books]

        book_combo = ctk.CTkComboBox(form, values=book_options, height=35)
        book_combo.pack(fill="x", pady=(0, 15))

        # Borrower name
        ctk.CTkLabel(form, text="Borrower Name *", anchor="w").pack(fill="x", pady=(0, 5))
        borrower_name = ctk.CTkEntry(form, height=35)
        borrower_name.pack(fill="x", pady=(0, 15))

        # Borrower contact
        ctk.CTkLabel(form, text="Borrower Contact (Phone/Email)", anchor="w").pack(fill="x", pady=(0, 5))
        borrower_contact = ctk.CTkEntry(form, height=35, placeholder_text="Optional")
        borrower_contact.pack(fill="x", pady=(0, 15))

        # Expected return date
        ctk.CTkLabel(form, text="Expected Return Date", anchor="w").pack(fill="x", pady=(0, 5))

        date_frame = ctk.CTkFrame(form, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 15))

        # Calculate default date (2 weeks from now)
        default_date = datetime.now() + timedelta(days=14)

        return_date = ctk.CTkEntry(
            date_frame,
            height=35,
            placeholder_text="YYYY-MM-DD"
        )
        return_date.insert(0, default_date.strftime("%Y-%m-%d"))
        return_date.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Quick date buttons
        quick_frame = ctk.CTkFrame(form, fg_color="transparent")
        quick_frame.pack(fill="x", pady=(0, 15))

        def set_quick_date(days: int):
            quick_date = datetime.now() + timedelta(days=days)
            return_date.delete(0, 'end')
            return_date.insert(0, quick_date.strftime("%Y-%m-%d"))

        ctk.CTkButton(
            quick_frame,
            text="1 Week",
            command=lambda: set_quick_date(7),
            width=80,
            height=25
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            quick_frame,
            text="2 Weeks",
            command=lambda: set_quick_date(14),
            width=80,
            height=25
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            quick_frame,
            text="1 Month",
            command=lambda: set_quick_date(30),
            width=80,
            height=25
        ).pack(side="left", padx=2)

        # Notes
        ctk.CTkLabel(form, text="Notes", anchor="w").pack(fill="x", pady=(0, 5))
        notes = ctk.CTkTextbox(form, height=100)
        notes.pack(fill="x", pady=(0, 15))

        # Buttons
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))

        def save_lending():
            # Validate
            if not book_combo.get() or not borrower_name.get():
                messagebox.showerror("Error", "Please select a book and enter borrower name!")
                return

            # Get book ID
            selected_index = book_options.index(book_combo.get())
            book_id = books[selected_index]['id']

            try:
                self.db.lend_book(
                    book_id=book_id,
                    borrower_name=borrower_name.get(),
                    borrower_contact=borrower_contact.get(),
                    expected_return_date=return_date.get(),
                    notes=notes.get("1.0", "end-1c")
                )

                self.refresh()
                dialog.destroy()
                messagebox.showinfo("Success", "Book lent successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to record lending: {str(e)}")

        ctk.CTkButton(
            btn_frame,
            text="Lend Book",
            command=save_lending,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))

    def return_book(self, lending_id: int):
        """Mark a book as returned"""
        if messagebox.askyesno("Confirm Return", "Mark this book as returned?"):
            try:
                self.db.return_book(lending_id)
                self.refresh()
                messagebox.showinfo("Success", "Book marked as returned!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to return book: {str(e)}")
