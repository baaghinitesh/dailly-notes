import os
import re
from typing import Any, List, Optional
from engine.config import MAX_UPDATES, _written_this_run

# ─── Disk scan ────────────────────────────────────────────────────────────────

_existing_on_disk: set = set()

def scan_existing_files() -> set:
    """
    Walk docs/notes/ at startup and collect all existing .md paths.
    Prevents regenerating articles that already exist on disk.
    """
    global _existing_on_disk
    existing = set()
    notes_root = "docs"
    if not os.path.isdir(notes_root):
        return existing
    for dirpath, _, filenames in os.walk(notes_root):
        for fname in filenames:
            if fname.endswith(".md"):
                full = os.path.join(dirpath, fname).replace("\\", "/")
                existing.add(full)
    print(f"🗂️  Found {len(existing)} existing articles on disk (notes + blogs)")
    _existing_on_disk = existing
    return existing

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


def picsum_seed(text: str) -> int:
    """Deterministic seed from string — matches JS strToSeed in ArticlePage.tsx."""
    h = 0
    for ch in text:
        h = (31 * h + ord(ch)) & 0xFFFFFFFF
    # Match JS: (Math.imul(31, h) + charCode) | 0 → signed 32-bit, then abs % 1000
    if h >= 0x80000000:
        h -= 0x100000000
    return abs(h) % 1000


def build_frontmatter(
    title: str, topic: str, section: str, tags: List[str], update_count: int
) -> str:
    tag_str = ", ".join(tags)
    prompt = url_encode(f"{section} {title} programming abstract")
    banner = f"https://image.pollinations.ai/prompt/{prompt}?width=1200&height=630&nologo=true"
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


def fix_mermaid_syntax(content: str) -> str:
    """
    Post-processing to fix common Mermaid syntax errors made by AI.
    - Fixes trailing arrows in labels like -->|Text|
    - Converts LR to TD for large graphs
    - Quotes node labels containing special characters
    - Cleans up non-breaking spaces
    """

    def _fix_block(match):
        block = match.group(1)

        # 1. Fix Bad Edge Label Syntax: -->|Text|> to -->|Text|
        # Also handles -.->|Text|> and ==>|Text|>
        block = re.sub(r'(-+>|=+>|-+\.-+>)\|([^|]+)\|\s*>', r'\1|\2|', block)

        # 2. Convert LR to TD if graph has many edges (better mobile layout)
        if re.search(r'(graph|flowchart)\s+LR', block):
            edges = re.findall(r'-->|-.->|==>', block)
            if len(edges) >= 4:
                block = re.sub(r'(graph|flowchart)\s+LR', r'\1 TD', block)

        # 3. Aggressive Node Label Quoting
        def _quote_label(m):
            prefix, opener, label, closer = m.groups()
            if not (label.startswith('"') and label.endswith('"')) and any(c in label for c in "()[]{}?/\\>!@#$%^&*+-=:;.,"):
                safe_label = label.replace('"', '\\"')
                return f'{prefix}{opener}"{safe_label}"{closer}'
            return m.group(0)

        # Shape patterns: [ ], { }, (( )), ([ ]), [[ ]], {{ }}, [/ /], [\ \], ( )
        shapes = [
            (r'([A-Za-z0-9_-]+)(\[)', r'(\])'),
            (r'([A-Za-z0-9_-]+)(\{)', r'(\})'),
            (r'([A-Za-z0-9_-]+)(\(\()', r'(\)\))'),
            (r'([A-Za-z0-9_-]+)(\(\[)', r'(\]\))'),
            (r'([A-Za-z0-9_-]+)(\[\[)', r'(\]\])'),
            (r'([A-Za-z0-9_-]+)(\{\{)', r'(\}\})'),
            (r'([A-Za-z0-9_-]+)(\[\/)', r'(\/\])'),
            (r'([A-Za-z0-9_-]+)(\[\\)', r'(\\\])'),
            (r'([A-Za-z0-9_-]+)(\()', r'(\))'),
        ]
        
        for opener_pat, closer_pat in shapes:
            full_pat = opener_pat + r'([\s\S]*?)' + closer_pat
            block = re.sub(full_pat, _quote_label, block)

        # 4. Clean non-breaking spaces and zero-width spaces
        block = block.replace('\u00A0', ' ').replace('\u200B', '')

        return f'```mermaid\n{block}```'

    return re.sub(r'```mermaid\s+([\s\S]*?)```', _fix_block, content)
