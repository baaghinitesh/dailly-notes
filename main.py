#!/usr/bin/env python3
"""
main.py — Groq/Llama-3 powered content engine for dailly-notes

Flow per article:
  1. Preflight check — verify API key is live and has quota (tiny test call)
  2. Randomly select a topic FILE from topics/
  3. From that file, randomly select a topic/problem not yet generated
  4. Call Groq API for content (with full error classification + backoff)
  5. Validate the returned content (length, required sections, not truncated)
  6. Write file only if content passes validation
  7. Commit and push

Folder layout (everything under docs/notes/):
  docs/notes/{section}/{section_key}/{slug}.md   ← conceptual notes
  docs/notes/dsa/{lang}/{difficulty}/{slug}.md   ← DSA problem solutions
  docs/notes/dsa/{section_key}/{slug}.md         ← DSA conceptual notes

Error handling guarantees:
  - API key validated BEFORE any generation attempt
  - Quota exhausted / token limit → skip remaining articles, commit what succeeded
  - Rate limit → exponential backoff (20s → 40s → 80s → 160s)
  - Truncated / empty content → rejected, file never written
  - Partial write failure → cleanup_files() removes incomplete artifacts
  - Git push failure → retry with rebase, fallback to per-article commits
  - Every failure is classified and logged with a clear reason
"""

import os
import random
import sys
import json
import time
import re
import git
from typing import Any, List, Optional, Tuple
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

# ─── Load topics (file-aware) ─────────────────────────────────────────────────

LANGS = ("java", "cpp", "c", "python", "javascript")
DIFFS = ("easy", "medium", "hard", "super_advanced")

def load_topic_files() -> List[dict]:
    """
    Load each topic JSON file as a separate entry.
    Enables file-first random selection: pick a file, then pick a topic within it.
    """
    topics_dir = "topics"
    if not os.path.isdir(topics_dir):
        print("❌ FATAL: topics/ directory not found")
        sys.exit(1)

    files = []
    for fname in sorted(os.listdir(topics_dir)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(topics_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)

            entry: dict = {
                "filename": fname,
                "dsa_problems": {lang: {d: [] for d in DIFFS} for lang in LANGS},
                "notes": {},
            }

            for lang in LANGS:
                lang_data = data.get("problems", {}).get(lang, {})
                for diff in DIFFS:
                    if diff in lang_data:
                        entry["dsa_problems"][lang][diff].extend(lang_data[diff])

            for subject, content in data.get("notes", {}).items():
                entry["notes"][subject] = content

            files.append(entry)
            print(f"  ✓ Loaded {fname}")
        except json.JSONDecodeError as e:
            print(f"⚠️  Invalid JSON in {fpath}: {e} — skipping")
        except Exception as e:
            print(f"⚠️  Failed to load {fpath}: {e} — skipping")

    if not files:
        print("❌ FATAL: No topic files loaded")
        sys.exit(1)

    return files


print("📂 Loading topic files...")
topic_files = load_topic_files()

_all_problems_count = sum(
    len(tf["dsa_problems"][lang][diff])
    for tf in topic_files
    for lang in LANGS
    for diff in DIFFS
)
_all_notes_count = sum(len(tf["notes"]) for tf in topic_files)
print(
    f"📚 Loaded {len(topic_files)} topic files | "
    f"{_all_problems_count} DSA problems | "
    f"{_all_notes_count} note subjects"
)


# ─── Disk scan ────────────────────────────────────────────────────────────────

def scan_existing_files() -> set:
    """
    Walk docs/notes/ at startup and collect all existing .md paths.
    Prevents regenerating articles that already exist on disk.
    """
    existing = set()
    notes_root = "docs/notes"
    if not os.path.isdir(notes_root):
        return existing
    for dirpath, _, filenames in os.walk(notes_root):
        for fname in filenames:
            if fname.endswith(".md"):
                full = os.path.join(dirpath, fname).replace("\\", "/")
                existing.add(full)
    print(f"🗂️  Found {len(existing)} existing articles on disk")
    return existing


_existing_on_disk: set = scan_existing_files()

# ─── Helpers ──────────────────────────────────────────────────────────────────

def flatten_to_strings(value: Any) -> List[str]:
    out: List[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, (list, tuple)):
        for v in value:
            out.extend(flatten_to_strings(v))
    elif isinstance(value, dict):
        for v in value.values():
            out.extend(flatten_to_strings(v))
    return out


def sanitize_filename(name: str, max_length: int = 60) -> str:
    name = name.strip()
    name = re.sub(r"[ /\\]+", "_", name)
    name = re.sub(r"[^A-Za-z0-9_\-]", "", name)
    return name[:max_length]


def url_encode(text: str) -> str:
    return text.strip().replace(" ", "%20").replace(":", "").replace("/", "")


def read_frontmatter(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", content)
        if not m:
            return {}
        meta: dict = {}
        for line in m.group(1).split("\n"):
            idx = line.find(":")
            if idx == -1:
                continue
            k = line[:idx].strip()
            v = line[idx + 1:].strip().strip('"\'')
            if k:
                meta[k] = v
        return meta
    except Exception:
        return {}


def build_frontmatter(
    title: str, topic: str, section: str, tags: List[str], update_count: int
) -> str:
    tag_str = ", ".join(tags)
    banner = (
        f"https://image.pollinations.ai/prompt/"
        f"{url_encode(topic)}%20{url_encode(section)}%20programming"
        f"?width=800&height=400&nologo=true"
    )
    return (
        f'---\n'
        f'title: "{title}"\n'
        f'topic: "{topic}"\n'
        f'section: "{section}"\n'
        f'tags: "{tag_str}"\n'
        f'banner: "{banner}"\n'
        f'update_count: {update_count}\n'
        f'---\n'
    )


def path_is_available(path: str) -> bool:
    norm = path.replace("\\", "/")
    return norm not in _written_this_run and norm not in _existing_on_disk


def path_is_updatable(path: str) -> Optional[int]:
    norm = path.replace("\\", "/")
    if norm in _written_this_run:
        return None
    if not os.path.exists(path):
        return None
    meta = read_frontmatter(path)
    try:
        count = int(meta.get("update_count", 0))
    except (ValueError, TypeError):
        count = 0
    return count if count < MAX_UPDATES else None


# ─── Content validation ───────────────────────────────────────────────────────

def validate_note_content(content: str, topic: str) -> None:
    """
    Validate that a generated note article meets quality standards.
    Raises ContentValidationError with a specific reason if it fails.
    """
    if not content or not content.strip():
        raise ContentValidationError("Content is empty")

    stripped = content.strip()
    char_count = len(stripped)
    word_count = len(stripped.split())

    if char_count < MIN_NOTE_CHARS:
        raise ContentValidationError(
            f"Content too short: {char_count} chars (minimum {MIN_NOTE_CHARS})"
        )

    if word_count < MIN_NOTE_WORDS:
        raise ContentValidationError(
            f"Content too short: {word_count} words (minimum {MIN_NOTE_WORDS})"
        )

    # Must have at least one code block
    code_blocks = re.findall(r"```\w*\n[\s\S]*?```", stripped)
    if len(code_blocks) < MIN_CODE_BLOCKS:
        raise ContentValidationError(
            f"Missing code blocks: found {len(code_blocks)}, need at least {MIN_CODE_BLOCKS}"
        )

    # Must have at least 2 markdown headings (## sections)
    headings = re.findall(r"^#{1,3} .+", stripped, re.MULTILINE)
    if len(headings) < 2:
        raise ContentValidationError(
            f"Too few sections: found {len(headings)} headings, need at least 2"
        )

    # Detect obvious truncation — content ending mid-sentence or mid-code-block
    last_200 = stripped[-200:]
    open_code = last_200.count("```") % 2 != 0
    if open_code:
        raise ContentValidationError("Content appears truncated: unclosed code block at end")

    # Detect AI refusal or error responses
    refusal_patterns = [
        r"^i (can't|cannot|am unable to|don't|do not)",
        r"^i'm sorry",
        r"^as an ai",
        r"^i apologize",
    ]
    first_100 = stripped[:100].lower()
    for pattern in refusal_patterns:
        if re.search(pattern, first_100):
            raise ContentValidationError(f"AI returned a refusal response: {stripped[:80]}")


def validate_dsa_content(code: str, summary: str, topic: str) -> None:
    """
    Validate that a generated DSA solution meets quality standards.
    Raises ContentValidationError with a specific reason if it fails.
    """
    if not code or not code.strip():
        raise ContentValidationError("DSA code is empty")

    if len(code.strip()) < MIN_DSA_CHARS:
        raise ContentValidationError(
            f"DSA code too short: {len(code.strip())} chars (minimum {MIN_DSA_CHARS})"
        )

    if not summary or not summary.strip():
        raise ContentValidationError("DSA summary is empty")

    if len(summary.strip()) < 100:
        raise ContentValidationError(
            f"DSA summary too short: {len(summary.strip())} chars"
        )

    # Summary must have at least one heading
    headings = re.findall(r"^#{1,3} .+", summary.strip(), re.MULTILINE)
    if len(headings) < 1:
        raise ContentValidationError("DSA summary missing headings")


# ─── Groq API — with full error classification ────────────────────────────────

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
    global _quota_exhausted

    if _quota_exhausted:
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
                _quota_exhausted = True
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


# ─── Preflight API check ──────────────────────────────────────────────────────

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
    global _quota_exhausted

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
            _quota_exhausted = True
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


# ─── File I/O ─────────────────────────────────────────────────────────────────

def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    norm = path.replace("\\", "/")
    _written_this_run.add(norm)
    _existing_on_disk.add(norm)
    print(f"📄 Written: {path} ({len(content):,} chars)")


def cleanup_files(paths: List[str]):
    """Remove files written during a failed generation and clean up empty dirs."""
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"🗑️  Cleaned up: {path}")
                norm = path.replace("\\", "/")
                _written_this_run.discard(norm)
                _existing_on_disk.discard(norm)
                parent = os.path.dirname(path)
                if os.path.isdir(parent) and not os.listdir(parent):
                    os.rmdir(parent)
        except Exception as e:
            print(f"⚠️  Could not clean up {path}: {e}")

# ─── Git ──────────────────────────────────────────────────────────────────────

def commit_and_push(message: str, retries: int = 3) -> bool:
    for attempt in range(1, retries + 1):
        try:
            repo = git.Repo(".")
            repo.git.add(A=True)
            if not repo.is_dirty(untracked_files=True):
                print("ℹ️  Nothing to commit.")
                return True
            repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
            repo.remote(name="origin").push()
            print(f"✅ Pushed: {message}")
            return True
        except git.exc.GitCommandError as e:
            if attempt < retries:
                print(f"⚠️  Push failed (attempt {attempt}), pulling and retrying: {e}")
                try:
                    git.Repo(".").git.pull("--rebase", "origin", "main")
                except Exception:
                    pass
                time.sleep(5)
            else:
                print(f"❌ Push failed after {retries} attempts: {e}")
                return False
    return False


# ─── System prompts ───────────────────────────────────────────────────────────

NOTE_SYSTEM = """You are a world-class senior software engineer and technical writer. Your job is to produce PREMIUM, DEEPLY DETAILED study notes that software engineers will use to prepare for FAANG interviews and build real production skills.

YOUR OUTPUT WILL BE AUTOMATICALLY REJECTED if any of these rules are violated. Follow every rule exactly.

━━━ CONTENT QUALITY RULES ━━━

RULE 1 — DEPTH OVER BREADTH
Every section must go deep. Do not write surface-level summaries.
- Explain WHY things work, not just WHAT they are
- Include internal implementation details (how the JVM handles it, how V8 optimizes it, etc.)
- Cover edge cases, gotchas, and non-obvious behaviors
- Include performance numbers and benchmarks where relevant

RULE 2 — CODE EXAMPLES (MANDATORY: at least 3, each must be different)
Every code example must be:
- COMPLETE and RUNNABLE — copy-paste into an IDE and it works
- WELL-COMMENTED — every non-obvious line has an inline comment
- REALISTIC — based on real production patterns, not toy examples
- PROGRESSIVELY COMPLEX — start simple, build to advanced

RULE 3 — DIAGRAMS (MANDATORY)
The ## Visual Diagram section MUST contain a ```mermaid block.
Choose the most appropriate diagram type:
- flowchart TD — for algorithms, decision trees, process flows
- sequenceDiagram — for request/response flows, API interactions
- classDiagram — for OOP relationships, design patterns
- graph LR — for dependency graphs, data flow
Make the diagram DETAILED — at least 6 nodes/steps.

RULE 4 — COMPARISON TABLE (MANDATORY)
The ## Comparison section MUST contain a Markdown table with at least 4 rows:
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
|----------|----------------|-----------------|------|------|----------|

RULE 5 — CALLOUTS (use throughout, minimum 4 total)
> **Note:** important context or background
> **Warning:** common mistake that causes bugs or performance issues
> **Tip:** optimization, best practice, or shortcut
> **Interview:** exactly what interviewers ask and what answer they want to hear

━━━ STRUCTURE RULES ━━━

START with the banner image — this is the VERY FIRST LINE, nothing before it:
![topic](BANNER_URL_PROVIDED_IN_USER_MESSAGE)

Then use ALL of these ## sections in this exact order:

## Introduction
- What it is, why it exists, what problem it solves
- Real-world relevance: where you encounter this in production
- Why every engineer needs to know this

## Core Concepts
- Precise definitions with no hand-waving
- Mental models and analogies that make it click
- Key terminology with clear explanations

## How It Works Internally
- Under-the-hood mechanics (memory layout, execution model, etc.)
- Step-by-step breakdown of what happens when you use it
- Implementation details that matter for performance

## Code Examples
- Example 1: Basic usage (beginner-friendly, fully commented)
- Example 2: Real-world pattern (production-style code)
- Example 3: Advanced usage or edge case handling
- Each example must have a brief explanation above it

## Visual Diagram
- MUST contain a ```mermaid block
- Diagram must illustrate the core concept visually
- Add a 2-3 sentence explanation below the diagram

## Comparison
- MUST contain a Markdown comparison table
- Compare at least 4 different approaches/alternatives
- Include time complexity, space complexity, pros, cons

## Real-world Use Cases
- 3-5 concrete production examples (name real companies/systems where possible)
- For each: what the problem was, why this solution was chosen, what the result was

## Common Pitfalls
- At least 4 specific mistakes engineers make
- For each: what the mistake is, why it happens, how to avoid it
- Include code showing the WRONG way vs the RIGHT way where helpful

## Interview Tips
- The 3-5 most common interview questions on this topic
- For each question: what a weak answer looks like vs what a strong answer looks like
- Key talking points that show deep understanding
- Follow-up questions to expect

## Key Takeaways
- 6-10 bullet points of the most important facts to remember
- Written as concise, memorable statements
- Include complexity numbers where relevant

━━━ FORMATTING RULES ━━━

- Do NOT include YAML frontmatter (added separately)
- Do NOT start with preamble ("Here are the notes", "Sure!", "I'll write...")
- Code language tags: ```java ```javascript ```typescript ```python ```go ```rust ```cpp ```bash ```sql ```yaml ```json
- Every code block must be COMPLETE — no "// ... rest of code", no pseudocode
- Target 1200-1600 words of dense, practical content
- Use **bold** for key terms on first use
- Use `inline code` for method names, variables, class names
"""

UPDATE_SYSTEM = """You are a senior software engineer appending a new advanced section to an existing technical article.

YOUR OUTPUT WILL BE REJECTED if any rule is violated.

RULES:
1. Do NOT rewrite or repeat existing content — ONLY append NEW content
2. The new section MUST cover something genuinely new: an advanced pattern, a production use case, a performance optimization, or a deep-dive sub-topic NOT already in the article
3. Start your response with a new ## heading — absolutely no preamble
4. MUST include at least one COMPLETE, RUNNABLE code example with inline comments
5. MUST include at least one callout: > **Note/Warning/Tip/Interview:**
6. ADD a ```mermaid diagram if the new concept has a visual component (flow, sequence, architecture)
7. ADD a comparison table if you're comparing approaches or trade-offs
8. Do NOT include YAML frontmatter
9. Target 400-600 words — write fully, do not cut short
10. Code must use the same language as the existing article
"""

DSA_SYSTEM = """You are a senior competitive programmer and FAANG interviewer. Write production-quality algorithm solutions with thorough explanations.

YOUR OUTPUT WILL BE REJECTED if any rule is violated.

OUTPUT FORMAT: A single fenced code block with the correct language tag. Nothing outside the code block.

INSIDE THE CODE BLOCK:

Lines 1-6 must be header comments in this EXACT format:
// Problem: <exact problem name>
// Language: <language name>
// Difficulty: <Easy|Medium|Hard|Super Advanced>
// Time Complexity: O(...) — with brief justification
// Space Complexity: O(...) — with brief justification
// Approach: <algorithm name and one-sentence description>
(use # for Python, /* */ for C/C++ if preferred)

SOLUTION REQUIREMENTS:
- COMPLETE and COMPILABLE — must run without modification
- Use standard LeetCode-style class/method signatures
- Every non-trivial line must have an inline comment explaining WHY
- Variable names must be descriptive (not single letters except loop counters)
- Handle ALL edge cases with explicit comments: // Edge case: empty input → return -1

FOR HARD AND SUPER_ADVANCED PROBLEMS:
- First show the brute force approach (commented out) with its complexity
- Then show the optimized solution with explanation of the improvement
- Add a comment block explaining the key insight that enables the optimization

EXAMPLE HEADER FORMAT:
// Problem: Two Sum
// Language: Java
// Difficulty: Easy
// Time Complexity: O(n) — single pass through array using HashMap
// Space Complexity: O(n) — HashMap stores at most n elements
// Approach: HashMap complement lookup — for each number, check if its complement exists
"""

DSA_SUMMARY_SYSTEM = """You are a senior algorithm expert and technical writer. Write a comprehensive, detailed explanation in Markdown.

YOUR OUTPUT WILL BE REJECTED if any section is missing or too short.

Use EXACTLY these sections in this exact order — do not skip any:

## Problem Understanding
3-4 sentences covering:
- What the problem is asking (in plain English)
- Key constraints and their implications
- What makes this problem non-trivial (why naive approach fails)

## Approach
4-5 sentences covering:
- The algorithm strategy and the intuition behind it
- Why this approach works (the mathematical/logical reasoning)
- What data structures are used and why they were chosen
- How the approach handles the key constraints

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(?)  | explain each term |
| Space  | O(?)  | explain what uses the space |

## Algorithm Walkthrough
Show a concrete step-by-step trace with a small example:
```
Input: [example input]
Step 1: [state of variables]
Step 2: [state of variables]
...
Output: [result]
```
Use a realistic example that exercises the main logic path.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[...]
    B --> C[...]
```
Show the algorithm's decision flow or data transformation visually.

## Key Insight
> **Tip:** The single most important insight — the "aha moment" that makes this solution click. Write it as a memorable one-liner.

## Edge Cases
Cover at least 3 edge cases:
- **Empty/null input**: [what happens and why]
- **Single element**: [what happens and why]
- **[Problem-specific edge case]**: [what happens and why]

## Common Mistakes
- **Mistake 1**: [what it is] → [how to avoid it]
- **Mistake 2**: [what it is] → [how to avoid it]

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → [brief answer]
- "Can you do it in O(1) space?" → [brief answer]
- "What if there are duplicates?" → [brief answer]

Do NOT include YAML frontmatter. Do NOT add preamble. Start directly with ## Problem Understanding.
"""

# ─── Topic exhaustion: ask AI to generate new topics ─────────────────────────

TOPIC_EXPANSION_SYSTEM = """You are a senior software engineer and curriculum designer. Your job is to generate NEW, UNIQUE programming topics that haven't been covered yet.

RULES:
1. Output ONLY a valid JSON array of strings — nothing else, no explanation, no markdown
2. Every topic must be specific and actionable (not vague like "Advanced Java")
3. No duplicates with the existing topics provided
4. Topics must be genuinely useful for software engineers and interview prep
5. Mix difficulty levels: some beginner-friendly, some advanced
6. Be specific: "Java Virtual Threads and Project Loom" not just "Java Concurrency"

OUTPUT FORMAT (exactly this, nothing else):
["Topic 1", "Topic 2", "Topic 3", ...]
"""

DSA_EXPANSION_SYSTEM = """You are a senior competitive programmer. Generate NEW, UNIQUE DSA problems that haven't been covered yet.

RULES:
1. Output ONLY a valid JSON object — nothing else, no explanation, no markdown
2. No duplicates with the existing problems provided
3. Problems must be real LeetCode-style problems with clear names
4. Mix classic problems with modern interview favorites

OUTPUT FORMAT (exactly this, nothing else):
{
  "easy": ["Problem 1", "Problem 2", ...],
  "medium": ["Problem 1", "Problem 2", ...],
  "hard": ["Problem 1", "Problem 2", ...],
  "super_advanced": ["Problem 1", "Problem 2", ...]
}
"""


# ─── Topic exhaustion: expand topics via AI when all are generated ────────────

def _all_notes_exhausted() -> bool:
    """Return True if every note topic across all files has already been generated."""
    for tf in topic_files:
        for section, content in tf["notes"].items():
            if isinstance(content, dict):
                for key, val in content.items():
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if not topic_str:
                            continue
                        path = f"docs/notes/{section}/{key}/{sanitize_filename(topic_str)}.md"
                        if path_is_available(path):
                            return False
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if not topic_str:
                        continue
                    path = f"docs/notes/{section}/{sanitize_filename(topic_str)}.md"
                    if path_is_available(path):
                        return False
    return True


def _all_dsa_exhausted() -> bool:
    """Return True if every DSA problem across all files has already been generated."""
    for tf in topic_files:
        for lang in LANGS:
            for diff in DIFFS:
                for q in tf["dsa_problems"][lang][diff]:
                    q = str(q).strip()
                    if not q:
                        continue
                    path = f"docs/notes/dsa/{lang}/{diff}/{sanitize_filename(q)}.md"
                    if path_is_available(path):
                        return False
    return True


def expand_note_topics(tf: dict, section: str, section_key: Optional[str]) -> int:
    """
    When a note section is exhausted, ask AI to generate 15 new unique topics for it.
    Appends them to the topic file's in-memory notes and saves the JSON.
    Returns the number of new topics added.
    """
    # Collect all existing topics in this section to avoid duplicates
    existing: List[str] = []
    content = tf["notes"].get(section, {})
    if isinstance(content, dict) and section_key:
        existing = flatten_to_strings(content.get(section_key, []))
    elif isinstance(content, list):
        existing = flatten_to_strings(content)

    existing_str = "\n".join(f"- {t}" for t in existing[:80])  # cap to avoid huge prompt

    print(f"🧠 Topics exhausted for [{section}/{section_key or ''}] — asking AI for new ones...")

    try:
        raw = call_groq(
            TOPIC_EXPANSION_SYSTEM,
            (
                f"Section: {section}" + (f" / {section_key}" if section_key else "") + "\n\n"
                f"Already covered topics (DO NOT repeat any of these):\n{existing_str}\n\n"
                f"Generate 15 NEW, SPECIFIC, UNIQUE topics for this section. "
                f"Output ONLY a JSON array of strings."
            ),
            max_tokens=800,
            context=f"expand topics: {section}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"⚠️  Could not expand topics for {section}: {e}")
        return 0

    # Parse the JSON array
    try:
        # Strip any markdown fences if AI wrapped it
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        new_topics: List[str] = json.loads(clean)
        if not isinstance(new_topics, list):
            raise ValueError("Expected a JSON array")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  AI returned invalid JSON for topic expansion: {e}\nRaw: {raw[:200]}")
        return 0

    # Deduplicate against existing
    existing_lower = {t.lower().strip() for t in existing}
    unique_new = [
        t for t in new_topics
        if isinstance(t, str) and t.strip() and t.lower().strip() not in existing_lower
    ]

    if not unique_new:
        print(f"⚠️  AI generated no new unique topics for {section}/{section_key}")
        return 0

    # Append to in-memory structure
    if isinstance(content, dict) and section_key:
        if section_key not in tf["notes"][section]:
            tf["notes"][section][section_key] = []
        if isinstance(tf["notes"][section][section_key], list):
            tf["notes"][section][section_key].extend(unique_new)
        else:
            tf["notes"][section][section_key] = flatten_to_strings(
                tf["notes"][section][section_key]
            ) + unique_new
    elif section in tf["notes"]:
        if isinstance(tf["notes"][section], list):
            tf["notes"][section].extend(unique_new)

    # Persist back to the JSON file
    fpath = os.path.join("topics", tf["filename"])
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            file_data = json.load(f)

        # Update the notes section in the file
        if "notes" not in file_data:
            file_data["notes"] = {}
        if section not in file_data["notes"]:
            file_data["notes"][section] = {}

        if isinstance(file_data["notes"][section], dict) and section_key:
            if section_key not in file_data["notes"][section]:
                file_data["notes"][section][section_key] = []
            file_data["notes"][section][section_key].extend(unique_new)
        elif isinstance(file_data["notes"][section], list):
            file_data["notes"][section].extend(unique_new)

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Added {len(unique_new)} new topics to {tf['filename']} [{section}/{section_key or ''}]")
        return len(unique_new)

    except Exception as e:
        print(f"⚠️  Could not save expanded topics to {fpath}: {e}")
        return len(unique_new)  # still added in-memory, can generate this run


def expand_dsa_problems(tf: dict, lang: str) -> int:
    """
    When DSA problems for a language are exhausted, ask AI to generate 20 new ones.
    Appends them to the topic file's in-memory problems and saves the JSON.
    Returns the number of new problems added.
    """
    existing_all: List[str] = []
    for diff in DIFFS:
        existing_all.extend(tf["dsa_problems"][lang][diff])

    existing_str = "\n".join(f"- {p}" for p in existing_all[:100])

    print(f"🧠 DSA problems exhausted for [{lang}] — asking AI for new ones...")

    try:
        raw = call_groq(
            DSA_EXPANSION_SYSTEM,
            (
                f"Language: {lang}\n\n"
                f"Already covered problems (DO NOT repeat any):\n{existing_str}\n\n"
                f"Generate 20 NEW, UNIQUE {lang} DSA problems (5 easy, 7 medium, 5 hard, 3 super_advanced). "
                f"Output ONLY a JSON object with keys: easy, medium, hard, super_advanced."
            ),
            max_tokens=800,
            context=f"expand DSA: {lang}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"⚠️  Could not expand DSA problems for {lang}: {e}")
        return 0

    try:
        clean = re.sub(r"```(?:json)?\s*|\s*```", "", raw).strip()
        new_problems: dict = json.loads(clean)
        if not isinstance(new_problems, dict):
            raise ValueError("Expected a JSON object")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  AI returned invalid JSON for DSA expansion: {e}\nRaw: {raw[:200]}")
        return 0

    existing_lower = {p.lower().strip() for p in existing_all}
    total_added = 0

    for diff in DIFFS:
        new_list = new_problems.get(diff, [])
        unique = [
            p for p in new_list
            if isinstance(p, str) and p.strip() and p.lower().strip() not in existing_lower
        ]
        tf["dsa_problems"][lang][diff].extend(unique)
        existing_lower.update(p.lower().strip() for p in unique)
        total_added += len(unique)

    # Persist to JSON file
    fpath = os.path.join("topics", tf["filename"])
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            file_data = json.load(f)

        if "problems" not in file_data:
            file_data["problems"] = {}
        if lang not in file_data["problems"]:
            file_data["problems"][lang] = {d: [] for d in DIFFS}

        for diff in DIFFS:
            new_list = new_problems.get(diff, [])
            existing_in_file = {p.lower().strip() for p in file_data["problems"][lang].get(diff, [])}
            unique = [
                p for p in new_list
                if isinstance(p, str) and p.strip() and p.lower().strip() not in existing_in_file
            ]
            file_data["problems"][lang].setdefault(diff, []).extend(unique)

        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(file_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Added {total_added} new DSA problems to {tf['filename']} [{lang}]")
    except Exception as e:
        print(f"⚠️  Could not save expanded DSA problems to {fpath}: {e}")

    return total_added


# ─── File-first topic pickers ─────────────────────────────────────────────────

def pick_topic_file_with_new_notes() -> Optional[dict]:
    """Randomly select a topic file that has at least one ungenerated note."""
    candidates = []
    for tf in topic_files:
        found = False
        for section, content in tf["notes"].items():
            if found:
                break
            if isinstance(content, dict):
                for key, val in content.items():
                    if found:
                        break
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if not topic_str:
                            continue
                        path = f"docs/notes/{section}/{key}/{sanitize_filename(topic_str)}.md"
                        if path_is_available(path):
                            candidates.append(tf)
                            found = True
                            break
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if not topic_str:
                        continue
                    path = f"docs/notes/{section}/{sanitize_filename(topic_str)}.md"
                    if path_is_available(path):
                        candidates.append(tf)
                        found = True
                        break
    if not candidates:
        return None
    return random.choice(candidates)


def pick_topic_file_with_new_dsa() -> Optional[dict]:
    """Randomly select a topic file that has at least one ungenerated DSA problem."""
    candidates = []
    for tf in topic_files:
        found = False
        for lang in LANGS:
            if found:
                break
            for diff in DIFFS:
                if found:
                    break
                for q in tf["dsa_problems"][lang][diff]:
                    q = str(q).strip()
                    if not q:
                        continue
                    path = f"docs/notes/dsa/{lang}/{diff}/{sanitize_filename(q)}.md"
                    if path_is_available(path):
                        candidates.append(tf)
                        found = True
                        break
    if not candidates:
        return None
    return random.choice(candidates)


def pick_new_note_from_file(tf: dict) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
    """From a specific topic file, pick a random ungenerated note."""
    all_triples: List[Tuple[str, Optional[str], str]] = []
    for section, content in tf["notes"].items():
        if isinstance(content, dict):
            for key, val in content.items():
                for topic_str in flatten_to_strings(val):
                    topic_str = topic_str.strip()
                    if topic_str:
                        all_triples.append((section, key, topic_str))
        else:
            for topic_str in flatten_to_strings(content):
                topic_str = topic_str.strip()
                if topic_str:
                    all_triples.append((section, None, topic_str))

    random.shuffle(all_triples)

    for section, section_key, note in all_triples:
        path = (
            f"docs/notes/{section}/{section_key}/{sanitize_filename(note)}.md"
            if section_key
            else f"docs/notes/{section}/{sanitize_filename(note)}.md"
        )
        if path_is_available(path):
            return note, path, section, section_key

    return None, None, None, None


def pick_dsa_from_file(tf: dict) -> Tuple[Optional[str], Optional[str], str, str]:
    """From a specific topic file, pick a random ungenerated DSA problem."""
    all_items: List[Tuple[str, str, str]] = []
    for lang in LANGS:
        for diff in DIFFS:
            for q in tf["dsa_problems"][lang][diff]:
                q = str(q).strip()
                if q:
                    all_items.append((lang, diff, q))

    random.shuffle(all_items)

    for lang, difficulty, question in all_items:
        path = f"docs/notes/dsa/{lang}/{difficulty}/{sanitize_filename(question)}.md"
        if path_is_available(path):
            return question, path, lang, difficulty

    return None, None, "java", "easy"


def pick_note_to_update() -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], int]:
    """Pick any existing note that can still be updated (update_count < MAX_UPDATES)."""
    shuffled_files = topic_files[:]
    random.shuffle(shuffled_files)

    for tf in shuffled_files:
        all_triples: List[Tuple[str, Optional[str], str]] = []
        for section, content in tf["notes"].items():
            if isinstance(content, dict):
                for key, val in content.items():
                    for topic_str in flatten_to_strings(val):
                        topic_str = topic_str.strip()
                        if topic_str:
                            all_triples.append((section, key, topic_str))
            else:
                for topic_str in flatten_to_strings(content):
                    topic_str = topic_str.strip()
                    if topic_str:
                        all_triples.append((section, None, topic_str))

        random.shuffle(all_triples)
        for section, section_key, note in all_triples:
            path = (
                f"docs/notes/{section}/{section_key}/{sanitize_filename(note)}.md"
                if section_key
                else f"docs/notes/{section}/{sanitize_filename(note)}.md"
            )
            count = path_is_updatable(path)
            if count is not None:
                return note, path, section, section_key, count

    return None, None, None, None, 0


# ─── Content generators ───────────────────────────────────────────────────────

def generate_dsa() -> Optional[str]:
    """
    Generate one DSA problem article.
    Flow: pick file → pick problem → call Groq (code) → call Groq (summary)
          → validate both → write file
    If all problems exhausted: ask AI to generate new ones, then continue.
    ALL Groq calls happen before ANY file is written.
    Raises GroqQuotaError / GroqAuthError to bubble up to main().
    """
    tf = pick_topic_file_with_new_dsa()
    if not tf:
        # All DSA problems exhausted — ask AI to generate new ones
        if _all_dsa_exhausted():
            print("🧠 All DSA problems exhausted — expanding via AI...")
            # Pick a random file and language to expand
            expand_tf = random.choice(topic_files)
            expand_lang = random.choice(list(LANGS))
            added = expand_dsa_problems(expand_tf, expand_lang)
            if added == 0:
                print("⚠️  AI could not generate new DSA problems — skipping DSA this run.")
                return None
            # Retry pick after expansion
            tf = pick_topic_file_with_new_dsa()
            if not tf:
                print("⚠️  Still no DSA problems available after expansion.")
                return None
        else:
            print("⚠️  No DSA file with available problems found.")
            return None

    question, md_path, lang, difficulty = pick_dsa_from_file(tf)
    if not question:
        print("⚠️  No available DSA problem found in selected file.")
        return None

    print(f"🔧 DSA [{lang}/{difficulty}] from [{tf['filename']}]: {question}")

    lang_tag = {"cpp": "cpp", "c": "c", "python": "python",
                "javascript": "javascript", "java": "java"}.get(lang, lang)

    # ── Step 1: Generate code solution ──────────────────────────────────────
    try:
        code_raw = call_groq(
            DSA_SYSTEM,
            (
                f"Problem: {question}\n"
                f"Language: {lang}\n"
                f"Difficulty: {difficulty}\n"
                f"Write the complete {lang} solution. "
                f"Handle all edge cases. Output ONLY the fenced code block."
            ),
            max_tokens=2500,
            context=f"DSA code: {question}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise  # bubble up — stop the run
    except GroqAPIError as e:
        print(f"❌ DSA code generation failed for '{question}': {e}")
        return None

    # Extract code from fenced block
    code_match = re.search(rf"```{re.escape(lang_tag)}\s*([\s\S]*?)```", code_raw)
    if not code_match:
        code_match = re.search(r"```\w*\s*([\s\S]*?)```", code_raw)
    code = (
        code_match.group(1).strip()
        if code_match
        else re.sub(r"```\w*\s*|```", "", code_raw).strip()
    )

    # ── Step 2: Generate summary/explanation ────────────────────────────────
    try:
        summary = call_groq(
            DSA_SUMMARY_SYSTEM,
            (
                f"Problem: {question}\n"
                f"Language: {lang}\n"
                f"Difficulty: {difficulty}\n"
                f"Solution code:\n```{lang_tag}\n{code}\n```"
            ),
            max_tokens=1000,
            context=f"DSA summary: {question}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"❌ DSA summary generation failed for '{question}': {e}")
        return None

    # ── Step 3: Validate content before writing ──────────────────────────────
    try:
        validate_dsa_content(code, summary, question)
    except ContentValidationError as e:
        print(f"❌ DSA content validation failed for '{question}': {e}")
        return None

    # ── Step 4: Write file ───────────────────────────────────────────────────
    banner_url = (
        f"https://image.pollinations.ai/prompt/"
        f"{url_encode(question)}%20{url_encode(lang)}%20algorithm"
        f"?width=800&height=400&nologo=true"
    )
    md_content = (
        f'---\n'
        f'title: "{question}"\n'
        f'language: "{lang}"\n'
        f'difficulty: "{difficulty}"\n'
        f'section: "dsa"\n'
        f'tags: "dsa, {lang}, {difficulty}, leetcode, algorithms, coding-interview"\n'
        f'banner: "{banner_url}"\n'
        f'update_count: 0\n'
        f'---\n\n'
        f'# {question}\n\n'
        f'![{question}]({banner_url})\n\n'
        f'{summary}\n\n'
        f'## {lang.upper() if lang in ("cpp", "c") else lang.capitalize()} Solution\n\n'
        f'```{lang_tag}\n{code}\n```\n'
    )

    save_file(md_path, md_content)
    print(f"✅ DSA article written: {md_path}")
    return f"📘 DSA [{lang}/{difficulty}]: {question}"


def generate_note() -> Optional[str]:
    """
    Generate one conceptual note article.
    Flow: pick file → pick topic → call Groq → validate → write file
    If all topics exhausted: ask AI to generate new ones, then continue.
    Falls back to update_existing_note() only if expansion also fails.
    Raises GroqQuotaError / GroqAuthError to bubble up to main().
    """
    tf = pick_topic_file_with_new_notes()
    if not tf:
        # All note topics exhausted — ask AI to generate new ones
        if _all_notes_exhausted():
            print("🧠 All note topics exhausted — expanding via AI...")
            # Pick a random file and section to expand
            expand_tf = random.choice(topic_files)
            if expand_tf["notes"]:
                expand_section = random.choice(list(expand_tf["notes"].keys()))
                expand_content = expand_tf["notes"][expand_section]
                expand_key = None
                if isinstance(expand_content, dict):
                    expand_key = random.choice(list(expand_content.keys()))
                added = expand_note_topics(expand_tf, expand_section, expand_key)
                if added > 0:
                    tf = pick_topic_file_with_new_notes()
            if not tf:
                print("⚠️  AI expansion failed — falling back to update existing note.")
                return update_existing_note()
        else:
            print("⚠️  No note file with available topics found — trying update.")
            return update_existing_note()

    note, path, section, section_key = pick_new_note_from_file(tf)
    if not note:
        print("⚠️  No available note in selected file — trying update instead.")
        return update_existing_note()

    label = f"{section}/{section_key}" if section_key else section
    print(f"📝 Note [{label}] from [{tf['filename']}]: {note}")

    banner_url = (
        f"https://image.pollinations.ai/prompt/"
        f"{url_encode(note)}%20{url_encode(section)}%20programming"
        f"?width=800&height=400&nologo=true"
    )

    # ── Step 1: Generate content ─────────────────────────────────────────────
    try:
        content_body = call_groq(
            NOTE_SYSTEM,
            (
                f"Topic: **{note}**\n"
                f"Learning path: **{section}**"
                + (f" → **{section_key}**" if section_key else "")
                + "\n\n"
                f"BANNER IMAGE — use this exact URL as the very first line:\n"
                f"![{note}]({banner_url})\n\n"
                f"MANDATORY CHECKLIST — your response will be rejected if any item is missing:\n"
                f"☐ Banner image as the very first line (URL above)\n"
                f"☐ ## Introduction — what it is, why it matters, real-world relevance\n"
                f"☐ ## Core Concepts — precise definitions, mental models, key terminology\n"
                f"☐ ## How It Works Internally — under-the-hood mechanics, step-by-step\n"
                f"☐ ## Code Examples — 3 COMPLETE, RUNNABLE examples (basic → advanced)\n"
                f"☐ ## Visual Diagram — MUST contain a ```mermaid block with 6+ nodes\n"
                f"☐ ## Comparison — MUST contain a Markdown table with 4+ rows\n"
                f"☐ ## Real-world Use Cases — 3+ production examples with company/system names\n"
                f"☐ ## Common Pitfalls — 4+ specific mistakes with wrong vs right code\n"
                f"☐ ## Interview Tips — 3+ common questions with weak vs strong answers\n"
                f"☐ ## Key Takeaways — 6-10 bullet points of must-remember facts\n\n"
                f"QUALITY REQUIREMENTS:\n"
                f"- Every code block must be COMPLETE and RUNNABLE — no '...' or pseudocode\n"
                f"- Include time/space complexity for every algorithm mentioned\n"
                f"- Use > **Note/Warning/Tip/Interview:** callouts throughout (minimum 4)\n"
                f"- Target 1200-1600 words — write fully, do not cut short\n"
                f"- Production-quality content that a senior engineer would be proud of"
            ),
            max_tokens=4096,
            context=f"Note: {note}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"❌ Note generation failed for '{note}': {e}")
        return None

    # ── Step 2: Validate content before writing ──────────────────────────────
    try:
        validate_note_content(content_body, note)
    except ContentValidationError as e:
        print(f"❌ Note content validation failed for '{note}': {e}")
        return None

    # ── Step 3: Write file ───────────────────────────────────────────────────
    tags = [
        section,
        note.split(":")[0].strip().lower().replace(" ", "-").replace("/", "-"),
        "programming",
        "notes",
        "interview",
    ]
    frontmatter = build_frontmatter(note, note, section, tags, update_count=0)
    save_file(path, frontmatter + "\n" + content_body)
    print(f"✅ Note article written: {path}")
    return f"📝 [{label}] {note}"


def update_existing_note() -> Optional[str]:
    """
    Append a new section to an existing note.
    On GroqAPIError, restores the original file content.
    Raises GroqQuotaError / GroqAuthError to bubble up to main().
    """
    note, path, section, section_key, current_count = pick_note_to_update()
    if not note:
        print("⚠️  No notes available to update either.")
        return None

    label = f"{section}/{section_key}" if section_key else section
    print(f"🔄 Update [{label}]: {note} → v{current_count + 1}")

    with open(path, "r", encoding="utf-8") as f:
        existing = f.read()

    body = re.sub(r"^---\r?\n[\s\S]*?\r?\n---\r?\n", "", existing).strip()

    # ── Step 1: Generate new section ────────────────────────────────────────
    try:
        new_section_text = call_groq(
            UPDATE_SYSTEM,
            (
                f"Existing article about '{note}' (section: {section}):\n\n"
                f"{body[:3000]}\n\n"
                f"Append a new advanced section covering a distinct sub-topic, "
                f"advanced pattern, or real-world use case NOT already covered above. "
                f"Include a complete code example and at least one callout."
            ),
            max_tokens=2048,
            context=f"Update: {note}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"❌ Note update failed for '{note}': {e}")
        return None

    # ── Step 2: Validate new section ────────────────────────────────────────
    if not new_section_text or len(new_section_text.strip()) < 100:
        print(f"❌ Update content too short for '{note}' — skipping")
        return None

    if not re.search(r"^#{1,3} .+", new_section_text.strip(), re.MULTILINE):
        print(f"❌ Update content missing heading for '{note}' — skipping")
        return None

    # ── Step 3: Write updated file ───────────────────────────────────────────
    new_count = current_count + 1
    meta = read_frontmatter(path)
    tags_raw = meta.get("tags", f"{section}, programming, notes")
    tags = [t.strip() for t in tags_raw.split(",")]
    new_frontmatter = build_frontmatter(
        note,
        meta.get("topic", note),
        meta.get("section", section),
        tags,
        new_count,
    )

    try:
        save_file(path, new_frontmatter + "\n" + body + "\n\n" + new_section_text)
        print(f"✅ Note updated: {path}")
        return f"🔄 [{label}] {note} (v{new_count})"
    except Exception as e:
        print(f"❌ Failed to write updated note '{note}': {e}")
        # Restore original
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(existing)
            print(f"↩️  Restored original: {path}")
            norm = path.replace("\\", "/")
            _written_this_run.discard(norm)
        except Exception as restore_err:
            print(f"⚠️  Could not restore {path}: {restore_err}")
        return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").lower()

    try:
        run_count = int(os.environ.get("RUN_COUNT", "5"))
    except ValueError:
        run_count = 5

    # Local runs generate 1 article; CI runs use RUN_COUNT
    if event_name not in ("schedule", "workflow_dispatch"):
        run_count = 1

    # Scheduled runs: random delay to spread load across the cron window
    if event_name == "schedule":
        delay = random.randint(0, 300)
        print(f"⏱️  Scheduled run — sleeping {delay}s before starting...")
        time.sleep(delay)
    else:
        print(f"▶️  Event: {event_name or 'local'}")

    print(f"🎯 Generating {run_count} article(s) this run\n")

    # ── Preflight: verify API key and quota BEFORE any generation ────────────
    if not preflight_check():
        if _quota_exhausted:
            print("⚠️  Quota exhausted — no articles generated this run.")
            # Exit 0: not a script error, just nothing to do
            sys.exit(0)
        else:
            print("❌ Preflight check failed — aborting run.")
            sys.exit(1)

    print()

    commit_messages: List[str] = []
    failed_count = 0
    quota_hit = False

    for i in range(run_count):
        print(f"\n─── Article {i + 1}/{run_count} ───")

        try:
            # 40% DSA problem solutions, 60% conceptual notes
            if random.random() < 0.40:
                msg = generate_dsa()
            else:
                msg = generate_note()

            if msg:
                commit_messages.append(msg)
            else:
                failed_count += 1

        except GroqAuthError as e:
            # Fatal — invalid key or model gone, stop everything
            print(f"❌ FATAL auth error: {e}")
            break

        except GroqQuotaError as e:
            # Quota hit mid-run — commit what we have and stop
            print(f"❌ Quota exhausted mid-run: {e}")
            print("⚠️  Stopping generation — will commit articles generated so far.")
            quota_hit = True
            break

        except Exception as e:
            # Unexpected error — log it, count as failure, continue
            print(f"❌ Unexpected error on article {i + 1}: {e}")
            failed_count += 1

        # Brief pause between articles to avoid hammering the API
        if i < run_count - 1 and not quota_hit:
            time.sleep(10)

    # ── Commit everything that succeeded ─────────────────────────────────────
    if commit_messages:
        if len(commit_messages) == 1:
            batch_msg = commit_messages[0]
        else:
            titles = "\n".join(f"  • {m}" for m in commit_messages)
            batch_msg = f"🤖 Auto-generated {len(commit_messages)} articles\n\n{titles}"

        success = commit_and_push(batch_msg)
        if not success:
            print("⚠️  Batch push failed — attempting per-article fallback commits...")
            for msg in commit_messages:
                commit_and_push(msg)
    else:
        print("⚠️  No articles were generated this run.")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_attempted = len(commit_messages) + failed_count
    print(f"\n{'─' * 50}")
    print(f"✅ Done. {len(commit_messages)}/{total_attempted} articles generated successfully.")
    if failed_count > 0:
        print(f"⚠️  {failed_count} article(s) failed (see logs above for reasons).")
    if quota_hit:
        print("⚠️  Run stopped early due to quota exhaustion.")

    # Exit 1 only if EVERY article failed (marks GH Actions run red)
    if failed_count > 0 and len(commit_messages) == 0:
        print("❌ All articles failed. Exiting with error.")
        sys.exit(1)


if __name__ == "__main__":
    main()
