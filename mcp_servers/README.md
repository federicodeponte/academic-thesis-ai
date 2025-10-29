# MCP Servers for Academic Research

This directory contains installation scripts for Model Context Protocol (MCP) servers that provide access to academic databases.

## Installed Servers

### 1. arXiv MCP Server
- **Source**: https://github.com/blazickjp/arxiv-mcp-server
- **Coverage**: Physics, Computer Science, Mathematics, Biology
- **Capabilities**:
  - Search papers by topic, author, category
  - Download and read full PDF content
  - Filter by date range
  - Local paper storage for faster access

### 2. Semantic Scholar MCP Server
- **Source**: https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server
- **Coverage**: 200M+ papers across all academic fields
- **Capabilities**:
  - Full-text search with advanced filters
  - Citation network exploration
  - Author profiles and publication history
  - Paper recommendations
  - Batch operations (up to 1,000 papers)
- **API Key**: Optional (increases rate limits from 100 req/5min to 1-10 req/sec)

### 3. Google Scholar MCP Server
- **Source**: https://github.com/JackKuo666/Google-Scholar-MCP-Server
- **Coverage**: Broadest coverage (everything Google Scholar indexes)
- **Capabilities**:
  - Keyword-based search
  - Advanced search (author, year range)
  - Author information retrieval
- **Note**: Uses web scraping (risk of rate limiting)

### 4. PubMed MCP Server
- **Source**: https://github.com/andybrandt/mcp-simple-pubmed
- **Coverage**: Medical and biomedical research
- **Capabilities**:
  - Search PubMed database
  - Access NCBI medical literature
- **API**: Uses official NCBI E-utilities

## Installation

### Quick Install (Recommended)
```bash
./install_all.sh
```

This script will:
1. Check prerequisites (uv, npx)
2. Detect your IDE (Claude Code / Cursor)
3. Install all 4 MCP servers
4. Generate configuration file
5. Test installation

### Manual Installation

If automatic installation fails, you can install servers individually:

#### arXiv
```bash
uv tool install arxiv-mcp-server
```

#### Semantic Scholar
```bash
git clone https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server.git ~/.mcp-servers/semantic-scholar
cd ~/.mcp-servers/semantic-scholar
python3 -m venv venv
source venv/bin/activate
pip install fastmcp semanticscholar
```

#### Google Scholar
```bash
git clone https://github.com/JackKuo666/Google-Scholar-MCP-Server.git ~/.mcp-servers/google-scholar
cd ~/.mcp-servers/google-scholar
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### PubMed
```bash
pip install mcp-simple-pubmed
```

## Configuration

After installation, MCP servers are configured in:
- **Claude Code**: `~/.config/Claude Code/mcp_config.json`
- **Cursor**: `~/.cursor/mcp_config.json`
- **Claude Desktop (macOS)**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Example configuration:
```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uv",
      "args": ["tool", "run", "arxiv-mcp-server", "--storage-path", "/path/to/papers"]
    },
    "semantic-scholar": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/run.py"],
      "env": {
        "SEMANTIC_SCHOLAR_API_KEY": "optional"
      }
    }
  }
}
```

## Usage in IDE

Once installed and configured:

1. Restart your IDE (Claude Code / Cursor)
2. Open a chat window
3. MCP tools are automatically available

Example prompts:
```
"Search arXiv for papers on 'transformers in NLP' from 2020-2024"
"Find the top 10 most-cited papers on climate modeling"
"Get citation network for paper DOI: 10.1234/example"
```

## API Keys (Optional)

### Semantic Scholar
Get a free API key at: https://www.semanticscholar.org/product/api

Add to your `.env` file:
```
SEMANTIC_SCHOLAR_API_KEY=your_key_here
```

Benefits:
- Higher rate limits (1-10 req/sec vs 100 req/5min)
- Priority access during high traffic
- Access to beta features

### PubMed
No API key required, but recommended for higher rate limits.

Get key at: https://www.ncbi.nlm.nih.gov/account/

## Troubleshooting

### MCP servers not appearing in IDE
1. Check config file exists and is valid JSON
2. Restart IDE completely
3. Check server paths are correct
4. Test servers manually (see below)

### Testing individual servers

**arXiv**:
```bash
arxiv-mcp-server --help
```

**Semantic Scholar**:
```bash
source ~/.mcp-servers/semantic-scholar/venv/bin/activate
python ~/.mcp-servers/semantic-scholar/run.py
```

**Google Scholar**:
```bash
source ~/.mcp-servers/google-scholar/venv/bin/activate
python ~/.mcp-servers/google-scholar/server.py
```

**PubMed**:
```bash
python3 -c "import mcp_simple_pubmed; print('OK')"
```

### Rate limiting issues

**Google Scholar**:
- Uses scraping, can be rate-limited
- Use delays between requests
- Consider using Semantic Scholar instead (official API)

**Semantic Scholar**:
- Free tier: 100 requests per 5 minutes
- With API key: 1-10 requests per second
- Implement exponential backoff on errors

### Permission errors
```bash
chmod +x install_all.sh
```

## Uninstallation

To remove MCP servers:

```bash
# Remove installations
uv tool uninstall arxiv-mcp-server
rm -rf ~/.mcp-servers/semantic-scholar
rm -rf ~/.mcp-servers/google-scholar
pip uninstall mcp-simple-pubmed

# Remove configuration
# (Edit your IDE's mcp_config.json and remove server entries)
```

## Support

- **arXiv Server**: https://github.com/blazickjp/arxiv-mcp-server/issues
- **Semantic Scholar**: https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server/issues
- **Google Scholar**: https://github.com/JackKuo666/Google-Scholar-MCP-Server/issues
- **PubMed**: https://github.com/andybrandt/mcp-simple-pubmed/issues
