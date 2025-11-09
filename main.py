#!/usr/bin/env python3
"""
BookKeeper Pro - Modern Book Management System
Main application entry point
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.views.main_window import MainWindow


def main():
    """Main application entry point"""
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
