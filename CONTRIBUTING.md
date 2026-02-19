# Contributing to HealthyFoods2

Thank you for your interest in contributing to HealthyFoods2! This document provides guidelines for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- Clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- Clear and descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass
6. Update documentation
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

#### Pull Request Guidelines

- Follow the existing code style
- Write clear commit messages
- Include tests for new functionality
- Update documentation for API changes
- Ensure CI/CD pipeline passes
- Link related issues in the PR description

## Development Setup

### Prerequisites

- Python 3.11+
- Docker
- Git

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/RoseTechCyber/HealthyFoods2.git
cd HealthyFoods2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Copy environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
python -m uvicorn app.main:app --reload
```

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and concise
- Maximum line length: 100 characters

### Code Quality Tools

```bash
# Run linter
flake8 app/

# Run formatter
black app/

# Run type checker
mypy app/

# Run security checks
bandit -r app/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_orders.py
```

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(orders): add real-time order tracking

Implemented WebSocket-based real-time tracking for orders.
Customers can now see live updates on their order status.

Closes #123
```

## Documentation

- Update README.md for user-facing changes
- Update API_DOCUMENTATION.md for API changes
- Add inline comments for complex logic
- Update deployment guides if infrastructure changes

## Testing Requirements

All contributions must include appropriate tests:

- Unit tests for business logic
- Integration tests for API endpoints
- End-to-end tests for critical workflows
- Maintain or improve code coverage

## Review Process

1. Automated checks must pass (CI/CD pipeline)
2. Code review by at least one maintainer
3. All comments addressed
4. Documentation updated
5. Changes tested in staging environment

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Getting Help

- Join our community chat (link)
- Check existing documentation
- Ask questions in GitHub Discussions
- Email: support@rosetechcyber.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- README.md Contributors section
- Release notes
- Annual contributor report

Thank you for contributing to HealthyFoods2! 🎉
