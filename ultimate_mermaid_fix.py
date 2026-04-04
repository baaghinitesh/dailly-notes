import os
import re

def aggressive_mermaid_fix(content: str) -> str:
    """
    Aggressively fixes Mermaid blocks to ensure all node labels are quoted if they 
    contain special characters, and handles common syntax errors.
    """
    def _fix_block(match):
        block = match.group(1)
        
        # 1. Fix Bad Edge Label Syntax: -->|Text|> to -->|Text|
        block = re.sub(r'(-+>|=+>|-+\.-+>)\|([^|]+)\|\s*>', r'\1|\2|', block)
        
        # 2. Fix Node Quotes systematically
        # We look for ID[label], ID(label), ID{label}, ID((label)), ID[[label]], ID{{label}}, ID[/label/], ID[\label\], ID[/label\], ID[\label/]
        
        def _quote_label(m):
            prefix, opener, label, closer = m.groups()
            # If label already has quotes, or is empty, or is just pure alphanumeric/space (mostly safe), 
            # but actually it's safest to just quote if it has ANY non-alphanumeric char and isn't quoted.
            if not (label.startswith('"') and label.endswith('"')) and any(c in label for c in "()[]{}?/\\>!@#$%^&*+-=:;.,"):
                # Escape existing quotes just in case
                safe_label = label.replace('"', '\\"')
                return f'{prefix}{opener}"{safe_label}"{closer}'
            return m.group(0)

        # Pattern for various node shapes:
        # (ID) ( [ { ([ [[ {{ [/ [\ [/ [\
        shapes = [
            (r'([A-Za-z0-9_-]+)(\[)', r'(\])'),        # [ ]
            (r'([A-Za-z0-9_-]+)(\{)', r'(\})'),        # { }
            (r'([A-Za-z0-9_-]+)(\(\()', r'(\)\))'),    # (( ))
            (r'([A-Za-z0-9_-]+)(\(\[)', r'(\]\))'),    # ([ ])
            (r'([A-Za-z0-9_-]+)(\[\[)', r'(\]\])'),    # [[ ]]
            (r'([A-Za-z0-9_-]+)(\{\{)', r'(\}\})'),    # {{ }}
            (r'([A-Za-z0-9_-]+)(\[\/)', r'(\/\])'),    # [/ /]
            (r'([A-Za-z0-9_-]+)(\[\\)', r'(\\\])'),    # [\ \]
            (r'([A-Za-z0-9_-]+)(\()', r'(\))'),        # ( ) - Lowest priority
        ]
        
        for opener_pat, closer_pat in shapes:
            # We match the opener, then any text that DOES NOT match a quote (to avoid double quoting) 
            # or the closer sequence, then the closer.
            # This is complex because closers can be 2 chars.
            # Simplified: match anything until closer, check if it's already quoted.
            full_pat = opener_pat + r'([\s\S]*?)' + closer_pat
            block = re.sub(full_pat, _quote_label, block)

        # 3. Clean up non-breaking spaces
        block = block.replace('\u00A0', ' ').replace('\u200B', '')
        
        return f'```mermaid\n{block}```'

    return re.sub(r'```mermaid\s+([\s\S]*?)```', _fix_block, content)

def main():
    docs_dir = "docs/notes"
    scanned = 0
    fixed = 0
    
    print(f"🚀 Starting AGGRESSIVE Mermaid fix in {docs_dir}...")
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                scanned += 1
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = aggressive_mermaid_fix(content)
                
                if new_content != content:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    fixed += 1
                    if fixed % 50 == 0:
                        print(f"  Processed {fixed} fixes...")

    print(f"\n{'─' * 50}")
    print(f"✅ Aggressive Fix Complete.")
    print(f"📊 Scanned: {scanned} files | Fixed: {fixed} files")

if __name__ == "__main__":
    main()
