import time
import sys
from engine import config
from engine.config import MODEL, client, GroqAPIError, GroqAuthError, GroqQuotaError

def _classify_groq_error(err_str: str) -> str:
    """
    Classify a Groq error string into a category.
    Returns one of: 'auth', 'quota', 'rate_limit', 'context_length',
                    'model_error', 'timeout', 'unknown'
    """
    e = err_str.lower()
    if any(x in e for x in ("invalid_api_key", "authentication", "unauthorized", "401")):
        return "auth"
    if any(x in e for x in ("quota", "billing", "insufficient_quota", "payment", "402")):
        return "quota"
    if any(x in e for x in ("rate_limit", "rate limit", "too many requests", "429")):
        return "rate_limit"
    if any(x in e for x in ("context_length", "context length", "maximum context", "token", "too long")):
        return "context_length"
    if any(x in e for x in ("model_decommissioned", "model_not_found", "model not found", "no such model")):
        return "model_error"
    if any(x in e for x in ("timeout", "timed out", "connection", "network", "503", "502", "500")):
        return "timeout"
    return "unknown"


def call_groq(
    system: str,
    user: str,
    max_tokens: int = 4096,
    retries: int = 4,
    context: str = "",
) -> str:
    """
    Call Groq API with full error classification and exponential backoff.

    Raises:
      GroqAuthError   — invalid key, stop everything
      GroqQuotaError  — quota exhausted, stop all generation
      GroqAPIError    — non-recoverable after all retries
    Never returns empty string — callers can trust the return value is real content.
    """
    if config._quota_exhausted:
        raise GroqQuotaError("Quota already exhausted this run")

    label = f" [{context}]" if context else ""

    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
                max_tokens=max_tokens,
                temperature=0.75,
            )

            content = response.choices[0].message.content
            if not content or not content.strip():
                raise GroqAPIError(f"Groq returned empty content{label}")

            # Check finish reason — 'length' means token limit hit mid-response
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "length":
                print(
                    f"⚠️  Response truncated by token limit{label} "
                    f"(finish_reason=length, max_tokens={max_tokens})"
                )
                # For notes we need complete content — raise so caller can decide
                raise GroqAPIError(
                    f"Response truncated at token limit{label} — content may be incomplete"
                )

            return content.strip()

        except GroqAPIError:
            raise  # re-raise our own errors immediately

        except Exception as e:
            err_str = str(e)
            category = _classify_groq_error(err_str)

            if category == "auth":
                print(f"❌ FATAL: Invalid API key or authentication error{label}: {e}")
                raise GroqAuthError(f"Authentication failed: {e}")

            elif category == "quota":
                print(f"❌ QUOTA EXHAUSTED{label}: {e}")
                config._quota_exhausted = True
                raise GroqQuotaError(f"API quota exhausted: {e}")

            elif category == "model_error":
                print(f"❌ FATAL: Model error{label}: {e}")
                raise GroqAuthError(f"Model error (fatal): {e}")

            elif category == "rate_limit":
                wait = 2 ** attempt * 10  # 20s, 40s, 80s, 160s
                print(
                    f"⏳ Rate limited{label}. "
                    f"Waiting {wait}s (attempt {attempt}/{retries})..."
                )
                time.sleep(wait)

            elif category == "context_length":
                print(f"⚠️  Context too long{label}: {e}")
                # Don't retry — context won't shrink
                raise GroqAPIError(f"Context length exceeded{label}: {e}")

            elif category == "timeout":
                wait = 5 * attempt
                print(
                    f"⚠️  Network/timeout error{label} (attempt {attempt}/{retries}). "
                    f"Waiting {wait}s: {e}"
                )
                if attempt < retries:
                    time.sleep(wait)

            else:
                print(f"⚠️  Groq error [{category}]{label} (attempt {attempt}/{retries}): {e}")
                if attempt < retries:
                    time.sleep(5)

    raise GroqAPIError(f"Groq API failed after {retries} attempts{label}")


def preflight_check() -> bool:
    """
    Before generating any content, verify:
      1. The API key is valid and authenticated
      2. The model is available
      3. The account has remaining quota
      4. A real response can be generated (not just a connection check)

    Returns True if all checks pass.
    Calls sys.exit(1) on auth/model errors (fatal).
    Returns False on quota exhaustion (skip generation, don't fail the run).
    """
    print("🔍 Running preflight API check...")

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Reply with exactly one word."},
                {"role": "user",   "content": "Say: OK"},
            ],
            max_tokens=5,
            temperature=0.0,
        )

        content = response.choices[0].message.content
        if not content or not content.strip():
            print("❌ Preflight FAILED: API returned empty response")
            return False

        print(f"✅ Preflight passed — API key valid, model responsive (got: '{content.strip()}')")
        return True

    except Exception as e:
        err_str = str(e)
        category = _classify_groq_error(err_str)

        if category == "auth":
            print(f"❌ FATAL: API key is invalid or unauthorized: {e}")
            sys.exit(1)

        elif category == "model_error":
            print(f"❌ FATAL: Model '{MODEL}' is unavailable: {e}")
            sys.exit(1)

        elif category == "quota":
            print(f"❌ Preflight FAILED: API quota exhausted — skipping all generation: {e}")
            config._quota_exhausted = True
            return False

        elif category == "rate_limit":
            # Rate limit on preflight — wait and retry once
            print(f"⏳ Rate limited on preflight, waiting 30s...")
            time.sleep(30)
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "Reply with one word."},
                        {"role": "user",   "content": "Say: OK"},
                    ],
                    max_tokens=5,
                    temperature=0.0,
                )
                content = response.choices[0].message.content
                if content and content.strip():
                    print(f"✅ Preflight passed after rate limit wait")
                    return True
            except Exception as e2:
                print(f"❌ Preflight FAILED after retry: {e2}")
                return False

        else:
            print(f"❌ Preflight FAILED [{category}]: {e}")
            return False

    return False
