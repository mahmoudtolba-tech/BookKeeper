# 📖 BookKeeper Pro - Modern Book Management System

A feature-rich, modern book management application for bookworms and book stores. Built with Python and CustomTkinter for a sleek, cross-platform experience.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 📚 Book Management
- **Complete Catalog**: Manage title, author, ISBN, year, publisher, pages, language, and more
- **Rich Descriptions**: Add detailed descriptions and notes for each book
- **Cover Images**: Support for book cover images
- **Rating System**: Rate books from 1-5 stars
- **Categories**: Organize books into colorful, customizable categories
- **Advanced Search**: Search by title, author, ISBN, or description
- **Category Filtering**: Quick filter by category

### 🔄 Lending System
- **Track Borrowed Books**: Keep track of who borrowed which books
- **Borrower Information**: Store borrower name and contact details
- **Due Dates**: Set and track expected return dates
- **Overdue Alerts**: Visual indicators for overdue books
- **Lending History**: Complete history of all book lendings
- **Notes**: Add notes to each lending transaction

### 📊 Statistics Dashboard
- **Total Books Count**: View your entire collection size
- **Category Breakdown**: Visual breakdown of books by category
- **Currently Borrowed**: See how many books are currently out
- **Average Rating**: Track your average book rating
- **Top Authors**: Identify your most-read authors
- **Recent Additions**: Track books added in the last 30 days

### 💾 Data Management
- **Export to CSV**: Export your entire library to CSV format
- **Import from CSV**: Bulk import books from CSV files
- **Export to JSON**: Export with full metadata
- **Database Backup**: Create backups of your database
- **Database Restore**: Restore from previous backups

### 🎨 Modern UI
- **Dark/Light Theme**: Switch between dark and light modes
- **Responsive Design**: Adapts to different window sizes
- **Tabbed Interface**: Organized into Books, Lending, Statistics, and Settings
- **Color-Coded Categories**: Visual category organization
- **Smooth Animations**: Modern, polished interface
- **Intuitive Navigation**: Easy-to-use interface for all skill levels

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- tkinter (GUI library - usually comes with Python on Windows/Mac)

**Linux users:** You may need to install tkinter separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

### Installation & Setup

#### Linux/Mac
```bash
# Clone or download the repository
cd BookKeeper

# Run the setup script (creates venv and installs dependencies)
./setup.sh

# Run the application
./run.sh
```

#### Windows
```cmd
# Clone or download the repository
cd BookKeeper

# Run the setup script (creates venv and installs dependencies)
setup.bat

# Run the application
run.bat
```

### Manual Setup
If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🏗️ Building Executables

You can create standalone executables for distribution:

### Linux/Mac
```bash
# Create a single executable file
./build.sh --onefile

# Or create a directory with executable and dependencies
./build.sh --onedir

# Custom name
./build.sh --onefile --name MyBookKeeper
```

### Windows
```cmd
# Create a single executable file
build.bat --onefile

# Or create a directory with executable and dependencies
build.bat --onedir

# Custom name
build.bat --onefile --name MyBookKeeper
```

The executable will be created in the `dist/` directory.

### Build Options
- `--onefile`: Create a single executable file (default)
- `--onedir`: Create a directory with executable and dependencies
- `--name NAME`: Set custom executable name
- `--help`: Show help message

## 📖 Usage Guide

### Adding Books
1. Navigate to the **Books** tab
2. Click **➕ Add New Book**
3. Fill in the book details (Title and Author are required)
4. Select a category and add a rating
5. Click **Save**

### Searching Books
1. Use the search bar at the top of the Books tab
2. Type any keyword (title, author, ISBN)
3. Results update in real-time
4. Use the category filter for more specific searches

### Lending Books
1. Navigate to the **Lending** tab
2. Click **➕ Lend a Book**
3. Select the book and enter borrower information
4. Set expected return date
5. Add optional notes
6. Click **Lend Book**

### Returning Books
1. Navigate to the **Lending** tab
2. Find the borrowed book in the list
3. Click **✓ Mark as Returned**

### Viewing Statistics
1. Navigate to the **Statistics** tab
2. View comprehensive statistics about your library
3. See category breakdowns and trends
4. Click **🔄 Refresh** to update statistics

### Exporting Data
1. Navigate to the **Settings** tab
2. Click **📤 Export to CSV** or **Export to JSON**
3. File will be saved in the `exports/` directory

### Importing Data
1. Navigate to the **Settings** tab
2. Click **📥 Import from CSV**
3. Select your CSV file
4. Books will be imported automatically

### Backing Up Database
1. Navigate to the **Settings** tab
2. Click **💾 Backup Database**
3. Backup will be saved in the `backups/` directory

## 🗂️ Project Structure

```
BookKeeper/
├── src/
│   ├── models/
│   │   └── database.py          # Database models and operations
│   ├── views/
│   │   ├── main_window.py       # Main application window
│   │   ├── books_view.py        # Books management interface
│   │   ├── lending_view.py      # Lending management interface
│   │   └── statistics_view.py   # Statistics dashboard
│   └── utils/
│       └── export_import.py     # Export/import utilities
├── data/                        # Database files
├── exports/                     # Exported data files
├── backups/                     # Database backups
├── assets/                      # Images and icons
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── setup.sh / setup.bat        # Setup scripts
├── run.sh / run.bat            # Run scripts
├── build.sh / build.bat        # Build scripts
└── README.md                    # This file
```

## 🔧 Technical Details

### Technologies Used
- **Python 3.8+**: Core programming language
- **CustomTkinter**: Modern UI framework
- **SQLite3**: Database engine
- **Pillow**: Image processing
- **PyInstaller**: Executable builder

### Database Schema
- **books**: Main books table with all book information
- **categories**: Book categories with colors
- **lending**: Lending transactions and history
- **notes**: Book notes and reviews

### Key Features Implementation
- **MVC Pattern**: Separation of models, views, and controllers
- **SQLite Database**: Efficient local database with foreign keys
- **Virtual Environment**: Isolated dependency management
- **Cross-Platform**: Works on Windows, Mac, and Linux
- **Modular Design**: Easy to extend and maintain

## 🎯 Roadmap

Future enhancements planned:
- [ ] Book cover image management
- [ ] Barcode scanning for ISBN
- [ ] Reading progress tracking
- [ ] Multiple user accounts
- [ ] Cloud sync capabilities
- [ ] Mobile app companion
- [ ] Advanced analytics and charts
- [ ] Wishlist management
- [ ] Integration with online book databases
- [ ] Email reminders for overdue books

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Author

- **Mahmoud Tolba** – *Solo Developer & Creator*  
  [@mahmoudtolba-tech](https://github.com/mahmoudtolba-tech)

## 🙏 Acknowledgments

- CustomTkinter library for the modern UI components
- The Python community for excellent documentation and support
- All bookworms and book stores who inspired this project

## 📧 Support

If you encounter any issues or have questions:
1. Check the documentation above
2. Search existing issues
3. Create a new issue with detailed information

## 🌟 Show Your Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 📖 Improving documentation
- 🔀 Contributing code

---

**Made with ❤️ for bookworms and book stores**

Perfect for:
- Personal book collections
- Small libraries
- Book stores
- Book clubs
- Schools and educational institutions
