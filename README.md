<div align="center">
  <a href="https://github.com/baaghinitesh/dailly-notes/actions/workflows/auto.yml">
    <img src="https://github.com/baaghinitesh/dailly-notes/actions/workflows/auto.yml/badge.svg" alt="Generate Content"/>
  </a>
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/github/license/baaghinitesh/dailly-notes" alt="License" />
</div>

# dailly-notes

Automated content engine that generates in-depth tech articles daily using Groq's Llama 3.3 70B model.

**Articles are published at:**

## 👉 [www.launchyourconcept.com/articles](https://www.launchyourconcept.com/articles)

---

## How it works

1. GitHub Actions runs 3× daily (6am, 12pm, 6pm UTC)
2. `main.py` picks a random topic from `topics/` JSON files
3. Generates rich Markdown content via Groq API
4. Commits the new article to `docs/notes/<subject>/`
5. `launchyourconcept.com` fetches and renders the articles directly from GitHub raw

## Topics

React · React Native · Node.js · Java · Python · TypeScript · Go · Rust · Kotlin · Swift · C++ · DSA · System Design · Databases · DevOps · Cloud AWS · Web Fundamentals · Software Engineering · Data Engineering · Mobile Development · Languages Overview

## Structure

```
docs/
  notes/<subject>/<Article_Title>.md   ← generated articles
  dsa/<difficulty>/<Problem_Name>.md   ← DSA solutions
topics/
  react_and_frontend.json
  backend_and_databases.json
  system_design.json
  ... (one file per topic group)
main.py          ← content generation script
```

## Setup (fork this repo)

1. Add `GROQ_API_KEY` to your repo's **Settings → Secrets → Actions**
2. The workflow runs automatically — or trigger manually from the Actions tab
