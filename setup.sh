#!/bin/bash
# Academic Thesis AI - Quick Setup Script

set -e

echo "🎓 Academic Thesis AI - Setup"
echo "=============================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install pip."
    exit 1
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt -q || pip install -r requirements.txt -q
echo "✅ Python dependencies installed"

# Setup .env file
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "📝 IMPORTANT: Edit .env and add your API keys:"
    echo "   - ANTHROPIC_API_KEY (for Claude)"
    echo "   - OPENAI_API_KEY (for GPT)"
    echo "   - GOOGLE_API_KEY (for Gemini)"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Create project folders
echo ""
echo "📁 Creating project folders..."
mkdir -p research/{papers,output}
mkdir -p sections
echo "✅ Project folders created"

# Install MCP servers
echo ""
read -p "Install MCP servers now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    chmod +x mcp_servers/install_all.sh
    ./mcp_servers/install_all.sh
fi

# Make utilities executable
echo ""
echo "🔧 Setting up utilities..."
chmod +x utils/*.py
echo "✅ Utilities ready"

echo ""
echo "=============================="
echo "🎉 Setup complete!"
echo "=============================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Restart your IDE (Claude Code or Cursor)"
echo "3. Open prompts/00_WORKFLOW.md to start writing"
echo ""
echo "Quick commands:"
echo "  - Export PDF:  python utils/export.py --format pdf --output paper.pdf final_thesis.md"
echo "  - Check AI:    python utils/ai_detection.py paper.md"
echo "  - Validate bib: python utils/citations.py --validate references.bib"
echo ""
echo "📖 Documentation: README.md"
echo "⚖️ Ethics: ETHICS.md"
echo ""
echo "Happy writing! 🚀"
