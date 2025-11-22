# Backend - Modal.com Thesis Generation Worker

This directory contains the Modal.com serverless worker that automatically generates theses daily.

## Setup

### 1. Install Modal CLI

```bash
pip install modal
modal setup
```

This will authenticate you with Modal (one-time setup).

### 2. Create Modal Secrets

Add your credentials to Modal's secret management:

```bash
# Supabase credentials
modal secret create supabase-credentials \
  SUPABASE_URL=https://your-project.supabase.co \
  SUPABASE_SERVICE_KEY=your-service-role-key

# Gemini API key
modal secret create gemini-api-key \
  GEMINI_API_KEY=your-gemini-api-key

# Resend API key
modal secret create resend-api-key \
  RESEND_API_KEY=your-resend-api-key
```

### 3. Deploy Worker

```bash
modal deploy modal_worker.py
```

This will:
- Deploy the scheduled function (runs daily at 9am UTC)
- Create persistent volume for temporary files
- Set up all dependencies

### 4. Test Locally

```bash
modal run modal_worker.py
```

This runs the batch processor once immediately (for testing).

## How It Works

1. **Daily Trigger**: Runs at 9am UTC every day
2. **Fetch Queue**: Gets next 100 waiting users (FIFO, email verified)
3. **Generate Thesis**: Runs your OpenDraft code for each user
4. **Upload Files**: Stores PDF/DOCX in Supabase Storage
5. **Update Database**: Marks thesis as completed, stores signed URLs
6. **Send Email**: Notifies user with download links

## Integration with OpenDraft

Replace the `generate_thesis_placeholder()` function with your actual thesis generation code:

```python
from opendraft_ai import ThesisGenerator

def generate_thesis_placeholder(topic: str, language: str, academic_level: str):
    generator = ThesisGenerator(model="gemini-2.5-flash")
    result = generator.generate(
        topic=topic,
        language=language,
        academic_level=academic_level
    )
    return result.pdf_path, result.docx_path
```

## Monitoring

View logs in real-time:

```bash
modal app logs thesis-generator
```

## Cost Estimate

- **Modal compute**: ~$0-30/month (within free tier for 100 jobs/day × 10 min)
- **Gemini API**: $0 (free tier: 1,500 requests/day)
- **Total**: ~$0-30/month

## Troubleshooting

**Error: "Secret not found"**
- Run `modal secret list` to verify secrets exist
- Recreate with commands above

**Error: "Permission denied"**
- Check Supabase service role key has correct permissions
- Verify storage bucket exists

**Files not uploading:**
- Check storage bucket name is 'thesis-files'
- Verify RLS policies allow service role to upload
