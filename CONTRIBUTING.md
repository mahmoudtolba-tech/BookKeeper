# Contributing to BookKeeper Pro

Thank you for your interest in contributing to BookKeeper Pro! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please create an issue with:
- Clear description of the feature
- Use cases and benefits
- Potential implementation ideas (optional)

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/BookKeeper.git
   cd BookKeeper
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Set up development environment**
   ```bash
   ./setup.sh  # or setup.bat on Windows
   ```

4. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

5. **Test your changes**
   - Make sure the application runs without errors
   - Test all affected functionality
   - Test on different operating systems if possible

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add some AmazingFeature"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/AmazingFeature
   ```

8. **Create a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Wait for review

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example
```python
def add_book(self, title: str, author: str, **kwargs) -> int:
    """
    Add a new book to the database.

    Args:
        title: Book title
        author: Book author
        **kwargs: Additional book attributes

    Returns:
        int: ID of the newly added book
    """
    # Implementation here
    pass
```

### File Organization
- Models in `src/models/`
- Views in `src/views/`
- Utilities in `src/utils/`
- Keep files focused on a single responsibility

### UI Guidelines
- Use CustomTkinter components consistently
- Follow existing color schemes
- Make UI responsive
- Add proper labels and tooltips
- Ensure accessibility

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Code editor (VS Code recommended)

### Recommended VS Code Extensions
- Python
- Pylance
- Python Docstring Generator
- GitLens

### Running Tests
Currently, BookKeeper Pro doesn't have automated tests. This is a great area for contribution!

## Project Structure

```
BookKeeper/
├── src/
│   ├── models/         # Database models
│   ├── views/          # UI components
│   └── utils/          # Utility functions
├── assets/             # Images, icons
├── data/              # Database files
├── exports/           # Export files
├── backups/           # Database backups
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## Areas for Contribution

### High Priority
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Documentation improvements

### Features
- [ ] Book cover image management
- [ ] Barcode scanning
- [ ] Reading progress tracking
- [ ] Cloud sync
- [ ] Advanced charts and analytics
- [ ] Email notifications

### UI/UX
- [ ] Keyboard shortcuts
- [ ] Dark theme improvements
- [ ] Accessibility features
- [ ] Mobile-responsive design
- [ ] Custom themes

## Questions?

Feel free to create an issue with your question or reach out to the maintainers.

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to learn and improve BookKeeper Pro together.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to BookKeeper Pro! 🎉
