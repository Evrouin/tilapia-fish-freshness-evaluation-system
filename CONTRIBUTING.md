# Contributing to Tilapia Fish Freshness Evaluation System

Thank you for your interest in contributing to this project! This document provides guidelines for contributing.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Evrouin/tilapia-fish-freshness-evaluation-system.git
   cd tilapia-fish-freshness-evaluation-system
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   make install-dev
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Quality
- Run `make format` to format code with Black and isort
- Run `make lint` to check code with flake8
- Run `make type-check` to run mypy type checking
- Run `make test` to run tests
- Run `make check-all` to run all quality checks

### Git Workflow
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run quality checks: `make check-all`
4. Commit your changes with descriptive messages
5. Push to your fork and create a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

### Testing
- Write tests for new functionality
- Ensure all tests pass before submitting PR
- Aim for good test coverage

## Project Structure

```
src/tilapia_freshness/
├── models/          # ML models (YOLO, GrabCut, Analyzer)
├── gui/             # GUI components
├── utils/           # Utility functions
├── enums/           # Enums and constants
├── config/          # Configuration management
└── exceptions/      # Custom exceptions
```

## Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Pull Request Guidelines

- Provide clear description of changes
- Reference related issues
- Include tests for new functionality
- Ensure all CI checks pass
- Update documentation if needed

## Questions?

Feel free to open an issue for questions or discussions about the project.
