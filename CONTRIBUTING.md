# Contributing to SourceGraph MCP

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/dalebrubaker/sourcegraph-mcp/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, SourceGraph version)
   - Relevant logs or error messages

### Suggesting Features

1. Check [Discussions](https://github.com/dalebrubaker/sourcegraph-mcp/discussions) first
2. Create a new discussion or issue describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Any alternatives you've considered
   - How it benefits other users

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly
5. Commit with clear messages: `git commit -m "Add feature: description"`
6. Push to your fork: `git push origin feature/my-feature`
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/dalebrubaker/sourcegraph-mcp.git
cd sourcegraph-mcp

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

## Code Style

- Follow [PEP 8](https://pep8.org/) Python style guide
- Use type hints where applicable
- Add docstrings for functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names

## Testing

Before submitting a PR:

1. Test with your local SourceGraph instance
2. Test with different query types
3. Verify error handling
4. Check that `test_connection.py` passes

```bash
python test_connection.py
```

## Documentation

- Update README.md if you add features
- Add examples for new query types
- Update SETUP.md if installation changes
- Comment complex code sections

## Commit Messages

Use clear, descriptive commit messages:

```
Add support for repository filters

- Implement repo: prefix in queries
- Add tests for repository filtering
- Update documentation with examples
```

## What We're Looking For

Particularly welcome contributions:

- **Bug fixes** - Always appreciated!
- **Documentation improvements** - Help others understand the project
- **New features** - Search filters, output formats, etc.
- **Examples** - Real-world usage examples
- **Performance improvements** - Make queries faster
- **Error handling** - Better error messages and recovery
- **Testing** - Automated tests would be great

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions

## Questions?

- Open a [Discussion](https://github.com/dalebrubaker/sourcegraph-mcp/discussions)
- Reach out in your Pull Request
- Check existing issues and PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make SourceGraph MCP better! 🎉
