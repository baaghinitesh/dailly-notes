import os
import re
import urllib.parse

def url_encode(text: str) -> str:
    return text.strip().replace(" ", "%20").replace(":", "").replace("/", "")

def process_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    title_match = re.search(r'^title:\s*"(.*)"', content, re.MULTILINE)
    section_match = re.search(r'^section:\s*"(.*)"', content, re.MULTILINE)
    
    if not title_match or not section_match:
        return

    title = title_match.group(1)
    section = section_match.group(1)
    
    prompt = url_encode(f"{section} {title} programming abstract")
    new_banner = f"https://image.pollinations.ai/prompt/{prompt}?width=1200&height=630&nologo=true"
    
    old_banner_match = re.search(r'^banner:\s*"(https://picsum\.photos(?:.*)?)"', content, re.MULTILINE)
    if not old_banner_match:
        return
        
    old_banner_url = old_banner_match.group(1)
    
    # Replace frontmatter
    new_content = content.replace(f'banner: "{old_banner_url}"', f'banner: "{new_banner}"')
    
    # Replace markdown embedded image body 
    # Usually formatted as ![alt](old_banner_url)
    new_content = new_content.replace(f']({old_banner_url})', f']({new_banner})')
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {path}")

def main():
    directory = 'd:/projects/dailly-notes/docs/notes'
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
