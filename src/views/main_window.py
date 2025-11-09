"""
Main Application Window for BookKeeper
Modern UI using CustomTkinter
"""

import customtkinter as ctk
from typing import Optional
from .books_view import BooksView
from .lending_view import LendingView
from .statistics_view import StatisticsView
from ..models.database import Database


class MainWindow:
    """Main application window with tabbed interface"""

    def __init__(self):
        # Initialize database
        self.db = Database()

        # Create main window
        self.window = ctk.CTk()
        self.window.title("BookKeeper Pro - Modern Book Management")
        self.window.geometry("1400x800")

        # Set theme
        ctk.set_appearance_mode("dark")  # dark, light, system
        ctk.set_default_color_theme("blue")  # blue, green, dark-blue

        # Create menu bar
        self.create_menu_bar()

        # Create main container
        self.main_container = ctk.CTkFrame(self.window)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabview
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True)

        # Add tabs
        self.books_tab = self.tabview.add("📚 Books")
        self.lending_tab = self.tabview.add("🔄 Lending")
        self.stats_tab = self.tabview.add("📊 Statistics")
        self.settings_tab = self.tabview.add("⚙️ Settings")

        # Initialize views
        self.books_view = BooksView(self.books_tab, self.db)
        self.lending_view = LendingView(self.lending_tab, self.db, self.books_view)
        self.stats_view = StatisticsView(self.stats_tab, self.db)
        # Pass reference to main window for statistics to access books view
        self.stats_view.main_window = self

        # Create settings view
        self.create_settings_view()

        # Bind tab change event to refresh views
        self.tabview.configure(command=self.on_tab_change)

    def create_menu_bar(self):
        """Create top menu bar with quick actions"""
        menu_frame = ctk.CTkFrame(self.window, height=50)
        menu_frame.pack(fill="x", padx=10, pady=(10, 0))

        # Title
        title_label = ctk.CTkLabel(
            menu_frame,
            text="📖 BookKeeper Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=10)

        # Theme switcher
        theme_label = ctk.CTkLabel(menu_frame, text="Theme:", font=ctk.CTkFont(size=12))
        theme_label.pack(side="right", padx=(0, 5), pady=10)

        self.theme_switch = ctk.CTkSegmentedButton(
            menu_frame,
            values=["Dark", "Light", "System"],
            command=self.change_theme
        )
        self.theme_switch.set("Dark")
        self.theme_switch.pack(side="right", padx=10, pady=10)

    def change_theme(self, value: str):
        """Change application theme"""
        ctk.set_appearance_mode(value.lower())

    def create_settings_view(self):
        """Create settings tab content"""
        settings_container = ctk.CTkFrame(self.settings_tab)
        settings_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            settings_container,
            text="⚙️ Application Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 20))

        # Database info
        db_frame = ctk.CTkFrame(settings_container)
        db_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            db_frame,
            text="Database Information",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        ctk.CTkLabel(
            db_frame,
            text=f"Database Path: {self.db.db_path}",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=5)

        # Backup/Export buttons
        button_frame = ctk.CTkFrame(settings_container)
        button_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            button_frame,
            text="Data Management",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        btn_container = ctk.CTkFrame(button_frame)
        btn_container.pack(padx=20, pady=10)

        ctk.CTkButton(
            btn_container,
            text="📤 Export to CSV",
            command=self.export_csv,
            width=200
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_container,
            text="📥 Import from CSV",
            command=self.import_csv,
            width=200
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_container,
            text="💾 Backup Database",
            command=self.backup_database,
            width=200
        ).pack(side="left", padx=5)

        # About section
        about_frame = ctk.CTkFrame(settings_container)
        about_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            about_frame,
            text="About BookKeeper Pro",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))

        about_text = """
        BookKeeper Pro - Advanced Book Management System

        Version: 2.0

        Features:
        • Complete book catalog management
        • Category organization with color coding
        • Lending tracking system
        • Notes and reviews
        • Statistics and analytics
        • Import/Export functionality
        • Modern, responsive interface

        Perfect for bookworms and book stores!
        """

        ctk.CTkLabel(
            about_frame,
            text=about_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(anchor="w", padx=20, pady=10)

    def export_csv(self):
        """Export books to CSV"""
        from ..utils.export_import import export_books_to_csv
        try:
            books_count = len(self.db.get_all_books())
            filepath = export_books_to_csv(self.db)
            if books_count == 0:
                self.show_message("Success", f"Empty CSV file created at: {filepath}\n\n(No books in database to export)")
            else:
                self.show_message("Success", f"Exported {books_count} book(s) to:\n{filepath}")
        except Exception as e:
            self.show_message("Error", f"Export failed: {str(e)}", error=True)

    def import_csv(self):
        """Import books from CSV"""
        from tkinter import filedialog
        from ..utils.export_import import import_books_from_csv

        filepath = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filepath:
            try:
                count = import_books_from_csv(self.db, filepath)
                self.show_message("Success", f"Imported {count} books successfully!")
                self.books_view.refresh()
            except Exception as e:
                self.show_message("Error", f"Import failed: {str(e)}", error=True)

    def backup_database(self):
        """Backup the database"""
        from ..utils.export_import import backup_database
        try:
            filepath = backup_database(self.db)
            self.show_message("Success", f"Database backed up to: {filepath}")
        except Exception as e:
            self.show_message("Error", f"Backup failed: {str(e)}", error=True)

    def show_message(self, title: str, message: str, error: bool = False):
        """Show a message dialog"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title(title)
        dialog.geometry("400x150")

        icon = "❌" if error else "✅"
        ctk.CTkLabel(
            dialog,
            text=f"{icon} {message}",
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=20, padx=20)

        ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        ).pack(pady=10)

        dialog.transient(self.window)
        dialog.update_idletasks()
        dialog.after(10, dialog.grab_set)

    def on_tab_change(self):
        """Handle tab change events"""
        current_tab = self.tabview.get()
        if "Statistics" in current_tab:
            self.stats_view.refresh()
        elif "Lending" in current_tab:
            self.lending_view.refresh()
        elif "Books" in current_tab:
            self.books_view.refresh()

    def run(self):
        """Start the application"""
        self.window.mainloop()

    def __del__(self):
        """Cleanup when application closes"""
        if hasattr(self, 'db'):
            self.db.close()
