# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in Academic Thesis AI, please report it privately.

### How to Report

**Do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security issues via one of these methods:

1. **GitHub Security Advisories** (Preferred)
   - Go to: https://github.com/federicodeponte/academic-thesis-ai/security/advisories
   - Click "New draft security advisory"
   - Provide detailed information about the vulnerability

2. **Email** (If GitHub Advisories is unavailable)
   - For urgent security matters, open a Discussion labeled "Security" with subject "[SECURITY - URGENT]"
   - Do not include vulnerability details publicly
   - We will provide private contact information within 24 hours

### What to Include

Please provide as much information as possible:

- **Type of vulnerability** (e.g., code injection, API key exposure, unauthorized access)
- **Location** (file path, line number, affected component)
- **Steps to reproduce** (detailed reproduction steps)
- **Potential impact** (what could an attacker do?)
- **Suggested fix** (if you have one)
- **Affected versions** (which versions are vulnerable)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Every 5 business days
- **Fix Timeline**: Depends on severity
  - **Critical**: 1-7 days
  - **High**: 7-30 days
  - **Medium**: 30-90 days
  - **Low**: Next scheduled release

### Disclosure Policy

- **Private disclosure first**: Allow us time to fix the issue
- **Coordinated disclosure**: We'll work with you on timing
- **Credit**: We'll acknowledge your contribution (unless you prefer to remain anonymous)
- **CVE assignment**: For serious vulnerabilities, we'll request a CVE

## Security Best Practices for Users

### API Key Protection

**CRITICAL:** Never commit API keys to Git or share them publicly.

```bash
# ✅ GOOD: Use environment variables
export GOOGLE_API_KEY="your-key-here"

# ❌ BAD: Hardcode in source files
api_key = "AIza..."  # DON'T DO THIS
```

### Safe Configuration

1. **Use .env files** (git ignored by default)
   ```bash
   cp .env.example .env
   # Edit .env with your keys
   ```

2. **Check .gitignore** before committing
   ```bash
   git status  # Ensure .env not tracked
   ```

3. **Rotate compromised keys immediately**
   - Google AI Studio: https://makersuite.google.com/app/apikey
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/settings/keys

### Input Validation

This tool uses user-provided research queries with LLM APIs. Be aware:

- **User input goes to external APIs** (Google, OpenAI, Anthropic)
- **Avoid sensitive data** in research queries
- **Review generated citations** for accuracy
- **Don't process untrusted markdown files** (potential for malicious LaTeX injection)

### Rate Limiting & Abuse Prevention

- **API rate limits** are enforced to prevent abuse
- **Concurrency limits** prevent overwhelming external services
- **Retry logic** has exponential backoff to avoid hammering APIs
- **Cost warnings** alert you to unexpected usage

## Known Security Considerations

### 1. LLM API Usage

- **Data sent to third parties**: Your research queries and thesis content are sent to LLM APIs
- **Privacy**: Review each API's privacy policy (Google, OpenAI, Anthropic)
- **Commercial use**: Ensure your API usage complies with terms of service

### 2. Citation Scraping

- **Web scraping risks**: Citation metadata is scraped from public sources
- **HTTPS verification**: We verify SSL certificates
- **Timeout limits**: Prevent indefinite hanging on slow/malicious servers
- **User-Agent**: We identify ourselves in HTTP headers

### 3. PDF Generation

- **LaTeX processing**: We use Pandoc/XeLaTeX which executes system commands
- **Sanitization**: Markdown is sanitized before LaTeX conversion
- **Temporary files**: Created in /tmp, cleaned up after processing
- **File permissions**: PDF output files use standard user permissions

### 4. Dependency Security

We use:
- **PyPI packages**: All dependencies from trusted sources
- **Version pinning**: Major versions pinned in requirements.txt
- **Regular updates**: Dependencies updated quarterly

**Run security scans:**
```bash
# Check for known vulnerabilities
pip install safety
safety check -r requirements.txt

# Or use GitHub Dependabot (automatic)
```

## Vulnerability Severity Classification

### Critical
- Remote code execution
- API key exposure to internet
- Unauthorized access to user data
- SQL injection, command injection

### High
- Privilege escalation
- Data leaks via logs/outputs
- Authentication bypass
- Cross-site scripting (XSS) in outputs

### Medium
- Denial of service
- Information disclosure
- Improper input validation
- Insecure defaults

### Low
- Non-security bugs
- Minor information leaks
- Issues requiring complex attack chains

## Security Updates

Security fixes are released as:
- **Patch releases** (e.g., 1.0.1) for minor fixes
- **Minor releases** (e.g., 1.1.0) for moderate fixes
- **Immediate hotfixes** for critical vulnerabilities

Subscribe to:
- GitHub Security Advisories (Watch → Custom → Security alerts)
- Release notifications (Watch → Custom → Releases)
- CHANGELOG.md for all changes

## Security Credits

We acknowledge security researchers who responsibly disclose vulnerabilities:

<!-- This section will be populated as researchers report issues -->

*No vulnerabilities have been reported yet.*

## Contact

For security concerns:
- **GitHub Advisories** (Preferred): https://github.com/federicodeponte/academic-thesis-ai/security/advisories
- **Urgent Issues**: Open a private Discussion with subject "[SECURITY - URGENT]"

For general questions:
- GitHub Issues: https://github.com/federicodeponte/academic-thesis-ai/issues
- Discussions: https://github.com/federicodeponte/academic-thesis-ai/discussions

---

**Last Updated**: November 20, 2025
