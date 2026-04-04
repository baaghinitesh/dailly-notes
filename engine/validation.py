import re
from engine.config import MIN_NOTE_CHARS, MIN_NOTE_WORDS, MIN_CODE_BLOCKS, MIN_DSA_CHARS, ContentValidationError

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
