#!/bin/bash
# Academic Thesis AI - MCP Server Installation Script
# Installs all required MCP servers for academic research

set -e  # Exit on error

echo "🚀 Academic Thesis AI - MCP Server Setup"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if uv is installed (needed for arXiv server)
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  'uv' not found. Installing...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Check if npx is installed (needed for Smithery)
if ! command -v npx &> /dev/null; then
    echo -e "${RED}❌ 'npx' not found. Please install Node.js first.${NC}"
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✓${NC} Prerequisites check passed"
echo ""

# Detect IDE (Claude Code vs Cursor)
IDE_CONFIG_PATH=""
if [ -d "$HOME/.config/Claude Code" ]; then
    IDE_CONFIG_PATH="$HOME/.config/Claude Code/mcp_config.json"
    IDE_NAME="Claude Code"
elif [ -d "$HOME/.cursor" ]; then
    IDE_CONFIG_PATH="$HOME/.cursor/mcp_config.json"
    IDE_NAME="Cursor"
elif [ -d "$HOME/Library/Application Support/Claude" ]; then
    IDE_CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    IDE_NAME="Claude Desktop (macOS)"
elif [ -d "$HOME/Library/Application Support/Cursor" ]; then
    IDE_CONFIG_PATH="$HOME/Library/Application Support/Cursor/mcp_config.json"
    IDE_NAME="Cursor (macOS)"
else
    echo -e "${YELLOW}⚠️  Could not auto-detect IDE. Will create config in current directory.${NC}"
    IDE_CONFIG_PATH="./mcp_config.json"
    IDE_NAME="Manual"
fi

echo -e "📍 Detected IDE: ${GREEN}${IDE_NAME}${NC}"
echo -e "📁 Config path: ${IDE_CONFIG_PATH}"
echo ""

# Create config directory if it doesn't exist
mkdir -p "$(dirname "$IDE_CONFIG_PATH")"

# Install MCP servers
echo "📦 Installing MCP Servers..."
echo ""

# 1. arXiv MCP Server
echo -e "${YELLOW}[1/4]${NC} Installing arXiv MCP Server..."
if command -v smithery &> /dev/null; then
    npx -y @smithery/cli install arxiv-mcp-server --client claude 2>/dev/null || true
else
    uv tool install arxiv-mcp-server
fi
echo -e "${GREEN}✓${NC} arXiv MCP Server installed"
echo ""

# 2. Semantic Scholar MCP Server
echo -e "${YELLOW}[2/4]${NC} Installing Semantic Scholar MCP Server..."
if [ ! -d "$HOME/.mcp-servers/semantic-scholar" ]; then
    git clone https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server.git "$HOME/.mcp-servers/semantic-scholar" 2>/dev/null || true
    cd "$HOME/.mcp-servers/semantic-scholar"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q fastmcp semanticscholar
    deactivate
    cd - > /dev/null
fi
echo -e "${GREEN}✓${NC} Semantic Scholar MCP Server installed"
echo ""

# 3. Google Scholar MCP Server
echo -e "${YELLOW}[3/4]${NC} Installing Google Scholar MCP Server..."
if [ ! -d "$HOME/.mcp-servers/google-scholar" ]; then
    git clone https://github.com/JackKuo666/Google-Scholar-MCP-Server.git "$HOME/.mcp-servers/google-scholar" 2>/dev/null || true
    cd "$HOME/.mcp-servers/google-scholar"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    deactivate
    cd - > /dev/null
fi
echo -e "${GREEN}✓${NC} Google Scholar MCP Server installed"
echo ""

# 4. PubMed MCP Server
echo -e "${YELLOW}[4/4]${NC} Installing PubMed MCP Server..."
pip install -q mcp-simple-pubmed 2>/dev/null || true
echo -e "${GREEN}✓${NC} PubMed MCP Server installed"
echo ""

# Generate MCP configuration
echo "⚙️  Generating MCP configuration..."

PAPER_STORAGE="${PAPER_STORAGE_PATH:-$HOME/academic-thesis-ai/research/papers}"
mkdir -p "$PAPER_STORAGE"

cat > "$IDE_CONFIG_PATH" << EOF
{
  "mcpServers": {
    "arxiv": {
      "command": "uv",
      "args": [
        "tool",
        "run",
        "arxiv-mcp-server",
        "--storage-path",
        "$PAPER_STORAGE"
      ]
    },
    "semantic-scholar": {
      "command": "$HOME/.mcp-servers/semantic-scholar/venv/bin/python",
      "args": [
        "$HOME/.mcp-servers/semantic-scholar/run.py"
      ],
      "env": {
        "SEMANTIC_SCHOLAR_API_KEY": "${SEMANTIC_SCHOLAR_API_KEY:-}"
      }
    },
    "google-scholar": {
      "command": "$HOME/.mcp-servers/google-scholar/venv/bin/python",
      "args": [
        "$HOME/.mcp-servers/google-scholar/server.py"
      ]
    },
    "pubmed": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_simple_pubmed"
      ]
    }
  }
}
EOF

echo -e "${GREEN}✓${NC} Configuration generated at: $IDE_CONFIG_PATH"
echo ""

# Test installation
echo "🧪 Testing MCP servers..."
echo ""

# Simple test: check if commands exist
TESTS_PASSED=0
TESTS_TOTAL=4

# Test arXiv
if command -v arxiv-mcp-server &> /dev/null || [ -f "$HOME/.local/bin/arxiv-mcp-server" ]; then
    echo -e "${GREEN}✓${NC} arXiv server command found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} arXiv server command not found"
fi

# Test Semantic Scholar
if [ -f "$HOME/.mcp-servers/semantic-scholar/run.py" ]; then
    echo -e "${GREEN}✓${NC} Semantic Scholar server found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} Semantic Scholar server not found"
fi

# Test Google Scholar
if [ -f "$HOME/.mcp-servers/google-scholar/server.py" ]; then
    echo -e "${GREEN}✓${NC} Google Scholar server found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} Google Scholar server not found"
fi

# Test PubMed
if python3 -c "import mcp_simple_pubmed" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} PubMed server found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗${NC} PubMed server not found"
fi

echo ""
echo "========================================"
if [ $TESTS_PASSED -eq $TESTS_TOTAL ]; then
    echo -e "${GREEN}🎉 Installation complete! ($TESTS_PASSED/$TESTS_TOTAL servers ready)${NC}"
else
    echo -e "${YELLOW}⚠️  Installation partially complete ($TESTS_PASSED/$TESTS_TOTAL servers ready)${NC}"
fi
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Restart your IDE ($IDE_NAME)"
echo "2. Open the prompts/ folder"
echo "3. Start with prompts/00_WORKFLOW.md"
echo ""
echo "MCP servers will be available in your IDE chat!"
