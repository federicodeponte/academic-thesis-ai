# Academic Thesis AI - Docker Image
# Includes all dependencies for PDF generation and AI agents

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # LaTeX for PDF generation (Pandoc engine)
    pandoc \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    # LibreOffice for alternative PDF generation
    libreoffice-writer \
    libreoffice-core-nogui \
    # System utilities
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker cache efficiency)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directories
RUN mkdir -p examples/output tests/outputs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port for Streamlit UI (when implemented)
EXPOSE 8501

# Default command: run tests to verify installation
CMD ["python", "tests/test_pdf_engines.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; from utils.pdf_engines import get_available_engines; sys.exit(0 if len(get_available_engines()) > 0 else 1)"
