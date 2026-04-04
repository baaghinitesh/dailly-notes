import os
import re

def audit_mermaid():
    docs_dir = "docs/notes"
    issue_count = 0
    total_files = 0
    total_diagrams = 0
    
    # Patterns that typically break Mermaid rendering
    # 1. Trailing arrow in edge labels: -->|Text|> 
    trailing_arrow = re.compile(r'(-+>|=+>|-+\.-+>)\|([^|]+)\|\s*>')
    
    # problematic characters that usually require quoting
    # NOTE: we only match if there is NO quote yet
    node_brackets = re.compile(r'([A-Za-z0-9_-]+)\[([^"\]]*[\(\)\{\}\[\]\?\/\>][^"\]]*)\]')
    node_braces   = re.compile(r'([A-Za-z0-9_-]+)\{([^"\}]*[\(\)\{\}\[\]\?\/\>][^"\}]*)\}')
    # For (round) nodes, we ONLY flag if there is an extra / ? [ ] { } > \ or another paren inside it
    node_parens   = re.compile(r'([A-Za-z0-9_-]+)\(([^"\)]*[\[\]\{\}\?\/\>\\][^"\)]*)\)')

    print(f"🔍 Starting systematic audit of Mermaid diagrams in {docs_dir}...")
    
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                total_files += 1
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Extract mermaid blocks
                mermaid_blocks = re.findall(r'```mermaid\s+([\s\S]*?)```', content)
                if not mermaid_blocks:
                    continue
                
                total_diagrams += len(mermaid_blocks)
                file_has_issue = False
                
                for i, block in enumerate(mermaid_blocks):
                    found_in_block = False
                    for line in block.split('\n'):
                        issues = []
                        if trailing_arrow.search(line):
                            issues.append("Trailing arrow (-->|T|>)")
                        if node_brackets.search(line):
                            issues.append("Unquoted special chars in []")
                        if node_braces.search(line):
                            issues.append("Unquoted special chars in {}")
                        if node_parens.search(line):
                            issues.append("Unquoted special chars in ()")

                        if issues:
                            if not file_has_issue:
                                print(f"\n📄 File: {path}")
                                file_has_issue = True
                            print(f"   🚩 Line: `{line.strip()}`")
                            for issue in issues:
                                print(f"      - {issue}")
                            issue_count += 1

    print(f"\n{'─' * 50}")
    print(f"✅ Audit Complete.")
    print(f"📊 Scanned: {total_files} files | {total_diagrams} diagrams")
    print(f"🚨 Issues Found: {issue_count}")
    
    if issue_count == 0:
        print("✨ All diagrams appear to have valid, clean syntax!")

if __name__ == "__main__":
    audit_mermaid()
