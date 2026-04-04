import os
import random
import time
from engine.config import (
    GROQ_API_KEY, _quota_exhausted, _written_this_run
)
from engine.utils import scan_existing_files
from engine.topics import load_topic_files
from engine.generators import generate_dsa, generate_note, generate_blog
from engine.io import commit_and_push

def main():
    if not GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY environment variable is not set.")
        return

    print("🚀 Dailly Notes Production Engine (Modular Version)")
    print("--------------------------------------------------")

    # 1. Initialize environment
    scan_existing_files()
    load_topic_files()

    # 2. Daily Quota: 4 Resources (Notes/DSA) and 2 Blog Posts
    target_resources = 4
    target_blogs = 2
    
    generated_resources = 0
    generated_blogs = 0
    total_generated = 0
    
    history = []

    # 3. Generate Resources
    print(f"\n--- Generating {target_resources} Study Resources ---")
    while generated_resources < target_resources and not _quota_exhausted:
        # 40% DSA, 60% Conceptual Notes
        if random.random() < 0.4:
            res = generate_dsa()
        else:
            res = generate_note()
            
        if res:
            history.append(res)
            generated_resources += 1
            total_generated += 1
            # Add a small delay between articles
            time.sleep(2)
        else:
            # If both return None, we might be truly exhausted or hit an error
            break

    # 4. Generate Blogs
    print(f"\n--- Generating {target_blogs} Professional Blog Posts ---")
    while generated_blogs < target_blogs and not _quota_exhausted:
        res = generate_blog()
        if res:
            history.append(res)
            generated_blogs += 1
            total_generated += 1
            time.sleep(2)
        else:
            break

    # 5. Finalize
    print("\n--------------------------------------------------")
    if total_generated > 0:
        print(f"✅ Success! Generated {total_generated} articles:")
        for item in history:
            print(f"  - {item}")
        
        # Deploy
        msg = f"Auto-content: {total_generated} new articles (Resources: {generated_resources}, Blogs: {generated_blogs})"
        if commit_and_push(msg):
            # 6. Sync with website (Shadow entries)
            print("\n🔄 Triggering website synchronization...")
            try:
                # Assuming relative path or absolute path to launchyourconcept
                # We use node to run the sync script
                import subprocess
                sync_script = "../../launchyourconcept/server/scripts/syncBlogs.js"
                if os.path.exists(sync_script):
                    subprocess.run(["node", "scripts/syncBlogs.js"], cwd="../../launchyourconcept/server", check=True)
                    print("✨ Website synchronization complete!")
                else:
                    # Try another path if not found (e.g. in workspace root)
                    sync_script_alt = "../launchyourconcept/server/scripts/syncBlogs.js"
                    if os.path.exists(sync_script_alt):
                        subprocess.run(["node", "scripts/syncBlogs.js"], cwd="../launchyourconcept/server", check=True)
                        print("✨ Website synchronization complete!")
            except Exception as e:
                print(f"⚠️  Website sync failed: {e}")
    else:
        print("ℹ️  No new articles were generated today.")

    if _quota_exhausted:
        print("⚠️  Stop triggered: Groq API quota reached.")

if __name__ == "__main__":
    main()
