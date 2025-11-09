"""
Statistics View - Dashboard with analytics
"""

import customtkinter as ctk
from ..models.database import Database


class StatisticsView:
    """Statistics and analytics dashboard"""

    def __init__(self, parent, db: Database):
        self.parent = parent
        self.db = db
        self.main_window = None  # Will be set by main_window

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_container = ctk.CTkScrollableFrame(self.parent)
        main_container.pack(fill="both", expand=True)

        # Title
        title_frame = ctk.CTkFrame(main_container)
        title_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            title_frame,
            text="📊 Library Statistics",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            title_frame,
            text="🔄 Refresh",
            command=self.refresh,
            height=35
        ).pack(side="right", padx=10)

        # Stats cards container
        self.stats_container = ctk.CTkFrame(main_container)
        self.stats_container.pack(fill="x", padx=20, pady=(0, 20))

        # Category breakdown container
        self.category_container = ctk.CTkFrame(main_container)
        self.category_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh(self):
        """Refresh statistics"""
        self.update_stats_cards()
        self.update_category_breakdown()

    def update_stats_cards(self):
        """Update the statistics cards"""
        # Clear existing cards
        for widget in self.stats_container.winfo_children():
            widget.destroy()

        # Get statistics
        stats = self.db.get_statistics()

        # Create grid layout for cards
        cards_data = [
            ("📚", "Total Books", stats['total_books'], "#3498db"),
            ("📑", "Categories", stats['total_categories'], "#9b59b6"),
            ("🔄", "Books Borrowed", stats['books_borrowed'], "#f39c12"),
            ("⭐", "Average Rating", f"{stats['average_rating']}/5", "#2ecc71"),
            ("✍️", "Top Author", stats['top_author'], "#e74c3c"),
            ("📅", "Added This Month", stats['recent_additions'], "#1abc9c"),
        ]

        # Create cards in a grid (3 columns)
        row_frame = None
        for i, (icon, label, value, color) in enumerate(cards_data):
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(self.stats_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)

            # Make top author card clickable
            if label == "Top Author":
                self.create_stat_card(row_frame, icon, label, value, color, clickable=True, click_value=stats['top_author'])
            else:
                self.create_stat_card(row_frame, icon, label, value, color)

    def create_stat_card(self, parent, icon: str, label: str, value, color: str, clickable: bool = False, click_value: str = None):
        """Create a statistics card"""
        card = ctk.CTkFrame(parent, fg_color=color, corner_radius=15)
        card.pack(side="left", fill="both", expand=True, padx=5)

        # Make clickable if requested
        if clickable and click_value and click_value != 'N/A':
            card.configure(cursor="hand2")
            card.bind("<Button-1>", lambda e: self.filter_by_author(click_value))

        # Content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Make content clickable too
        if clickable and click_value and click_value != 'N/A':
            content.configure(cursor="hand2")
            content.bind("<Button-1>", lambda e: self.filter_by_author(click_value))

        # Icon
        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=ctk.CTkFont(size=40)
        )
        icon_label.pack()
        if clickable and click_value and click_value != 'N/A':
            icon_label.configure(cursor="hand2")
            icon_label.bind("<Button-1>", lambda e: self.filter_by_author(click_value))

        # Value
        value_label = ctk.CTkLabel(
            content,
            text=str(value),
            font=ctk.CTkFont(size=32, weight="bold")
        )
        value_label.pack(pady=(5, 0))
        if clickable and click_value and click_value != 'N/A':
            value_label.configure(cursor="hand2")
            value_label.bind("<Button-1>", lambda e: self.filter_by_author(click_value))

        # Label
        label_widget = ctk.CTkLabel(
            content,
            text=label + (" (click to filter)" if clickable and click_value != 'N/A' else ""),
            font=ctk.CTkFont(size=14),
            text_color="gray90"
        )
        label_widget.pack()
        if clickable and click_value and click_value != 'N/A':
            label_widget.configure(cursor="hand2")
            label_widget.bind("<Button-1>", lambda e: self.filter_by_author(click_value))

    def update_category_breakdown(self):
        """Update category breakdown"""
        # Clear existing content
        for widget in self.category_container.winfo_children():
            widget.destroy()

        # Title
        ctk.CTkLabel(
            self.category_container,
            text="📑 Books by Category",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w", padx=20, pady=(10, 15))

        # Get category stats
        category_stats = self.db.get_category_stats()

        if not category_stats:
            ctk.CTkLabel(
                self.category_container,
                text="No categories found",
                text_color="gray"
            ).pack(pady=20)
            return

        # Calculate total books for percentage
        total_books = sum(cat['book_count'] for cat in category_stats)

        # Create category bars
        for category in category_stats:
            if category['book_count'] > 0:  # Only show categories with books
                self.create_category_bar(
                    category['name'],
                    category['book_count'],
                    total_books,
                    category.get('color', '#3498db'),
                    category['id']
                )

    def create_category_bar(self, name: str, count: int, total: int, color: str, category_id: int):
        """Create a category bar chart item"""
        container = ctk.CTkFrame(self.category_container, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=5)

        # Make clickable
        container.configure(cursor="hand2")
        container.bind("<Button-1>", lambda e: self.filter_by_category(name))

        # Category name and count
        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.pack(fill="x")
        info_frame.configure(cursor="hand2")
        info_frame.bind("<Button-1>", lambda e: self.filter_by_category(name))

        name_label = ctk.CTkLabel(
            info_frame,
            text=name,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
            width=150
        )
        name_label.pack(side="left")
        name_label.configure(cursor="hand2")
        name_label.bind("<Button-1>", lambda e: self.filter_by_category(name))

        count_label = ctk.CTkLabel(
            info_frame,
            text=f"{count} books",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w",
            width=80
        )
        count_label.pack(side="left")
        count_label.configure(cursor="hand2")
        count_label.bind("<Button-1>", lambda e: self.filter_by_category(name))

        # Percentage
        percentage = (count / total * 100) if total > 0 else 0
        percent_label = ctk.CTkLabel(
            info_frame,
            text=f"{percentage:.1f}%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color,
            anchor="e",
            width=60
        )
        percent_label.pack(side="right")
        percent_label.configure(cursor="hand2")
        percent_label.bind("<Button-1>", lambda e: self.filter_by_category(name))

        # Progress bar
        bar_frame = ctk.CTkFrame(container, fg_color="transparent")
        bar_frame.pack(fill="x", pady=(3, 0))
        bar_frame.configure(cursor="hand2")
        bar_frame.bind("<Button-1>", lambda e: self.filter_by_category(name))

        # Background bar
        bg_bar = ctk.CTkFrame(bar_frame, height=25, fg_color="#2b2b2b", corner_radius=10)
        bg_bar.pack(fill="x")
        bg_bar.configure(cursor="hand2")
        bg_bar.bind("<Button-1>", lambda e: self.filter_by_category(name))

        # Filled bar
        if percentage > 0:
            filled_bar = ctk.CTkFrame(
                bg_bar,
                height=25,
                fg_color=color,
                corner_radius=10
            )
            filled_bar.place(relx=0, rely=0, relwidth=percentage/100, relheight=1)
            filled_bar.configure(cursor="hand2")
            filled_bar.bind("<Button-1>", lambda e: self.filter_by_category(name))

    def filter_by_category(self, category_name: str):
        """Switch to Books tab and filter by category"""
        if self.main_window:
            # Switch to Books tab
            self.main_window.tabview.set("📚 Books")
            # Set the category filter
            self.main_window.books_view.category_filter.set(category_name)
            # Apply the filter
            self.main_window.books_view.filter_by_category(category_name)

    def filter_by_author(self, author_name: str):
        """Switch to Books tab and filter by author"""
        if self.main_window:
            # Switch to Books tab
            self.main_window.tabview.set("📚 Books")
            # Set the search text
            self.main_window.books_view.search_entry.delete(0, 'end')
            self.main_window.books_view.search_entry.insert(0, author_name)
            # Trigger search
            self.main_window.books_view.search_books()

    def create_chart_placeholder(self, parent, title: str, height: int = 250):
        """Create a placeholder for a chart"""
        chart_frame = ctk.CTkFrame(parent, height=height)
        chart_frame.pack(fill="x", padx=20, pady=10)
        chart_frame.pack_propagate(False)

        ctk.CTkLabel(
            chart_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        ctk.CTkLabel(
            chart_frame,
            text="📊\nChart visualization placeholder",
            font=ctk.CTkFont(size=40),
            text_color="gray"
        ).pack(expand=True)
