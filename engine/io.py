import os
import json
import git
import time
import random
from typing import List
from engine.config import AUTHOR_NAME, AUTHOR_EMAIL, _written_this_run
from engine.utils import scan_existing_files

def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    norm = path.replace("\\", "/")
    _written_this_run.add(norm)
    # We don't have easy access to _existing_on_disk from here without a global or import
    # but we can call scan_existing_files() if needed, or just let it be.
    # Actually, it's better to keep _existing_on_disk updated.
    from engine.utils import _existing_on_disk
    _existing_on_disk.add(norm)
    print(f"📄 Written: {path} ({len(content):,} chars)")


def cleanup_files(paths: List[str]):
    """Remove files written during a failed generation and clean up empty dirs."""
    from engine.utils import _existing_on_disk
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

def generate_manifest():
    """Outputs all existing .md files into articles_manifest.json."""
    existing = scan_existing_files()
    try:
        with open("articles_manifest.json", "w", encoding="utf-8") as f:
            json.dump(sorted(list(existing)), f, indent=2)
        print(f"✅ Generated articles_manifest.json with {len(existing)} articles.")
    except Exception as e:
        print(f"⚠️  Could not write articles_manifest.json: {e}")

def commit_and_push(message: str, retries: int = 3) -> bool:
    generate_manifest()
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
