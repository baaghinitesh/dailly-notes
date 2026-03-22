# Setup & Configuration

This project automatically generates study notes and DSA solutions using Groq's Llama-3 70B model, deployed to GitHub Pages via GitHub Actions.

## Requirements

- Python 3.11+
- A [Groq API key](https://console.groq.com)
- GitHub repository with Pages enabled

## Local Setup

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
python main.py
```

## GitHub Actions Setup

Add a repository secret named `GROQ_API_KEY` with your Groq API key.

The workflow runs automatically twice daily (3am and 3pm UTC) and can also be triggered manually from the Actions tab with a custom `run_count`.

## Content Structure

- `docs/notes/{topic}/` — Study notes (React, Java, React Native, DSA)
- `docs/dsa/{easy,medium,hard}/` — LeetCode solutions in Java
- `topics.json` — Source of truth for all topics

## Extending Topics

Edit `topics.json` to add new topics. The automation will pick them up on the next run.
