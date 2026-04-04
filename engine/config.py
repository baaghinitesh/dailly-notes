import os
import sys
from groq import Groq

# ─── Config ───────────────────────────────────────────────────────────────────

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
AUTHOR_NAME  = os.environ.get("AUTHOR_NAME", "baaghinitesh")
AUTHOR_EMAIL = os.environ.get("AUTHOR_EMAIL", "baaghinitesh@gmail.com")
MODEL        = "llama-3.3-70b-versatile"
MAX_UPDATES  = 5

# Minimum content thresholds — reject anything shorter
MIN_NOTE_CHARS   = 800    # notes must be at least 800 chars
MIN_DSA_CHARS    = 300    # DSA solution + summary must be at least 300 chars
MIN_NOTE_WORDS   = 150    # notes must have at least 150 words
MIN_CODE_BLOCKS  = 1      # every article must have at least 1 code block

if not GROQ_API_KEY:
    print("❌ FATAL: Missing GROQ_API_KEY environment variable")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

# In-memory set of paths written this run — prevents same-run duplicates
_written_this_run: set = set()

# Flag set when quota is exhausted — stops further API calls
_quota_exhausted: bool = False

# ─── Custom exceptions ────────────────────────────────────────────────────────

class GroqAPIError(Exception):
    """Non-recoverable Groq API failure after all retries."""
    pass

class GroqQuotaError(Exception):
    """API key quota exhausted or daily limit reached — stop all generation."""
    pass

class GroqAuthError(Exception):
    """Invalid API key or authentication failure — fatal, exit immediately."""
    pass

class ContentValidationError(Exception):
    """Generated content failed quality/completeness validation."""
    pass

LANGS = ("java", "cpp", "c", "python", "javascript")
DIFFS = ("easy", "medium", "hard", "super_advanced")
