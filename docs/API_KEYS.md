# API Keys Setup Guide

**Time needed: 5 minutes**

This guide shows you exactly how to get an API key for Academic Thesis AI.

---

## Which API Should I Choose?

### Quick Decision Tree

**Just getting started / Want FREE option?**
→ **Google Gemini** (generous free tier, good quality)

**Writing important thesis/dissertation?**
→ **Claude Sonnet 4.5** (best quality, $20-50 per paper)

**On a budget but need better quality?**
→ **Gemini 2.5 Pro** ($5-15 per paper)

**Already have OpenAI credits?**
→ **GPT-5** (good quality, familiar)

---

## Cost Comparison

| Model | 6,000-word Paper | Master's Thesis (20k words) | Quality |
|-------|------------------|----------------------------|---------|
| **Gemini 2.5 Flash** | $0-5 (FREE tier) | $10-20 | Good |
| **Gemini 2.5 Pro** | $5-15 | $20-40 | Very Good |
| **Claude Sonnet 4.5** | $20-50 | $50-100 | Excellent |
| **GPT-5** | $30-60 | $60-120 | Very Good |

**Free tiers:**
- **Gemini:** 1,500 requests/day (usually enough for 1-2 papers)
- **Claude:** $5 credit for new users
- **OpenAI:** No free tier

**Recommendation:** Start with Gemini. Upgrade to Claude if you need better quality.

---

## Option 1: Google Gemini (RECOMMENDED)

### Why Gemini?
- ✅ FREE tier (generous limits)
- ✅ Fast responses
- ✅ Good quality for most papers
- ✅ Easy setup (just Google account needed)

### Step-by-Step Setup (2 minutes)

**1. Go to Google AI Studio**

Visit: https://aistudio.google.com/apikey

**2. Sign in with Google Account**

Use your existing Google account (Gmail, etc.)

**3. Create API Key**

Click the blue **"Create API Key"** button

**4. Copy Your API Key**

Click **"Copy"** next to your new key

It will look like: `AIzaSyA...` (about 40 characters)

**5. Add to .env.local**

Open `.env.local` in your text editor and add:

```bash
GOOGLE_API_KEY=AIzaSyA...your-key-here...
```

**6. Verify It Works**

Run the test:
```bash
python examples/quick_test.py
```

You should see: `✅ API key valid`

### Google Search Grounding (NEW)

Your Google API key also enables **Google Search grounding** for citation discovery:

- 🔍 **Real-time source discovery** - Finds web sources with Google Search integration
- ✅ **URL validation** - Automatically validates and unwraps URLs
- 🌐 **Web source support** - Complements academic databases with general web sources

**How it works:**
1. Academic databases (Crossref, Semantic Scholar) are tried first
2. If no academic paper found, Gemini with Google Search grounding searches the web
3. URLs are validated (HTTP 200 check) and redirects unwrapped
4. Only verified, accessible sources are added to citations

**Requirements:**
- `google-generativeai >= 0.8.0` (automatically installed)
- Same Google API key as above

No additional setup needed - grounding is enabled automatically!

---

## Option 2: Claude (Anthropic)

### Why Claude?
- ✅ Best quality for academic writing
- ✅ Excellent at following complex prompts
- ✅ Good at citations and formal language
- ❌ More expensive than Gemini

### Step-by-Step Setup (3 minutes)

**1. Go to Anthropic Console**

Visit: https://console.anthropic.com/

**2. Create Account**

Click **"Sign Up"** and create account with email

**3. Add Payment Method**

- Click **"Settings"** → **"Billing"**
- Add credit card
- You'll get $5 free credit

**4. Get API Key**

- Click **"API Keys"** in sidebar
- Click **"Create Key"**
- Give it a name (e.g., "Academic Thesis AI")
- Click **"Create"**

**5. Copy Your API Key**

Click **"Copy"** - it looks like: `sk-ant-api03-...`

**IMPORTANT:** You can only see this ONCE. Save it immediately!

**6. Add to .env.local**

```bash
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

**7. Set as Default (Optional)**

In `.env.local`, also add:
```bash
DEFAULT_LLM=claude
```

**8. Verify It Works**

```bash
python examples/quick_test.py
```

---

## Option 3: OpenAI (GPT)

### Why OpenAI?
- ✅ Familiar brand
- ✅ Good documentation
- ✅ Widely used
- ❌ More expensive than Gemini
- ❌ No free tier

### Step-by-Step Setup (3 minutes)

**1. Go to OpenAI Platform**

Visit: https://platform.openai.com/signup

**2. Create Account**

Sign up with email or Google/Microsoft account

**3. Add Payment Method**

- Click **"Settings"** → **"Billing"**
- Add credit card
- Add at least $10 credit

**4. Create API Key**

- Click **"API Keys"** in sidebar
- Click **"Create new secret key"**
- Name it: "Academic Thesis AI"
- Click **"Create"**

**5. Copy Your API Key**

Save immediately - it looks like: `sk-...`

You can only see this ONCE!

**6. Add to .env.local**

```bash
OPENAI_API_KEY=sk-...your-key-here...
```

**7. Set as Default (Optional)**

```bash
DEFAULT_LLM=openai
```

**8. Verify It Works**

```bash
python examples/quick_test.py
```

---

## Multi-LLM Setup (Advanced)

You can configure ALL three API keys and switch between them:

**.env.local:**
```bash
# All three API keys
GOOGLE_API_KEY=AIzaSyA...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Default to use
DEFAULT_LLM=gemini

# Use better model for validation
USE_PRO_FOR_VALIDATION=true
```

**Why use multiple?**
- Start with Gemini (free) for drafts
- Use Claude for final polish
- Fall back if one has downtime

---

## Troubleshooting

### "API key invalid" Error

**For Gemini:**
- Make sure key starts with `AIzaSy`
- Check you copied the entire key (no spaces)
- Try generating a new key at https://aistudio.google.com/apikey

**For Claude:**
- Make sure key starts with `sk-ant-`
- Verify billing is set up at https://console.anthropic.com/settings/billing
- Check you have credit remaining

**For OpenAI:**
- Make sure key starts with `sk-`
- Verify you added payment at https://platform.openai.com/account/billing
- Check usage limits aren't exceeded

### "Rate limit exceeded" Error

**Solutions:**
1. Wait a few minutes and try again
2. If using Gemini free tier:
   - You hit 1,500 requests/day limit
   - Upgrade to paid tier or wait 24 hours
3. If using Claude/OpenAI:
   - Add more credit to your account
   - Check current usage

### "Connection refused" Error

**Possible causes:**
1. No internet connection
2. Firewall blocking API requests
3. API service is down (check status pages)

**Check status:**
- Gemini: https://status.cloud.google.com/
- Claude: https://status.anthropic.com/
- OpenAI: https://status.openai.com/

### Key Not Loading

**Check your .env.local file:**

```bash
# Print your API key (first 20 chars only for security)
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv('.env.local', override=True)
key = os.getenv('GOOGLE_API_KEY', 'NOT FOUND')
print(f'API Key: {key[:20]}...' if len(key) > 20 else key)
"
```

Should print: `API Key: AIzaSy...`

If it says `NOT FOUND`, your key isn't in `.env.local`

---

## Security Best Practices

### ✅ DO:
- Keep API keys in `.env.local` (gitignored)
- Never commit `.env.local` to git
- Use separate keys for development vs production
- Rotate keys periodically
- Set usage limits in API dashboards

### ❌ DON'T:
- Put keys in code files
- Commit keys to GitHub
- Share keys publicly
- Use same key across multiple projects
- Share screenshots with keys visible

### If Your Key Leaks:

**Immediate steps:**
1. Delete the leaked key in API dashboard
2. Generate a new key
3. Update `.env.local` with new key
4. If leaked on GitHub:
   - Delete the commit (git rebase or force push)
   - Consider the repository compromised
   - Rotate ALL secrets

---

## Cost Monitoring

### Set Usage Limits

**Gemini:**
- Dashboard: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
- Set daily request limit

**Claude:**
- Dashboard: https://console.anthropic.com/settings/limits
- Set monthly spending limit
- Get email alerts at 50%/80%

**OpenAI:**
- Dashboard: https://platform.openai.com/account/limits
- Set hard limit (account won't exceed this)
- Soft limit (get email alert)

### Monitor Usage

Check spending regularly:
- **Gemini:** https://console.cloud.google.com/billing
- **Claude:** https://console.anthropic.com/settings/billing
- **OpenAI:** https://platform.openai.com/account/usage

**Typical usage for one paper:**
- Scout + Scribe (research): 50-100 API calls
- Writing agents: 200-300 API calls
- Validation agents: 100-150 API calls
- **Total:** 350-550 API calls per paper

---

## FAQ

**Q: Can I use the free tier forever?**

A: Gemini's free tier is permanent but has rate limits (1,500 requests/day). For serious use, upgrade to paid tier.

**Q: Which model is best for academic writing?**

A: Claude Sonnet 4.5 produces the most academic-sounding text. Gemini 2.5 Pro is close and cheaper.

**Q: Can I switch models mid-paper?**

A: Yes! Change `DEFAULT_LLM` in `.env.local` anytime.

**Q: Do I need all three API keys?**

A: No! One is enough. Start with Gemini (free).

**Q: How do I know when I'm using too much?**

A: Set up billing alerts in your API dashboard. Most papers cost <$20 with Claude.

**Q: What if I run out of free tier?**

A: Either add payment method or wait 24 hours for limits to reset.

---

## Next Steps

✅ **Got your API key?**

1. Add it to `.env.local`
2. Run test: `python examples/quick_test.py`
3. Start tutorial: [examples/tutorial/README.md](../examples/tutorial/README.md)

❌ **Still having issues?**

- Check [FAQ.md](../FAQ.md)
- Check [docs/INSTALLATION.md](INSTALLATION.md)
- Open GitHub issue

---

**Ready?** → Go back to [00_START_HERE.md](../00_START_HERE.md) and run the test!
