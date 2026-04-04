import os
import re

def fix_mermaid_syntax(content: str) -> str:
    """
    Post-processing to fix common Mermaid syntax errors made by AI.
    - Fixes trailing arrows in labels like -->|Text|>
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

        # 3. Quote node labels containing special characters (brackets, slashes, etc)
        def _quote_node(m):
            node_id, opener, text, closer = m.groups()
            if any(c in text for c in "()[]{}?/>") and not (text.startswith('"') and text.endswith('"')):
                return f'{node_id}{opener}"{text}"{closer}'
            return m.group(0)

        # Node patterns: id[Text], id{Text}, id(Text)
        block = re.sub(r'([A-Za-z0-9_-]+)(\[)([^"\]][^\]]*)(\])', _quote_node, block)
        block = re.sub(r'([A-Za-z0-9_-]+)(\{)([^"\}][^\}]*)(\})', _quote_node, block)
        block = re.sub(r'([A-Za-z0-9_-]+)(\()([^"\)][^\)]*)(\))', _quote_node, block)

        # 4. Clean non-breaking spaces and zero-width spaces
        block = block.replace('\u00A0', ' ').replace('\u200B', '')

        return f'```mermaid\n{block}```'

    return re.sub(r'```mermaid\s+([\s\S]*?)```', _fix_block, content)

def main():
    docs_dir = "docs/notes"
    count = 0
    fixed = 0
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                count += 1
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = fix_mermaid_syntax(content)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    fixed += 1
                    if fixed % 10 == 0:
                        print(f"  Processed {fixed} files...")

    print(f"✅ Scanning complete. Scanned {count} files, fixed {fixed} files.")

if __name__ == "__main__":
    main()
