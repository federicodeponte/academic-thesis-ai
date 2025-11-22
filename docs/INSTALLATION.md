# Installation & Troubleshooting Guide

Detailed setup instructions and solutions to common problems.

---

## Prerequisites

### System Requirements
- **OS:** Windows 10+, macOS 10.15+, or Linux
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Disk Space:** 500MB for dependencies
- **Internet:** Required for AI API calls

### Check Your Python Version

```bash
python3 --version
```

Should show `Python 3.8.x` or higher.

**Don't have Python?**
- **macOS:** `brew install python3`
- **Ubuntu/Debian:** `sudo apt install python3 python3-pip`
- **Windows:** Download from https://python.org (check "Add to PATH")

---

## Installation Steps

### Step 1: Clone Repository

```bash
git clone https://github.com/federicodeponte/opendraft.git
cd opendraft
```

### Step 2: Create Virtual Environment (Recommended)

**Why use venv?**
- Isolates dependencies from system Python
- Prevents conflicts with other projects
- Makes cleanup easy (just delete venv/ folder)

**Create venv:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

**You'll know it worked when your prompt shows `(venv)`**

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**This installs:**
- google-generativeai (for Gemini)
- anthropic (for Claude)
- openai (for GPT)
- markdown, weasyprint, python-docx (for exports)
- requests, python-dotenv (utilities)

**Expected time:** 2-5 minutes depending on internet speed

### Step 4: Configure API Key

```bash
# Copy template to .env.local (recommended)
cp .env.example .env.local

# Edit .env.local and add your API key
# See docs/API_KEYS.md for how to get one
```

### Step 5: Verify Setup

```bash
python examples/quick_test.py
```

**Success looks like:**
```
✅ All packages installed
✅ API key valid
✅ Setup successful!
```

---

## Common Installation Issues

### Issue: "python3: command not found"

**Cause:** Python not installed or not in PATH

**Solutions:**
```bash
# Try "python" instead of "python3"
python --version

# If that works, use "python" in all commands
# If not, install Python first
```

**macOS:** `brew install python3`
**Ubuntu:** `sudo apt install python3`
**Windows:** Download from python.org

### Issue: "pip: command not found"

**Cause:** pip not installed

**Solution:**
```bash
# macOS/Linux
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

### Issue: "Permission denied" when installing packages

**Cause:** Trying to install globally without sudo

**Solutions:**

**Option A: Use virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Option B: Install with --user flag**
```bash
pip install --user -r requirements.txt
```

**Option C: Use sudo (not recommended)**
```bash
sudo pip install -r requirements.txt
```

### Issue: "SSL: CERTIFICATE_VERIFY_FAILED"

**Cause:** Firewall or proxy blocking HTTPS

**Solutions:**

**If you're behind corporate firewall:**
```bash
# Set proxy
export HTTP_PROXY=http://proxy.company.com:port
export HTTPS_PROXY=http://proxy.company.com:port

# Then retry installation
pip install -r requirements.txt
```

**If using macOS:**
```bash
# Install certificates
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Issue: "ModuleNotFoundError" when running code

**Cause:** Virtual environment not activated or packages not installed

**Solution:**
```bash
# Make sure venv is activated (you see "(venv)" in prompt)
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: WeasyPrint installation fails

**WeasyPrint** has system dependencies.

**macOS:**
```bash
brew install pango
pip install weasyprint
```

**Ubuntu/Debian:**
```bash
sudo apt install libpango-1.0-0 libpangocairo-1.0-0
pip install weasyprint
```

**Windows:**
Follow: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows

**Alternative:** Use python-docx only (Word export)

### Issue: "No module named 'google.generativeai'"

**Cause:** Package not installed correctly

**Solution:**
```bash
# Reinstall specifically
pip install --upgrade google-generativeai

# Or reinstall all
pip install -r requirements.txt --force-reinstall
```

---

## Platform-Specific Guides

### macOS Setup

```bash
# 1. Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python3

# 3. Clone and setup
git clone https://github.com/federicodeponte/opendraft.git
cd opendraft
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env.local
# Edit .env.local with your favorite editor

# 5. Test
python examples/quick_test.py
```

### Windows Setup

```powershell
# 1. Install Python from python.org
# Check "Add Python to PATH" during installation

# 2. Clone and setup
git clone https://github.com/federicodeponte/opendraft.git
cd opendraft
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure API key
copy .env.example .env.local
# Edit .env.local with Notepad

# 4. Test
python examples\quick_test.py
```

### Linux Setup (Ubuntu/Debian)

```bash
# 1. Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# 2. Clone and setup
git clone https://github.com/federicodeponte/opendraft.git
cd opendraft
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env.local
nano .env.local  # or vim, emacs, etc.

# 4. Test
python examples/quick_test.py
```

---

## Advanced Setup

### Using Multiple Python Versions

If you have multiple Python versions:

```bash
# Use specific version
python3.10 -m venv venv
# or
python3.11 -m venv venv
```

### Installing in Editable Mode

For development:

```bash
pip install -e .
```

This lets you modify code without reinstalling.

### Upgrading Dependencies

```bash
# Upgrade all packages
pip install --upgrade -r requirements.txt

# Or upgrade specific package
pip install --upgrade google-generativeai
```

---

## Uninstallation

### Remove Everything

```bash
# Delete virtual environment
rm -rf venv/

# Delete repository
cd ..
rm -rf opendraft/
```

### Keep Config, Remove Code

```bash
# Backup your .env.local
cp .env.local ~/academic-thesis-backup.env

# Delete repo
cd ..
rm -rf opendraft/

# Later, restore:
# cp ~/academic-thesis-backup.env opendraft/.env.local
```

---

## Verification Checklist

After installation, verify:

- [ ] `python3 --version` shows 3.8+
- [ ] `which python3` shows path (or `where python3` on Windows)
- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] `pip list` shows all packages installed
- [ ] `.env.local` exists with API key
- [ ] `python examples/quick_test.py` passes all tests

If all checkboxes pass, you're ready!

---

## Still Having Issues?

**Check:**
- [FAQ.md](../FAQ.md) - Common questions
- [docs/API_KEYS.md](API_KEYS.md) - API setup help
- [GitHub Issues](https://github.com/federicodeponte/opendraft/issues) - Known problems

**Get Help:**
1. Search existing GitHub issues
2. Check FAQ
3. Open new issue with details:
   - OS and version
   - Python version
   - Error message
   - What you tried

We're here to help!
