#!/usr/bin/env python3
"""
main.py — Groq/Llama-3 powered content engine for dailly-notes
- Generates rich Markdown notes with YAML frontmatter
- Tracks update_count per article (max 5 updates before skipping)
- Generates DSA solutions in Java with Markdown wrapper
- Proper rate limiting and retry logic for Groq API
- No signal.SIGALRM (cross-platform safe)
- Single workflow: generate → commit → deploy
"""

import os
import random
import sys
import json
import time
import re
import git
from typing import Any, List, Iterable
from groq import Groq

# ─── Config ───────────────────────────────────────────────────────────────────

GROQ_API_KEY  = os.environ.get("GROQ_API_KEY")
AUTHOR_NAME   = os.environ.get("AUTHOR_NAME", "baaghinitesh")
AUTHOR_EMAIL  = os.environ.get("AUTHOR_EMAIL", "baaghinitesh@gmail.com")
MODEL         = "llama3-70b-8192"   # Groq's fastest large model
MAX_UPDATES   = 5                   # max times an article gets updated

if not GROQ_API_KEY:
    print("❌ Missing GROQ_API_KEY environment variable")
    sys.exit(1)

client = Groq(api_key=GROQ_API_KEY)

# ─── Load topics ──────────────────────────────────────────────────────────────

def load_all_topics() -> dict:
    """
    Load and merge all topic files:
    - topics/dsa.json        → easy, medium, hard, notes.dsa
    - topics/*.json          → notes.<subject>
    Falls back to legacy topics.json if topics/ dir doesn't exist.
    """
    merged: dict = {"easy": [], "medium": [], "hard": [], "notes": {}}

    topics_dir = "topics"
    if os.path.isdir(topics_dir):
        for fname in sorted(os.listdir(topics_dir)):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(topics_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Merge DSA lists
                for key in ("easy", "medium", "hard"):
                    if key in data:
                        merged[key].extend(data[key])
                # Merge notes sections
                for subject, content in data.get("notes", {}).items():
                    merged["notes"][subject] = content
            except Exception as e:
                print(f"⚠️ Failed to load {fpath}: {e}")
    else:
        # Legacy fallback
        with open("topics.json", "r", encoding="utf-8") as f:
            merged = json.load(f)

    return merged

topics = load_all_topics()
print(f"📚 Loaded topics: {len(topics.get('easy', []))} easy, "
      f"{len(topics.get('medium', []))} medium, "
      f"{len(topics.get('hard', []))} hard, "
      f"{len(topics.get('notes', {}))} note subjects")

# ─── Helpers ──────────────────────────────────────────────────────────────────

def flatten_to_strings(value: Any) -> List[str]:
    """Recursively flatten nested topics.json structures to a list of strings."""
    out = []
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


def read_frontmatter(path: str) -> dict:
    """Parse YAML frontmatter from an existing markdown file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n", content)
        if not m:
            return {}
        meta = {}
        for line in m.group(1).split("\n"):
            idx = line.find(":")
            if idx == -1:
                continue
            k = line[:idx].strip()
            v = line[idx+1:].strip().strip('"\'')
            if k:
                meta[k] = v
        return meta
    except Exception:
        return {}


def build_frontmatter(title: str, topic: str, tags: List[str], update_count: int) -> str:
    tag_str = ", ".join(tags)
    banner = f"https://image.pollinations.ai/prompt/{topic.replace(' ', '%20')}%20programming?width=800&height=400&nologo=true"
    return f"""---
title: "{title}"
topic: "{topic}"
tags: "{tag_str}"
banner: "{banner}"
update_count: {update_count}
---
"""

# ─── Groq API call with retry ─────────────────────────────────────────────────

def call_groq(system: str, user: str, max_tokens: int = 4096, retries: int = 3) -> str:
    """Call Groq API with exponential backoff on rate limit errors."""
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
                wait = 2 ** attempt * 10   # 20s, 40s, 80s
                print(f"⏳ Rate limited. Waiting {wait}s before retry {attempt}/{retries}...")
                time.sleep(wait)
            else:
                print(f"❌ Groq API error (attempt {attempt}): {e}")
                if attempt == retries:
                    return f"⚠️ Content generation failed after {retries} attempts: {e}"
                time.sleep(5)
    return "⚠️ Content generation failed."

# ─── System prompts ───────────────────────────────────────────────────────────

NOTE_SYSTEM = """You are an expert technical writer creating premium study notes for software engineers.

STRICT FORMATTING RULES — follow exactly:
1. Use proper Markdown headings (## for sections, ### for subsections)
2. Every code example MUST use a fenced code block with the correct language tag
   e.g. ```java, ```javascript, ```typescript, ```python, ```go, ```bash, ```sql, ```yaml
3. Add a context-aware banner image: ![Topic](https://image.pollinations.ai/prompt/{url_encoded_topic}%20programming?width=800&height=400&nologo=true)
4. Use blockquotes for important notes: > **Note:** ...
5. Use tables where comparisons are needed (e.g. comparing approaches, complexity)
6. Include at least 3 practical, real-world code examples
7. Use Mermaid diagrams (```mermaid) for architecture, flow, or sequence diagrams where helpful
8. Do NOT include YAML frontmatter — that is added separately
9. Do NOT add any preamble like "Here are the notes:" — start directly with the content
10. Structure: Introduction → Core Concepts → Code Examples → Real-world Use Cases → Common Pitfalls → Summary
11. Aim for depth: cover both beginner understanding AND advanced nuances
"""

UPDATE_SYSTEM = """You are an expert technical writer updating an existing study article.

RULES:
1. Do NOT rewrite the existing content — only APPEND a new section at the end
2. The new section must cover a distinct sub-topic, advanced pattern, or real-world use case not already covered
3. Use the same Markdown formatting as the existing article
4. Add at least one new code example with proper language tag
5. Start your response with a new ## heading
6. Do NOT include YAML frontmatter
"""

DSA_SYSTEM = """You are an expert competitive programmer. Provide clean, well-commented Java solutions.

RULES:
1. Output ONLY raw Java code — no markdown fences, no explanation
2. Class name must be CamelCase derived from the problem name
3. Include the problem name and difficulty as a comment at the top
4. Include time and space complexity as comments
5. The solution must be complete and compilable
"""

# ─── Pickers ──────────────────────────────────────────────────────────────────

def pick_new_file(candidates: Iterable[Any], format_path):
    flat = [str(c).strip() for c in flatten_to_strings(candidates) if str(c).strip()]
    if not flat:
        return None, None
    random.shuffle(flat)
    for candidate in flat:
        path = format_path(candidate)
        if not os.path.exists(path):
            return candidate, path
    return None, None


def pick_updatable_file(candidates: Iterable[Any], format_path):
    """Pick an existing file with update_count < MAX_UPDATES."""
    flat = [str(c).strip() for c in flatten_to_strings(candidates) if str(c).strip()]
    random.shuffle(flat)
    for candidate in flat:
        path = format_path(candidate)
        if os.path.exists(path):
            meta = read_frontmatter(path)
            count = int(meta.get("update_count", 0))
            if count < MAX_UPDATES:
                return candidate, path, count
    return None, None, 0


def pick_dsa():
    difficulty = random.choice(["easy", "medium", "hard"])
    candidates = topics.get(difficulty, [])
    question, path = pick_new_file(
        candidates,
        lambda q: f"docs/dsa/{difficulty}/{sanitize_filename(q)}.md"
    )
    return (question, path), difficulty


def pick_note():
    notes_root = topics.get("notes", {})
    if not notes_root:
        return None, None, None
    section = random.choice(list(notes_root.keys()))
    candidates = notes_root.get(section, [])
    note, path = pick_new_file(
        candidates,
        lambda n: f"docs/notes/{section}/{sanitize_filename(n)}.md"
    )
    return note, path, section


def pick_note_to_update():
    notes_root = topics.get("notes", {})
    if not notes_root:
        return None, None, None, 0
    sections = list(notes_root.keys())
    random.shuffle(sections)
    for section in sections:
        candidates = notes_root.get(section, [])
        note, path, count = pick_updatable_file(
            candidates,
            lambda n, s=section: f"docs/notes/{s}/{sanitize_filename(n)}.md"
        )
        if note:
            return note, path, section, count
    return None, None, None, 0

# ─── File + Git ───────────────────────────────────────────────────────────────

def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Written: {path} ({len(content)} chars)")


def commit_and_push(message: str):
    repo = git.Repo(".")
    repo.git.add(A=True)
    if repo.is_dirty(untracked_files=True):
        repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
        repo.remote(name="origin").push()
        print(f"✅ Pushed: {message}")
    else:
        print("ℹ️ Nothing to commit.")

# ─── Tasks ────────────────────────────────────────────────────────────────────

def add_dsa():
    result, difficulty = pick_dsa()
    question, md_path = result
    if not question:
        print("⚠️ No new DSA question to add.")
        return False

    print(f"🔧 Generating DSA: {question} ({difficulty})")

    # Java solution
    java_code = call_groq(
        DSA_SYSTEM,
        f"Problem: {question}\nDifficulty: {difficulty}\nWrite the complete Java solution.",
        max_tokens=2048
    )
    java_code = re.sub(r"```java\s*|```\s*", "", java_code).strip()

    # Summary
    summary = call_groq(
        "You are a technical writer. Write a concise algorithm summary.",
        f"Problem: {question}\nJava solution:\n{java_code}\n\nWrite:\n## Approach\n...\n\n## Complexity\n- Time: O(...)\n- Space: O(...)",
        max_tokens=512
    )

    # Save Java file
    java_path = md_path.replace(".md", ".java")
    save_file(java_path, java_code)

    # Save Markdown
    banner_topic = question.replace(" ", "%20")
    md_content = f"""---
title: "{question}"
difficulty: "{difficulty}"
tags: "dsa, {difficulty}, java"
banner: "https://image.pollinations.ai/prompt/{banner_topic}%20algorithm?width=800&height=400&nologo=true"
update_count: 0
---

# {question}

![{question}](https://image.pollinations.ai/prompt/{banner_topic}%20algorithm?width=800&height=400&nologo=true)

{summary}

## Java Solution

```java
{java_code}
```
"""
    save_file(md_path, md_content)
    commit_and_push(f"📘 DSA: {question} ({difficulty})")
    return True


def add_note():
    note, path, section = pick_note()
    if not note:
        # Try updating an existing one instead
        return update_note()

    print(f"📝 Generating note: {note} [{section}]")
    url_topic = note.replace(" ", "%20")

    content_body = call_groq(
        NOTE_SYSTEM,
        f"Write comprehensive study notes for: **{note}**\nContext: This is part of the {section} learning path.",
        max_tokens=4096
    )

    tags = [section, note.split(":")[0].strip().lower().replace(" ", "-")]
    frontmatter = build_frontmatter(note, note, tags, update_count=0)
    full_content = frontmatter + "\n" + content_body

    save_file(path, full_content)
    commit_and_push(f"📝 Note: {note}")
    return True


def update_note():
    note, path, section, current_count = pick_note_to_update()
    if not note:
        print("⚠️ No notes available to update.")
        return False

    print(f"🔄 Updating note: {note} (update #{current_count + 1})")

    with open(path, "r", encoding="utf-8") as f:
        existing = f.read()

    # Strip frontmatter for the prompt
    body = re.sub(r"^---\r?\n[\s\S]*?\r?\n---\r?\n", "", existing).strip()

    new_section = call_groq(
        UPDATE_SYSTEM,
        f"Existing article about '{note}':\n\n{body[:3000]}\n\nAppend a new advanced section.",
        max_tokens=2048
    )

    new_count = current_count + 1

    # Rebuild frontmatter with updated count
    meta = read_frontmatter(path)
    tags_raw = meta.get("tags", section)
    tags = [t.strip() for t in tags_raw.split(",")]
    new_frontmatter = build_frontmatter(note, meta.get("topic", note), tags, new_count)

    updated = new_frontmatter + "\n" + body + "\n\n" + new_section

    save_file(path, updated)
    commit_and_push(f"🔄 Updated note: {note} (v{new_count})")
    return True

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").lower()
    run_count_env = os.environ.get("RUN_COUNT", "1")

    try:
        run_count = int(run_count_env)
    except Exception:
        run_count = 1

    # Only allow multiple runs on manual dispatch
    if event_name != "workflow_dispatch":
        run_count = 1

    # Scheduled runs: random delay up to 2 hours to spread load
    if event_name == "schedule":
        delay = random.randint(0, 7200)
        print(f"⏱️ Scheduled run. Sleeping {delay}s...")
        time.sleep(delay)
    else:
        print(f"▶️ Running immediately ({event_name or 'local'})")

    for i in range(run_count):
        print(f"\n─── Iteration {i+1}/{run_count} ───")
        # 50/50 chance: add DSA or add/update note
        if random.random() < 0.5:
            add_dsa()
        else:
            add_note()
        # Small pause between iterations to respect rate limits
        if i < run_count - 1:
            time.sleep(3)

    print("\n✅ Done.")


if __name__ == "__main__":
    main()
