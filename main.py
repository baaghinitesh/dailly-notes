#!/usr/bin/env python3
"""
main.py — Groq/Llama-3 powered content engine for dailly-notes

Guarantees:
  - No duplicate articles: checks os.path.exists AND tracks generated paths in-memory
  - Fair section coverage: shuffles ALL (section, topic) pairs globally, not section-first
  - Batch commit: all articles in a run committed together in one push
  - Per-article commit fallback: if batch push fails, retries per-article
  - Exponential backoff on Groq rate limits
  - 3 scheduled runs/day × 3 articles = ~9 new articles/day
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

if not GROQ_API_KEY:
    print("❌ Missing GROQ_API_KEY environment variable")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

# In-memory set of paths written this run — prevents same-run duplicates
# even before the file is committed to disk by another iteration
_written_this_run: set = set()

# ─── Load topics ──────────────────────────────────────────────────────────────

def load_all_topics() -> dict:
    """
    Load all topics from the topics/ directory.
    - DSA easy/medium/hard lists come from topics/dsa.json
    - All notes sections come from the per-language/topic JSON files
    Later files in sorted order overwrite earlier ones for the same notes key.
    """
    merged: dict = {"easy": [], "medium": [], "hard": [], "notes": {}}
    topics_dir = "topics"

    if not os.path.isdir(topics_dir):
        print("❌ topics/ directory not found")
        sys.exit(1)

    for fname in sorted(os.listdir(topics_dir)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(topics_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in ("easy", "medium", "hard"):
                if key in data:
                    merged[key].extend(data[key])
            for subject, content in data.get("notes", {}).items():
                merged["notes"][subject] = content
        except Exception as e:
            print(f"⚠️  Failed to load {fpath}: {e}")

    return merged


topics = load_all_topics()
print(
    f"📚 Loaded: {len(topics.get('easy', []))} easy, "
    f"{len(topics.get('medium', []))} medium, "
    f"{len(topics.get('hard', []))} hard DSA problems | "
    f"{len(topics.get('notes', {}))} note subjects"
)

# ─── Helpers ──────────────────────────────────────────────────────────────────

def flatten_to_strings(value: Any) -> List[str]:
    """Recursively flatten any nested structure to a list of strings."""
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
    """Parse YAML frontmatter block from a Markdown file."""
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
    """True if the file doesn't exist on disk AND wasn't written this run."""
    return path not in _written_this_run and not os.path.exists(path)


def path_is_updatable(path: str) -> Optional[int]:
    """
    Returns current update_count if the file exists and count < MAX_UPDATES.
    Returns None otherwise.
    """
    if path in _written_this_run:
        return None  # already touched this run
    if not os.path.exists(path):
        return None
    meta = read_frontmatter(path)
    count = int(meta.get("update_count", 0))
    return count if count < MAX_UPDATES else None

# ─── Groq API ─────────────────────────────────────────────────────────────────

def call_groq(
    system: str, user: str, max_tokens: int = 4096, retries: int = 4
) -> str:
    """Call Groq with exponential backoff on rate limits."""
    for attempt in range(1, retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "429" in err:
                wait = 2 ** attempt * 10  # 20s, 40s, 80s, 160s
                print(f"⏳ Rate limited. Waiting {wait}s (attempt {attempt}/{retries})...")
                time.sleep(wait)
            elif "model_decommissioned" in err.lower() or "model_not_found" in err.lower():
                # Non-retryable — wrong model ID, fail immediately
                print(f"❌ Fatal Groq error (model issue): {e}")
                sys.exit(1)
            else:
                print(f"❌ Groq error (attempt {attempt}): {e}")
                if attempt == retries:
                    return f"⚠️ Content generation failed after {retries} attempts: {e}"
                time.sleep(5)
    return "⚠️ Content generation failed."

# ─── System prompts ───────────────────────────────────────────────────────────

NOTE_SYSTEM = """You are an expert technical writer creating premium, in-depth study notes for software engineers preparing for interviews and building real-world skills.

STRICT FORMATTING RULES — follow every rule exactly:

1. START directly with content — no preamble like "Here are the notes" or "Sure!"

2. STRUCTURE every article with these sections (use ## headings):
   - Introduction (what it is, why it matters)
   - Core Concepts (theory, definitions, mental models)
   - Code Examples (at least 3 practical, real-world examples)
   - Real-world Use Cases
   - Common Pitfalls & How to Avoid Them
   - Summary / Key Takeaways

3. CODE BLOCKS — always use fenced blocks with the correct language tag:
   ```java  ```javascript  ```typescript  ```python  ```go  ```rust  ```cpp  ```bash  ```sql  ```yaml  ```json

4. BANNER IMAGE — include exactly this at the very top (before Introduction):
   ![Topic Name](https://image.pollinations.ai/prompt/TOPIC_URL_ENCODED%20programming?width=800&height=400&nologo=true)

5. MERMAID DIAGRAMS — use ```mermaid for architecture, flow, sequence, or class diagrams:
   ```mermaid
   graph TD
     A[Client] --> B[API Gateway]
     B --> C[Service A]
     B --> D[Service B]
   ```

6. CALLOUTS — use blockquotes for notes, warnings, and tips:
   > **Note:** This is important.
   > **Warning:** Avoid this pitfall.
   > **Tip:** Use this pattern for better performance.

7. COMPARISON TABLES — use Markdown tables when comparing approaches or complexity:
   | Approach | Time | Space | When to Use |
   |----------|------|-------|-------------|

8. DEPTH — cover both beginner understanding AND advanced nuances:
   - Time/space complexity where relevant
   - Performance considerations
   - Interview tips where applicable
   - Mention related concepts (do not hyperlink)

9. Do NOT include YAML frontmatter — that is added separately.
10. Aim for 700-1200 words of rich, dense, practical content.
"""

UPDATE_SYSTEM = """You are an expert technical writer updating an existing study article.

STRICT RULES:
1. Do NOT rewrite existing content — only APPEND a new section at the end
2. The new section MUST cover a distinct sub-topic, advanced pattern, or real-world use case NOT already in the article
3. Use the same Markdown formatting as the existing article
4. Include at least one new fenced code block with the correct language tag
5. Start your response with a new ## heading
6. Add a Mermaid diagram if it helps explain the new section
7. Do NOT include YAML frontmatter
8. Do NOT add any preamble — start directly with the ## heading
"""

DSA_SYSTEM = """You are an expert competitive programmer. Write clean, well-commented Java solutions.

STRICT RULES:
1. Output ONLY raw Java code — no markdown fences, no explanation text outside comments
2. Class name must be CamelCase derived from the problem name
3. Line 1: // Problem: <problem name>
4. Line 2: // Difficulty: <difficulty>
5. Line 3: // Time Complexity: O(...)
6. Line 4: // Space Complexity: O(...)
7. Include inline comments explaining key algorithmic steps
8. The solution must be complete and compilable
9. Use standard LeetCode-style method signatures
"""

DSA_SUMMARY_SYSTEM = """You are a technical writer. Write a concise algorithm explanation.

FORMAT (use exactly these headings):

## Approach
[2-3 sentences explaining the algorithm strategy]

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(?)  | ...    |
| Space  | O(?)  | ...    |

## Key Insight
> **Tip:** [The core insight that makes this solution efficient]

## Edge Cases
- [Edge case 1]
- [Edge case 2]
"""

# ─── Smart pickers (no duplicates, fair coverage) ─────────────────────────────

def pick_new_note() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Pick a (note, path, section) that has never been generated.

    Strategy: build a flat list of ALL (section, topic) pairs across ALL sections,
    shuffle it globally, then find the first one whose file doesn't exist.
    This ensures fair coverage across all subjects — no section gets starved.
    """
    notes_root = topics.get("notes", {})
    if not notes_root:
        return None, None, None

    # Build flat list of all (section, topic_string) pairs
    all_pairs: List[Tuple[str, str]] = []
    for section, content in notes_root.items():
        for topic_str in flatten_to_strings(content):
            topic_str = topic_str.strip()
            if topic_str:
                all_pairs.append((section, topic_str))

    random.shuffle(all_pairs)

    for section, note in all_pairs:
        path = f"docs/notes/{section}/{sanitize_filename(note)}.md"
        if path_is_available(path):
            return note, path, section

    return None, None, None


def pick_note_to_update() -> Tuple[Optional[str], Optional[str], Optional[str], int]:
    """
    Pick a (note, path, section, count) for an existing article that can still be updated.

    Strategy: same global shuffle across all sections for fairness.
    """
    notes_root = topics.get("notes", {})
    if not notes_root:
        return None, None, None, 0

    all_pairs: List[Tuple[str, str]] = []
    for section, content in notes_root.items():
        for topic_str in flatten_to_strings(content):
            topic_str = topic_str.strip()
            if topic_str:
                all_pairs.append((section, topic_str))

    random.shuffle(all_pairs)

    for section, note in all_pairs:
        path = f"docs/notes/{section}/{sanitize_filename(note)}.md"
        count = path_is_updatable(path)
        if count is not None:
            return note, path, section, count

    return None, None, None, 0


def pick_dsa() -> Tuple[Tuple[Optional[str], Optional[str]], str]:
    """
    Pick a DSA problem that hasn't been solved yet.

    Strategy: shuffle ALL difficulties together so we don't get stuck
    if one difficulty pool is exhausted.
    """
    all_dsa: List[Tuple[str, str]] = []
    for difficulty in ("easy", "medium", "hard"):
        for q in topics.get(difficulty, []):
            q = str(q).strip()
            if q:
                all_dsa.append((difficulty, q))

    random.shuffle(all_dsa)

    for difficulty, question in all_dsa:
        path = f"docs/dsa/{difficulty}/{sanitize_filename(question)}.md"
        if path_is_available(path):
            return (question, path), difficulty

    return (None, None), "easy"

# ─── File I/O ─────────────────────────────────────────────────────────────────

def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    _written_this_run.add(path)
    print(f"📄 Written: {path} ({len(content):,} chars)")

# ─── Git ──────────────────────────────────────────────────────────────────────

def commit_and_push(message: str, retries: int = 3) -> bool:
    """Stage all changes, commit, and push. Returns True on success."""
    for attempt in range(1, retries + 1):
        try:
            repo = git.Repo(".")
            repo.git.add(A=True)
            if not repo.is_dirty(untracked_files=True):
                print("ℹ️  Nothing to commit.")
                return True
            repo.index.commit(
                message,
                author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL)
            )
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

# ─── Content generators ───────────────────────────────────────────────────────

def generate_dsa() -> Optional[str]:
    """Generate one DSA article. Returns commit message or None on failure."""
    (question, md_path), difficulty = pick_dsa()
    if not question:
        print("⚠️  All DSA problems already generated.")
        return None

    print(f"🔧 DSA [{difficulty}]: {question}")

    java_code = call_groq(
        DSA_SYSTEM,
        f"Problem: {question}\nDifficulty: {difficulty}\nWrite the complete Java solution.",
        max_tokens=2048,
    )
    java_code = re.sub(r"```java\s*|```\s*", "", java_code).strip()

    summary = call_groq(
        DSA_SUMMARY_SYSTEM,
        f"Problem: {question}\nDifficulty: {difficulty}\nJava solution:\n{java_code}",
        max_tokens=700,
    )

    java_path = md_path.replace(".md", ".java")
    save_file(java_path, java_code)

    banner_url = (
        f"https://image.pollinations.ai/prompt/"
        f"{url_encode(question)}%20algorithm%20data%20structure"
        f"?width=800&height=400&nologo=true"
    )
    md_content = (
        f'---\n'
        f'title: "{question}"\n'
        f'difficulty: "{difficulty}"\n'
        f'tags: "dsa, {difficulty}, java, leetcode"\n'
        f'banner: "{banner_url}"\n'
        f'update_count: 0\n'
        f'---\n\n'
        f'# {question}\n\n'
        f'![{question}]({banner_url})\n\n'
        f'{summary}\n\n'
        f'## Java Solution\n\n'
        f'```java\n{java_code}\n```\n'
    )
    save_file(md_path, md_content)
    return f"📘 DSA [{difficulty}]: {question}"


def generate_note() -> Optional[str]:
    """Generate one new note article. Returns commit message or None."""
    note, path, section = pick_new_note()
    if not note:
        print("⚠️  All note topics already generated — trying update instead.")
        return update_existing_note()

    print(f"📝 Note [{section}]: {note}")

    content_body = call_groq(
        NOTE_SYSTEM,
        (
            f"Write comprehensive, in-depth study notes for: **{note}**\n"
            f"Context: This is part of the **{section}** learning path.\n"
            f"Include the banner image at the very top using this URL:\n"
            f"https://image.pollinations.ai/prompt/"
            f"{url_encode(note)}%20{url_encode(section)}%20programming"
            f"?width=800&height=400&nologo=true\n"
            f"Make the content rich, practical, and interview-ready."
        ),
        max_tokens=4096,
    )

    tags = [
        section,
        note.split(":")[0].strip().lower().replace(" ", "-").replace("/", "-"),
        "programming",
        "notes",
    ]
    frontmatter = build_frontmatter(note, note, section, tags, update_count=0)
    save_file(path, frontmatter + "\n" + content_body)
    return f"📝 [{section}] {note}"


def update_existing_note() -> Optional[str]:
    """Append a new section to an existing note. Returns commit message or None."""
    note, path, section, current_count = pick_note_to_update()
    if not note:
        print("⚠️  No notes available to update either.")
        return None

    print(f"🔄 Update [{section}]: {note} → v{current_count + 1}")

    with open(path, "r", encoding="utf-8") as f:
        existing = f.read()

    body = re.sub(r"^---\r?\n[\s\S]*?\r?\n---\r?\n", "", existing).strip()

    new_section_text = call_groq(
        UPDATE_SYSTEM,
        (
            f"Existing article about '{note}' (section: {section}):\n\n"
            f"{body[:3000]}\n\n"
            f"Append a new advanced section covering a distinct sub-topic, "
            f"advanced pattern, or real-world use case not already covered."
        ),
        max_tokens=2048,
    )

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

    save_file(path, new_frontmatter + "\n" + body + "\n\n" + new_section_text)
    return f"🔄 [{section}] {note} (v{new_count})"

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").lower()

    try:
        run_count = int(os.environ.get("RUN_COUNT", "3"))
    except ValueError:
        run_count = 3

    # Local runs default to 1 to avoid accidental bulk generation
    if event_name not in ("schedule", "workflow_dispatch"):
        run_count = 1

    # Scheduled: small random delay (0–5 min) to spread load across GitHub infra
    if event_name == "schedule":
        delay = random.randint(0, 300)
        print(f"⏱️  Scheduled run — sleeping {delay}s before starting...")
        time.sleep(delay)
    else:
        print(f"▶️  Event: {event_name or 'local'}")

    print(f"🎯 Generating {run_count} article(s) this run\n")

    commit_messages: List[str] = []

    for i in range(run_count):
        print(f"\n─── Article {i + 1}/{run_count} ───")

        # 35% DSA, 65% notes — notes are richer for launchyourconcept readers
        if random.random() < 0.35:
            msg = generate_dsa()
        else:
            msg = generate_note()

        if msg:
            commit_messages.append(msg)

        # Pause between Groq calls to stay within rate limits
        if i < run_count - 1:
            time.sleep(10)

    # ── Batch commit + push ──────────────────────────────────────────────────
    if commit_messages:
        # Build a single descriptive commit message
        if len(commit_messages) == 1:
            batch_msg = commit_messages[0]
        else:
            titles = "\n".join(f"  • {m}" for m in commit_messages)
            batch_msg = f"🤖 Auto-generated {len(commit_messages)} articles\n\n{titles}"

        success = commit_and_push(batch_msg)
        if not success:
            # Fallback: try committing each file individually
            print("⚠️  Batch push failed — attempting per-article fallback commits...")
            for msg in commit_messages:
                commit_and_push(msg)
    else:
        print("⚠️  No articles were generated this run.")

    print(f"\n✅ Done. {len(commit_messages)}/{run_count} articles generated.")


if __name__ == "__main__":
    main()
