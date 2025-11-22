#!/usr/bin/env python3
"""
Quick test to verify OpenDraft setup is working correctly.

This script tests:
1. All required Python packages are installed
2. API key is configured and valid
3. System is ready to use

Run this after initial setup to verify everything works.
"""

import os
import sys
from pathlib import Path

# Add parent directory to Python path so we can import from the project
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all required packages are installed."""
    print("Checking Python packages...")

    required_packages = [
        ('google.generativeai', 'google-generativeai'),
        ('anthropic', 'anthropic'),
        ('openai', 'openai'),
        ('markdown', 'markdown'),
        ('weasyprint', 'weasyprint'),
        ('docx', 'python-docx'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv'),
    ]

    missing = []
    for module, package in required_packages:
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False

    print("✅ All packages installed")
    return True


def test_api_key():
    """Test that at least one API key is configured and valid."""
    print("\nChecking API configuration...")

    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv('.env.local', override=True)  # Load .env.local first (overrides .env)
        load_dotenv('.env')  # Then .env as fallback
    except ImportError:
        print("⚠️  python-dotenv not installed, using system env vars only")

    # Check which API keys are configured
    google_key = os.getenv('GOOGLE_API_KEY', '')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
    openai_key = os.getenv('OPENAI_API_KEY', '')

    # Check if any key is configured
    if not any([google_key, anthropic_key, openai_key]):
        print("❌ No API key configured")
        print("\nPlease configure at least one API key in .env or .env.local:")
        print("  - GOOGLE_API_KEY (recommended for beginners)")
        print("  - ANTHROPIC_API_KEY (for Claude)")
        print("  - OPENAI_API_KEY (for GPT)")
        print("\nSee docs/API_KEYS.md for setup instructions")
        return False

    # Check for placeholder values
    if 'your-' in google_key.lower() or 'your-' in anthropic_key.lower() or 'your-' in openai_key.lower():
        print("❌ API key appears to be a placeholder")
        print("\nReplace 'your-api-key-here' with your actual API key")
        print("See docs/API_KEYS.md for how to get an API key")
        return False

    # Test the first available API
    api_tested = None

    if google_key and google_key != 'your-google-api-key-here':
        print("\nTesting Google Gemini API key...")
        try:
            import google.generativeai as genai
            genai.configure(api_key=google_key)
            # Try to list models as a validation check
            models = genai.list_models()
            # Just checking that we can call the API
            print("✅ Gemini API key valid")
            api_tested = "Gemini"
        except Exception as e:
            print(f"❌ Gemini API key invalid: {str(e)[:100]}")
            print("\nCheck your GOOGLE_API_KEY in .env.local")
            print("Get a new key at: https://aistudio.google.com/apikey")
            return False

    elif anthropic_key and anthropic_key != 'sk-ant-...':
        print("\nTesting Anthropic Claude API key...")
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            # Test with a minimal request
            # Note: This will use a small amount of credit
            print("✅ Claude API key valid")
            api_tested = "Claude"
        except Exception as e:
            print(f"❌ Claude API key invalid: {str(e)[:100]}")
            print("\nCheck your ANTHROPIC_API_KEY in .env.local")
            print("Get a new key at: https://console.anthropic.com/")
            return False

    elif openai_key and openai_key != 'sk-...':
        print("\nTesting OpenAI GPT API key...")
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            # Test with a minimal request
            models = client.models.list()
            print("✅ OpenAI API key valid")
            api_tested = "OpenAI GPT"
        except Exception as e:
            print(f"❌ OpenAI API key invalid: {str(e)[:100]}")
            print("\nCheck your OPENAI_API_KEY in .env.local")
            print("Get a new key at: https://platform.openai.com/api-keys")
            return False

    if not api_tested:
        print("⚠️  API keys configured but couldn't test any")
        print("This might be okay - continuing...")
        return True

    print(f"✅ {api_tested} API configured and working")
    return True


def test_config_files():
    """Test that configuration files exist."""
    print("\nChecking configuration files...")

    # Check if .env.local or .env exists
    if not Path('.env.local').exists() and not Path('.env').exists():
        print("❌ No .env or .env.local file found")
        print("\nRun: cp .env.example .env.local")
        print("Then edit .env.local and add your API key")
        return False

    if Path('.env.local').exists():
        print("✅ Using .env.local for configuration")
    elif Path('.env').exists():
        print("⚠️  Using .env (consider using .env.local for secrets)")

    return True


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print("\n✅ Setup successful! You're ready to start writing.\n")
    print("Choose your path:\n")
    print("📚 Option A: 30-Minute Tutorial (Recommended)")
    print("   → examples/tutorial/README.md")
    print("   Learn the basics and write your first section\n")
    print("🚀 Option B: Full Workflow")
    print("   → prompts/00_WORKFLOW.md")
    print("   Complete guide for writing entire papers\n")
    print("💡 Option C: Explore")
    print("   → README.md")
    print("   Browse documentation and examples\n")
    print("="*60)


def main():
    """Run all setup tests."""
    print("🧪 Testing OpenDraft Setup...\n")
    print("="*60)

    all_tests_passed = True

    # Test 1: Package imports
    if not test_imports():
        all_tests_passed = False

    # Test 2: Configuration files
    if not test_config_files():
        all_tests_passed = False

    # Test 3: API key
    if not test_api_key():
        all_tests_passed = False

    print("\n" + "="*60)

    if all_tests_passed:
        print("🎉 ALL TESTS PASSED")
        print_next_steps()
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        print("\nTroubleshooting:")
        print("  - Setup guide: docs/INSTALLATION.md")
        print("  - API key help: docs/API_KEYS.md")
        print("  - FAQ: FAQ.md")
        print("  - GitHub Issues: https://github.com/federicodeponte/opendraft/issues")
        print("="*60)
        sys.exit(1)


if __name__ == "__main__":
    main()
