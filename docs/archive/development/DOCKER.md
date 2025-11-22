# Docker Deployment Guide

Run OpenDraft in a containerized environment with all dependencies pre-installed.

---

## Quick Start

### 1. Build the Image

```bash
docker-compose build
```

This creates a Docker image with:
- Python 3.11
- Pandoc + LaTeX (PDF generation)
- LibreOffice (alternative PDF engine)
- All Python dependencies
- Complete OpenDraft framework

**Build time:** 5-10 minutes (first time)

### 2. Run Tests

```bash
docker-compose run --rm test
```

Verifies all PDF engines work correctly.

### 3. Start the Web UI (when implemented)

```bash
docker-compose up -d
```

Access at: http://localhost:8501

---

## Usage Patterns

### Interactive Shell

Run an interactive session inside the container:

```bash
docker-compose run --rm opendraft bash
```

Then use any utility:
```bash
# Inside container
python utils/export_professional.py examples/tutorial/my_paper.md --pdf output.pdf
python tests/test_pdf_engines.py
```

### Generate PDF from Host Files

Mount your files and generate PDF:

```bash
docker-compose run --rm \
    -v $(pwd)/my_paper.md:/app/input.md \
    opendraft \
    python utils/export_professional.py input.md --pdf output.pdf
```

### Run Specific Agent Tests

```bash
docker-compose run --rm opendraft \
    python tests/scripts/test_scout_agent.py
```

---

## Environment Variables

Create `.env` file in project root:

```bash
# API Keys (at least one required)
ANTHROPIC_API_KEY=your_claude_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here

# Optional
GPTZERO_API_KEY=your_gptzero_key_here
```

Docker Compose automatically loads this file.

---

## Advanced Configuration

### Custom Resource Limits

Edit `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'      # Use up to 4 CPUs
      memory: 8G       # Use up to 8GB RAM
```

### Persistent Data

All important directories are mounted as volumes:
- `./examples` - Templates and tutorials
- `./tests/outputs` - Generated test files
- `./research` - Your research data

Files created inside the container persist on your host machine.

### Using Different Python Versions

Edit `Dockerfile` first line:

```dockerfile
FROM python:3.10-slim  # or 3.12-slim
```

Then rebuild:
```bash
docker-compose build --no-cache
```

---

## Production Deployment

### Build for Production

```bash
docker build -t opendraft:v1.1.0 .
docker tag opendraft:v1.1.0 your-registry/opendraft:v1.1.0
docker push your-registry/opendraft:v1.1.0
```

### Run in Production

```bash
docker run -d \
    --name opendraft \
    -p 8501:8501 \
    -v $(pwd)/examples:/app/examples \
    -v $(pwd)/.env:/app/.env:ro \
    --restart unless-stopped \
    your-registry/opendraft:v1.1.0
```

### Health Monitoring

Check container health:
```bash
docker ps
# Look for "healthy" status

docker inspect --format='{{.State.Health.Status}}' opendraft
```

---

## Troubleshooting

### Build Fails with "No space left on device"

Clean up Docker:
```bash
docker system prune -a
```

### "Permission denied" errors

Fix volume permissions:
```bash
chmod -R 755 examples/ tests/outputs/
```

### PDF generation fails inside container

Check engine availability:
```bash
docker-compose run --rm opendraft \
    python -c "from utils.pdf_engines import get_available_engines; print(get_available_engines())"
```

Should show: `['Pandoc/LaTeX', 'LibreOffice', 'WeasyPrint']`

### Container exits immediately

Check logs:
```bash
docker-compose logs opendraft
```

### Out of memory during LaTeX installation

Increase Docker Desktop memory:
- Docker Desktop → Settings → Resources
- Set memory to 4GB minimum
- Restart Docker

---

## Image Details

**Image size:** ~1.5 GB

**Includes:**
- Python 3.11 runtime
- Pandoc 2.x
- TeX Live (LaTeX distribution)
- LibreOffice Writer
- All Python dependencies from `requirements.txt`

**Security:**
- Runs as non-root user (coming in v1.2)
- No exposed credentials
- Environment variables via `.env` file

---

## Development Workflow

### Hot Reload Development

For development with live code updates:

```bash
docker-compose run --rm \
    -v $(pwd):/app \
    opendraft \
    bash
```

Changes to code are immediately reflected inside container.

### Debugging

Add debug flag:
```bash
docker-compose run --rm \
    -e PYTHONUNBUFFERED=1 \
    opendraft \
    python -m pdb tests/test_pdf_engines.py
```

---

## Maintenance

### Update Dependencies

1. Edit `requirements.txt`
2. Rebuild image:
   ```bash
   docker-compose build --no-cache
   ```

### Update System Packages

Edit `Dockerfile` to change `apt-get install` packages, then rebuild.

### Clean Up Old Images

```bash
docker image prune -a
```

---

## Multi-Platform Builds

Build for ARM64 (Mac M1/M2) and AMD64 (x86):

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
    -t opendraft:multi-arch .
```

---

## Questions?

- Check main `README.md` for general documentation
- See `TROUBLESHOOTING.md` for common issues
- Open GitHub issue for bugs

---

**Docker simplifies deployment and ensures consistent environments across all systems!** 🐳
