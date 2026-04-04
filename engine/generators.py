import re
import random
from typing import Optional
from engine.config import (
    LANGS, GroqQuotaError, GroqAuthError, GroqAPIError
)
from engine.utils import (
    picsum_seed, fix_mermaid_syntax, read_frontmatter, build_frontmatter
)
from engine.topics import (
    _all_notes_exhausted, expand_note_topics, pick_new_note_from_file,
    pick_note_to_update, pick_topic_file_with_new_blogs, _all_blogs_exhausted,
    pick_blog_from_file
)
from engine.api import call_groq
from engine.validation import validate_dsa_content, validate_note_content
from engine.io import save_file
from engine.prompts import (
    DSA_SYSTEM, DSA_SUMMARY_SYSTEM, NOTE_SYSTEM, UPDATE_SYSTEM, BLOG_GENERATION_SYSTEM
)

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
    # Difficulty-aware token budget: complex problems need more tokens
    _summary_tokens = {"easy": 1500, "medium": 2000, "hard": 2500, "super_advanced": 3000}
    summary_max_tokens = _summary_tokens.get(difficulty, 2000)

    try:
        summary = call_groq(
            DSA_SUMMARY_SYSTEM,
            (
                f"Problem: {question}\n"
                f"Language: {lang}\n"
                f"Difficulty: {difficulty}\n"
                f"Solution code:\n```{lang_tag}\n{code}\n```"
            ),
            max_tokens=summary_max_tokens,
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
    except Exception as e:
        print(f"❌ DSA content validation failed for '{question}': {e}")
        return None

    # ── Step 4: Write file ───────────────────────────────────────────────────
    seed = picsum_seed(lang + question)
    banner_url = f"https://picsum.photos/seed/{seed}/1200/630"
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
        f'{summary}\n\n'
        f'## {lang.upper() if lang in ("cpp", "c") else lang.capitalize()} Solution\n\n'
        f'```{lang_tag}\n{code}\n```\n'
    )

    md_content = fix_mermaid_syntax(md_content)
    save_file(md_path, md_content)
    print(f"✅ DSA article written: {md_path}")
    return f"DSA Study [{lang}/{difficulty}]: {question}"


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

    seed = picsum_seed(section + note)
    banner_url = f"https://picsum.photos/seed/{seed}/1200/630"

    # ── Step 1: Generate content ─────────────────────────────────────────────
    try:
        content_body = call_groq(
            NOTE_SYSTEM,
            (
                f"Topic: **{note}**\n"
                f"Learning path: **{section}**"
                + (f" → **{section_key}**" if section_key else "")
                + "\n\n"
                f"MANDATORY CHECKLIST — your response will be rejected if any item is missing:\n"
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
    except Exception as e:
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
    final_content = fix_mermaid_syntax(frontmatter + "\n" + content_body)
    save_file(path, final_content)
    print(f"✅ Note article written: {path}")
    return f"Study Note [{label}]: {note}"


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

    try:
        with open(path, "r", encoding="utf-8") as f:
            existing = f.read()

        body = re.sub(r"^---\r?\n[\s\S]*?\r?\n---\r?\n", "", existing).strip()

        # ── Step 1: Generate new section ────────────────────────────────────────
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
        final_content = fix_mermaid_syntax(new_frontmatter + "\n" + body + "\n\n" + new_section_text)
        save_file(path, final_content)
        print(f"✅ Note updated: {path}")
        return f"Update [{label}]: {note} (revised)"
    except Exception as e:
        print(f"❌ Failed to write updated note '{note}': {e}")
        return None

def generate_blog() -> Optional[str]:
    """
    Generate one professional blog post.
    Flow: pick file → pick blog topic → call Groq (full article) → validate → write file
    """
    tf = pick_topic_file_with_new_blogs()
    if not tf:
        if _all_blogs_exhausted():
            print("🧠 All blog topics exhausted — skipping blog generation.")
            return None
        else:
            print("⚠️  No blog file with available topics found.")
            return None

    blog_data, md_path = pick_blog_from_file(tf)
    if not blog_data:
        print("⚠️  No available blog in selected file.")
        return None

    topic = blog_data.get("topic")
    category = blog_data.get("category", "Technology")
    tags = blog_data.get("tags", "blog, tech, business")
    difficulty = blog_data.get("difficulty", "Intermediate")

    print(f"✍️  Generating Blog [{category}] from [{tf['filename']}]: {topic}")

    # ── Step 1: Generate full article ─────────────────────────────────────────
    try:
        content_body = call_groq(
            BLOG_GENERATION_SYSTEM,
            (
                f"Topic: {topic}\n"
                f"Category: {category}\n"
                f"Tags: {tags}\n"
                f"Difficulty: {difficulty}\n"
                f"Full Article Content Instructions: Provide a deep, insightful, and professional blog post."
            ),
            max_tokens=4096,
            context=f"Blog: {topic}",
        )
    except (GroqQuotaError, GroqAuthError):
        raise
    except GroqAPIError as e:
        print(f"❌ Blog generation failed for '{topic}': {e}")
        return None

    # ── Step 2: Validate content ─────────────────────────────────────────────
    # Standard blog validation (length + structure)
    if not content_body or len(content_body.strip()) < 1000:
        print(f"⚠️  Blog content too short for '{topic}' — skipping")
        return None

    # ── Step 3: Write file ───────────────────────────────────────────────────
    final_content = fix_mermaid_syntax(content_body)
    
    # Ensure source: github is in the frontmatter if AI missed it
    if "source: github" not in final_content:
        # Simple injection if frontmatter exists
        final_content = re.sub(r"---(\r?\n)", r"--- \1source: github\1", final_content, count=1)

    save_file(md_path, final_content)
    print(f"✅ Blog article written: {md_path}")
    return f"Blog Post [{category}]: {topic}"
