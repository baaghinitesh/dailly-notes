#!/usr/bin/env python3
"""
main.py — Groq/Llama-3 powered content engine for dailly-notes
Refactored into modules under the engine/ directory.
"""

import os
import sys
import time
import random
from typing import List

from engine import config
from engine.api import preflight_check
from engine.topics import load_topic_files, LANGS, DIFFS
from engine.utils import scan_existing_files
from engine.generators import generate_dsa, generate_note
from engine.io import commit_and_push
from engine.config import GroqAuthError, GroqQuotaError

def main():
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").lower()

    try:
        run_count = int(os.environ.get("RUN_COUNT", "5"))
    except ValueError:
        run_count = 5

    # Local runs generate 1 article; CI runs use RUN_COUNT
    if event_name not in ("schedule", "workflow_dispatch"):
        run_count = 1

    # Scheduled runs: random delay to spread load across the cron window
    if event_name == "schedule":
        delay = random.randint(0, 300)
        print(f"⏱️  Scheduled run — sleeping {delay}s before starting...")
        time.sleep(delay)
    else:
        print(f"▶️  Event: {event_name or 'local'}")

    # ─── Initialize Engine ───────────────────────────────────────────────────
    print("📂 Loading topic files...")
    topic_files = load_topic_files()
    
    _all_problems_count = sum(
        len(tf["dsa_problems"][lang][diff])
        for tf in topic_files
        for lang in LANGS
        for diff in DIFFS
    )
    _all_notes_count = sum(len(tf["notes"]) for tf in topic_files)
    print(
        f"📚 Loaded {len(topic_files)} topic files | "
        f"{_all_problems_count} DSA problems | "
        f"{_all_notes_count} note subjects"
    )

    scan_existing_files()

    print(f"🎯 Generating {run_count} article(s) this run\n")

    # ── Preflight: verify API key and quota BEFORE any generation ────────────
    if not preflight_check():
        if config._quota_exhausted:
            print("⚠️  Quota exhausted — no articles generated this run.")
            # Exit 0: not a script error, just nothing to do
            sys.exit(0)
        else:
            print("❌ Preflight check failed — aborting run.")
            sys.exit(1)

    print()

    commit_messages: List[str] = []
    failed_count = 0
    quota_hit = False

    for i in range(run_count):
        print(f"\n─── Article {i + 1}/{run_count} ───")

        try:
            # 40% DSA problem solutions, 60% conceptual notes
            if random.random() < 0.40:
                msg = generate_dsa()
            else:
                msg = generate_note()

            if msg:
                commit_messages.append(msg)
            else:
                failed_count += 1

        except GroqAuthError as e:
            # Fatal — invalid key or model gone, stop everything
            print(f"❌ FATAL auth error: {e}")
            break

        except GroqQuotaError as e:
            # Quota hit mid-run — commit what we have and stop
            print(f"❌ Quota exhausted mid-run: {e}")
            print("⚠️  Stopping generation — will commit articles generated so far.")
            quota_hit = True
            break

        except Exception as e:
            # Unexpected error — log it, count as failure, continue
            print(f"❌ Unexpected error on article {i + 1}: {e}")
            failed_count += 1

        # Brief pause between articles to avoid hammering the API
        if i < run_count - 1 and not quota_hit:
            time.sleep(10)

    # ── Commit everything that succeeded ─────────────────────────────────────
    if commit_messages:
        if len(commit_messages) == 1:
            batch_msg = commit_messages[0]
        else:
            titles = "\n".join(f"  • {m}" for m in commit_messages)
            prefixes = [
                f"Add {len(commit_messages)} new study articles",
                f"Content Update: Added {len(commit_messages)} new resources",
                f"Published {len(commit_messages)} new technical notes",
                f"Update library with {len(commit_messages)} new study guides"
            ]
            batch_msg = f"{random.choice(prefixes)}\n\n{titles}"

        success = commit_and_push(batch_msg)
        if not success:
            print("⚠️  Batch push failed — attempting per-article fallback commits...")
            for msg in commit_messages:
                commit_and_push(msg)
    else:
        print("⚠️  No articles were generated this run.")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_attempted = len(commit_messages) + failed_count
    print(f"\n{'─' * 50}")
    print(f"✅ Done. {len(commit_messages)}/{total_attempted} articles generated successfully.")
    if failed_count > 0:
        print(f"⚠️  {failed_count} article(s) failed (see logs above for reasons).")
    if quota_hit:
        print("⚠️  Run stopped early due to quota exhaustion.")

    # Exit 1 only if EVERY article failed (marks GH Actions run red)
    if failed_count > 0 and len(commit_messages) == 0:
        print("❌ All articles failed. Exiting with error.")
        sys.exit(1)


if __name__ == "__main__":
    main()
