# Contributing to OpenDraft

Thank you for considering contributing! This project helps researchers worldwide conduct better academic research with AI assistance.

## 🎉 First Time Contributors - Start Here!

**Never contributed to open source before?** No problem! We welcome beginners.

### Easy Ways to Contribute (No Coding Required!)

1. **Fix Typos in Documentation** (5-10 minutes)
   ```bash
   # 1. Click "Edit" on any .md file in GitHub
   # 2. Fix the typo
   # 3. Click "Propose changes"
   # 4. Submit pull request
   ```
   That's it! We'll review and merge.

2. **Improve Examples** (15-30 minutes)
   - Add comments to example theses
   - Create new example use cases
   - Improve example README files

3. **Test and Report Bugs** (30 minutes)
   - Try generating a thesis on your topic
   - Report issues using our [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml)
   - Include what went wrong and your setup details

4. **Share Your Experience** (10 minutes)
   - Write about how you used the tool
   - Share tips in [GitHub Discussions](../../discussions)
   - Help other users with questions

### Good First Issues

Look for issues labeled [`good-first-issue`](../../issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - these are:
- Well-documented
- Relatively simple
- Don't require deep codebase knowledge
- Have clear acceptance criteria

**Need help?** Comment on the issue or ask in [Discussions](../../discussions). We're here to help!

---

## Table of Contents

- [First Time Contributors](#-first-time-contributors---start-here)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Testing Guidelines](#testing-guidelines)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)

---

## How to Contribute

### 1. Report Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, package version)
- Relevant error messages and logs

### 2. Suggest Features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) and explain:
- The problem you're trying to solve
- Your proposed solution
- Specific use cases in academic research
- Priority level for your workflow

### 3. Improve Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples and use cases
- Improve code comments and docstrings
- Update outdated information
- Add tutorials or guides

### 4. Add MCP Servers

Expand integration with academic databases:
- New academic databases (IEEE, ACM, arXiv, etc.)
- Follow existing patterns in `mcp_servers/`
- Include comprehensive error handling
- Test with real-world data
- Document API requirements and limitations

### 5. Enhance Agents

Improve AI agent capabilities:
- Better prompt engineering for more accurate results
- New specialized agents for specific research tasks
- Improved output formatting and parsing
- Better context management
- Enhanced error handling and retries

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, or virtualenv)

### Initial Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/opendraft.git
cd opendraft

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies
pip install -r requirements-dev.txt  # If available

# 5. Copy environment template
cp .env.example .env

# 6. Configure your API keys
# Edit .env with your API credentials
```

### Environment Variables

Required API keys (add to `.env`):
```bash
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here  # If using Claude
OPENAI_API_KEY=your_openai_key_here  # If using OpenAI
```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update your main branch
git checkout main
git pull origin main

# Create a new feature branch
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code patterns
- Add comments for complex logic
- Update documentation as needed
- Write tests for new functionality

### 3. Test Your Changes

```bash
# Run the full test suite
python -m pytest

# Run specific test file
python -m pytest tests/test_your_feature.py

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Manual testing
python main.py  # Test your feature interactively
```

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add support for new database"
# See Commit Guidelines below for format
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Then create a Pull Request on GitHub
# Use the PR template and fill in all sections
```

## Testing Guidelines

### Writing Tests

Tests should be:
- **Isolated**: Each test should be independent
- **Repeatable**: Same input = same output
- **Fast**: Keep tests quick to run
- **Clear**: Easy to understand what's being tested

### Test Structure

```python
# tests/test_example.py
import pytest
from your_module import your_function

def test_your_function_with_valid_input():
    """Test that your_function works with valid input."""
    # Arrange
    input_data = "test data"
    expected_output = "expected result"

    # Act
    result = your_function(input_data)

    # Assert
    assert result == expected_output

def test_your_function_handles_errors():
    """Test that your_function handles errors gracefully."""
    with pytest.raises(ValueError):
        your_function(invalid_input)
```

### Test Coverage

Aim for:
- **Core functionality**: 90%+ coverage
- **Utility functions**: 80%+ coverage
- **Edge cases**: Test error handling, empty inputs, boundary conditions
- **Integration**: Test component interactions

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_agents/

# With verbose output
pytest -v

# With coverage report
pytest --cov=. --cov-report=term-missing

# Stop on first failure
pytest -x

# Run only tests that failed last time
pytest --lf
```

## Code Style Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Keep functions focused and small (< 50 lines ideally)
- Use type hints where applicable
- Write docstrings for all public functions/classes

### Code Formatting

```bash
# Format code with black (if configured)
black .

# Check with flake8
flake8 .

# Sort imports with isort
isort .
```

### Docstring Format

```python
def process_research_paper(paper_text: str, query: str) -> dict:
    """
    Process a research paper and extract relevant information.

    Args:
        paper_text (str): Full text of the research paper
        query (str): Research query or topic of interest

    Returns:
        dict: Extracted information including:
            - summary (str): Paper summary
            - key_findings (list): Main findings
            - citations (list): Referenced papers

    Raises:
        ValueError: If paper_text is empty
        APIError: If API call fails

    Example:
        >>> paper = "This is a research paper..."
        >>> result = process_research_paper(paper, "machine learning")
        >>> print(result['summary'])
    """
    # Implementation here
    pass
```

### Naming Conventions

- **Functions/variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Private methods**: `_leading_underscore`
- **Protected**: `_single_leading_underscore`

## Commit Guidelines

### Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(agents): add literature review agent
fix(retry): handle rate limiting correctly
docs(readme): update installation instructions
test(mcp): add tests for IEEE database integration
refactor(utils): simplify error handling logic
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with main
- [ ] Self-review completed

### PR Description

Use the [PR template](.github/pull_request_template.md) and include:
- Clear description of changes
- Related issues (if applicable)
- Testing performed
- Screenshots/examples (if UI changes)
- Breaking changes noted

### Review Process

1. Automated checks must pass (if CI/CD configured)
2. At least one maintainer review required
3. Address all review comments
4. Keep PR focused (one feature/fix per PR)
5. Be responsive to feedback

### After Approval

- Maintainers will merge your PR
- Your changes will be included in the next release
- You'll be added to contributors list

## Community Guidelines

### Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to maintaining a professional, respectful academic community.

### Communication

- **Issues**: Bug reports and feature requests
- **Discussions**: Questions, ideas, and general discussion
- **Pull Requests**: Code contributions
- **Security**: For vulnerabilities only (see [SECURITY.md](SECURITY.md))

### Maintainer Response Time Commitments

We strive to respond to contributions in a timely manner:

| Type | Target Response Time | Notes |
|------|---------------------|-------|
| **Security Issues** | Within 48 hours | See [SECURITY.md](SECURITY.md) |
| **Bug Reports** | Within 1 week | Acknowledgment + initial triage |
| **Feature Requests** | Within 2 weeks | Feedback on feasibility |
| **Pull Requests** | Within 1 week | Initial review + feedback |
| **Discussions** | Within 3-5 days | Community-driven, best effort |

**Important:**
- Response ≠ Fix - We'll acknowledge and provide timeline
- Complex issues may take longer to resolve
- Community PRs are reviewed before maintainer PRs
- Critical bugs and security issues are prioritized

**If you don't get a response:**
1. Check if you followed the template
2. Ping the issue/PR after the response window
3. Ask in [Discussions](../../discussions) for visibility

### Getting Help

- Check existing [documentation](README.md)
- Search [existing issues](../../issues)
- Ask in [Discussions](../../discussions)
- Review [examples](examples/)

### Academic Integrity

When contributing, ensure:
- All sources are properly cited
- No plagiarized code
- Methodology is transparent
- Research ethics are followed
- Proper attribution for ideas and implementations

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if file exists)
- Acknowledged in release notes
- Credited in documentation (for significant contributions)

## Questions?

- Open a [Discussion](../../discussions) for general questions
- Create an [Issue](../../issues) for bugs or feature requests
- Check [existing documentation](README.md) first

Thank you for contributing to OpenDraft! Your efforts help researchers worldwide. 🎓
