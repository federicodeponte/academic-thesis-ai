"""
Modal.com worker for automated thesis generation
Runs daily at 9am UTC, processes 100 waiting users from Supabase
"""

import modal
import os
from datetime import datetime
from supabase import create_client
import resend

# Create Modal app
app = modal.App("thesis-generator")

# Modal image with dependencies
image = modal.Image.debian_slim().pip_install(
    "supabase==2.3.4",
    "resend==0.7.0",
    "google-generativeai==0.3.2",
    # Add Academic Thesis AI dependencies here
)

# Persistent volume for temporary thesis files
volume = modal.Volume.from_name("thesis-temp", create_if_missing=True)

@app.function(
    schedule=modal.Cron("0 9 * * *"),  # Daily at 9am UTC (cron format)
    timeout=3600,  # 1 hour max
    volumes={"/tmp/thesis": volume},
    secrets=[
        modal.Secret.from_name("supabase-credentials"),  # SUPABASE_URL, SUPABASE_SERVICE_KEY
        modal.Secret.from_name("gemini-api-key"),  # GEMINI_API_KEY
        modal.Secret.from_name("resend-api-key"),  # RESEND_API_KEY
    ],
    image=image,
)
def daily_thesis_batch():
    """
    Main scheduled function - processes 100 waiting users daily
    """
    print(f"[{datetime.now()}] Starting daily thesis batch...")

    # Initialize clients
    supabase = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_KEY"]
    )
    resend.api_key = os.environ["RESEND_API_KEY"]

    # Get next 100 waiting users (FIFO, email verified)
    response = supabase.table('waitlist') \
        .select('*') \
        .eq('status', 'waiting') \
        .eq('email_verified', True) \
        .order('position', desc=False) \
        .limit(100) \
        .execute()

    users = response.data
    print(f"Found {len(users)} users to process")

    success_count = 0
    failed_count = 0

    # Process each thesis
    for user in users:
        max_retries = 3
        retry_count = 0
        success = False

        while retry_count < max_retries and not success:
            try:
                if retry_count > 0:
                    print(f"Retry {retry_count}/{max_retries} for {user['email']}...")
                else:
                    print(f"Processing thesis for {user['email']}...")

                # Update status to processing (only on first attempt)
                if retry_count == 0:
                    supabase.table('waitlist').update({
                        'status': 'processing',
                        'processing_started_at': datetime.now().isoformat()
                    }).eq('id', user['id']).execute()

                # Generate thesis (placeholder - integrate your Academic Thesis AI code)
                pdf_path, docx_path = generate_thesis_placeholder(
                    topic=user['thesis_topic'],
                    language=user['language'],
                    academic_level=user['academic_level']
                )

                # Upload to Supabase Storage (overwrite if retrying)
                with open(pdf_path, 'rb') as pdf_file:
                    supabase.storage.from_('thesis-files').upload(
                        f"{user['id']}/thesis.pdf",
                        pdf_file.read(),
                        file_options={"content-type": "application/pdf", "upsert": "true"}
                    )

                with open(docx_path, 'rb') as docx_file:
                    supabase.storage.from_('thesis-files').upload(
                        f"{user['id']}/thesis.docx",
                        docx_file.read(),
                        file_options={"content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "upsert": "true"}
                    )

                # Get signed URLs (7-day expiry)
                pdf_signed = supabase.storage.from_('thesis-files').create_signed_url(
                    f"{user['id']}/thesis.pdf",
                    expires_in=604800  # 7 days
                )
                docx_signed = supabase.storage.from_('thesis-files').create_signed_url(
                    f"{user['id']}/thesis.docx",
                    expires_in=604800
                )

                # Update status to completed
                supabase.table('waitlist').update({
                    'status': 'completed',
                    'completed_at': datetime.now().isoformat(),
                    'pdf_url': pdf_signed['signedURL'],
                    'docx_url': docx_signed['signedURL']
                }).eq('id', user['id']).execute()

                # Send completion email
                send_completion_email(
                    user['email'],
                    user['full_name'],
                    pdf_signed['signedURL'],
                    docx_signed['signedURL']
                )

                success_count += 1
                success = True
                print(f"✅ Completed thesis for {user['email']}")

            except Exception as e:
                retry_count += 1
                print(f"❌ Error processing {user['email']} (attempt {retry_count}/{max_retries}): {e}")

                if retry_count >= max_retries:
                    # Mark as failed only after all retries exhausted
                    supabase.table('waitlist').update({
                        'status': 'failed'
                    }).eq('id', user['id']).execute()
                    failed_count += 1
                    print(f"💀 Permanently failed thesis for {user['email']} after {max_retries} attempts")
                else:
                    # Wait before retrying (exponential backoff: 5s, 10s, 20s)
                    import time
                    wait_time = 5 * (2 ** (retry_count - 1))
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)

    print(f"[{datetime.now()}] Batch complete: {success_count} success, {failed_count} failed")

    # Log daily stats
    supabase.table('daily_processing_log').insert({
        'date': datetime.now().date().isoformat(),
        'processed_count': success_count,
        'failed_count': failed_count,
        'completed_at': datetime.now().isoformat()
    }).execute()


def generate_thesis_placeholder(topic: str, language: str, academic_level: str):
    """
    Placeholder function - replace with your Academic Thesis AI integration

    Returns:
        tuple: (pdf_path, docx_path)
    """
    # TODO: Integrate your Academic Thesis AI code here
    # Example:
    # from your_thesis_ai import generate_thesis
    # result = generate_thesis(topic, language, academic_level, model="gemini-2.5-flash")
    # return result.pdf_path, result.docx_path

    # For now, create dummy files
    pdf_path = "/tmp/thesis/thesis.pdf"
    docx_path = "/tmp/thesis/thesis.docx"

    with open(pdf_path, 'w') as f:
        f.write("Placeholder PDF")
    with open(docx_path, 'w') as f:
        f.write("Placeholder DOCX")

    return pdf_path, docx_path


def send_completion_email(email: str, name: str, pdf_url: str, docx_url: str):
    """Send thesis completion notification email using React Email template"""
    # Note: Python backend uses simple HTML for now
    # For proper React Email templates, integrate with Next.js API route
    resend.Emails.send({
        "from": "Academic Thesis AI <hello@academic-thesis.ai>",
        "to": email,
        "subject": "Your AI-Generated Thesis is Ready! 🎓",
        "html": f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Ubuntu, sans-serif; background-color: #f6f9fc; margin: 0; padding: 0; }}
                    .container {{ background-color: #ffffff; margin: 0 auto; padding: 20px 0 48px; max-width: 600px; }}
                    .header {{ color: #26251e; font-size: 24px; font-weight: bold; margin: 40px 0; padding: 0 40px; text-align: center; }}
                    .content {{ color: #4b5563; font-size: 16px; line-height: 24px; margin: 16px 0; padding: 0 40px; }}
                    .button-container {{ padding: 27px 40px; text-align: center; }}
                    .button-pdf {{ background-color: #8B5CF6; border-radius: 8px; color: #fff; font-size: 16px; font-weight: bold; text-decoration: none; padding: 12px 24px; margin: 8px 8px 8px 0; display: inline-block; }}
                    .button-docx {{ background-color: #6366f1; border-radius: 8px; color: #fff; font-size: 16px; font-weight: bold; text-decoration: none; padding: 12px 24px; margin: 8px 0; display: inline-block; }}
                    .alert-box {{ background-color: #fef3c7; border-radius: 8px; margin: 24px 40px; padding: 16px; border: 1px solid #fbbf24; }}
                    .alert-text {{ color: #26251e; font-size: 14px; line-height: 20px; margin: 0 0 8px 0; }}
                    .footer {{ color: #6b7280; font-size: 14px; line-height: 24px; margin: 32px 0; padding: 0 40px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="header">Your Thesis is Ready, {name}! 🎓</h1>
                    <p class="content">We've generated your thesis using our 15 AI agents. Download it now:</p>
                    <div class="button-container">
                        <a href="{pdf_url}" class="button-pdf">Download PDF</a>
                        <a href="{docx_url}" class="button-docx">Download Word</a>
                    </div>
                    <div class="alert-box">
                        <p class="alert-text"><strong>⏰ These links expire in 7 days.</strong><br/>Make sure to download your thesis files before they expire.</p>
                    </div>
                    <p class="content">Love your thesis? Star us on <a href="https://github.com/federicodeponte/academic-thesis-ai" style="color: #8B5CF6; text-decoration: underline;">GitHub</a>!</p>
                    <p class="footer">Thanks,<br/>Academic Thesis AI Team</p>
                </div>
            </body>
            </html>
        """
    })


# For manual testing
@app.local_entrypoint()
def main():
    """Test function locally"""
    daily_thesis_batch.remote()
