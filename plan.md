# Content Engine Plan — dailly-notes × launchyourconcept

## Architecture Overview

A self-sustaining AI content engine:
- **dailly-notes** (GitHub repo) — Python script generates Markdown articles via Groq/Llama-3, commits to GitHub, deploys to MkDocs Pages
- **launchyourconcept** (React frontend) — fetches raw Markdown from GitHub, renders it with react-markdown + syntax highlighting + Mermaid diagrams

---

## ✅ DONE

### Infrastructure
- [x] Groq/Llama-3 70B replaces Gemini — blazing fast inference, ideal for GitHub Actions
- [x] `main.py` — full content engine with rich prompts, frontmatter, banner images, Mermaid, callouts, tables
- [x] `auto.yml` — 3 scheduled runs/day (6am, 12pm, 6pm UTC), generates 3 articles per run = ~9 articles/day
- [x] `concurrency` guard in workflow — prevents git push conflicts between runs
- [x] `git pull --rebase` before generate step — avoids stale branch conflicts
- [x] `mkdocs.yml` — Material theme, dark mode, Mermaid superfences, Inter/JetBrains Mono fonts, awesome-pages
- [x] `requirements.txt` — groq, gitpython, mkdocs-material, pymdown-extensions, mkdocs-awesome-pages-plugin

### Topics Coverage (16 JSON files)
- [x] `dsa.json` — 90+ easy, 100+ medium, 80+ hard LeetCode problems + 12 DSA concept sections
- [x] `web_fundamentals.json` — HTML, CSS (fundamentals + layout + advanced), JS (fundamentals + core + async + DOM + advanced), browser performance, web security, SEO/a11y
- [x] `react_and_frontend.json` — React (11 sections), React Native (7 sections), frontend-tooling
- [x] `backend_and_databases.json` — Node.js, Express, REST, Auth, Redis, PostgreSQL, MongoDB, ORMs, DB design, Python web frameworks
- [x] `system_design.json` — fundamentals, networking, caching, databases at scale, message queues, microservices, storage, design patterns, 20 classic problems, cloud/devops
- [x] `devops_and_cloud.json` — Linux/shell, Git, Docker, Kubernetes, CI/CD, monitoring, IaC, AWS core/databases/serverless/containers
- [x] `software_engineering.json` — design patterns, architecture, API design, testing, code quality, security engineering, data engineering, mobile development
- [x] `lang_overview.json` — language comparison, learning roadmaps, feature comparison, polyglot programming, emerging languages
- [x] `lang_java.json` — Java basics → OOP → collections → generics/streams → concurrency → Spring Boot → modern features → ecosystem (with 0_Overview: benefits, drawbacks, when to use)
- [x] `lang_typescript.json` — type system → interfaces/classes → generics → utility types → advanced patterns → config/tooling → framework integrations
- [x] `lang_python.json` — basics → OOP → advanced → web frameworks → data science → ecosystem
- [x] `lang_golang.json` — basics → data structures → functions/interfaces → concurrency → stdlib → web dev → database/testing → tooling
- [x] `lang_rust.json` — ownership/borrowing → types/pattern matching → traits/generics → smart pointers → error handling → iterators/closures → async → systems/unsafe → ecosystem
- [x] `lang_cpp.json` — fundamentals → OOP → modern C++11-23 → templates/metaprogramming → STL → memory management → build/tooling
- [x] `lang_kotlin.json` — basics → functions/OOP → collections/functional → coroutines → Android → Jetpack Compose → KMP → server-side
- [x] `lang_swift.json` — basics → collections → functions/closures → OOP/protocols → memory/error handling → Swift concurrency → iOS/SwiftUI → ecosystem

### Frontend (launchyourconcept)
- [x] `useArticleTopics.ts` — fetches all 16 topic files in parallel, merges notes sections, builds TopicGroup tree
- [x] `ArticlesIndex.tsx` — grid of topic cards with search, distinct icons + colors per language/subject
- [x] `ArticlesSidebar.tsx` — sticky desktop sidebar + mobile drawer, per-topic icons/colors for all subjects
- [x] `ArticlePage.tsx` — full article reader with:
  - Dark/light syntax highlighting (oneDark/oneLight via react-syntax-highlighter)
  - **Mermaid diagram rendering** (lazy-loaded, neutral theme, error fallback)
  - Pollinations.ai banner images with gradient fallback per topic
  - TOC with IntersectionObserver active tracking
  - Copy-to-clipboard on code blocks
  - Read time, update count, tags meta row
  - Breadcrumb navigation (desktop + mobile)
- [x] Routes: `/articles` and `/articles/:topic/:slug`
- [x] Links in navbar, company dropdown, mobile sidebar

### Content Quality (Prompt Engineering)
- [x] Rich NOTE_SYSTEM prompt enforces: banner image, Mermaid diagrams, callouts (Note/Warning/Tip), comparison tables, 3+ code examples, 600-1200 words
- [x] UPDATE_SYSTEM appends new sections without rewriting existing content
- [x] DSA_SYSTEM generates compilable Java with complexity analysis
- [x] Exponential backoff on Groq rate limits (20s, 40s, 80s)
- [x] 40% DSA / 60% notes weighting per run

---

## 🔄 IN PROGRESS / NEEDS VERIFICATION

- [ ] Verify Mermaid renders correctly in production build (test with a real article that has ```mermaid blocks)
- [ ] Verify Pollinations.ai banner images load (they can be slow/unreliable — gradient fallback handles it)
- [ ] First real articles need to be generated and pushed to confirm full pipeline works end-to-end

---

## ❌ PENDING / IMPROVEMENTS NEEDED

### SEO (Critical — React is CSR)
- [ ] **Server-side rendering for article pages** — Google bot sees blank page currently
  - Option A: Add `/api/article/:topic/:slug` route in Express server that fetches GitHub raw MD, converts to HTML with `marked` or `unified`, returns full HTML page with meta tags
  - Option B: Migrate to Next.js (bigger change but proper SSR/SSG built-in)
  - Option C: Prerender with `vite-plugin-ssr` or `@prerenderer/plugin-vite`
- [ ] **Dynamic meta tags per article** — title, description, og:image should reflect article content
  - Currently react-helmet-async is installed — wire it up in ArticlePage with article frontmatter data
- [ ] **Sitemap generation** — auto-generate sitemap.xml listing all article URLs
  - Can be done server-side by scanning GitHub tree API for all .md files in docs/notes/

### Content Engine
- [ ] **AI topic discovery** — when all topics in a section are exhausted, call Groq to generate 10 new topics and append to the relevant JSON file
- [ ] **Cross-linking** — articles should reference related articles (e.g., "See also: Closures in JavaScript")
- [ ] **Code quality validation** — Java solutions should be compiled/tested before commit (add `javac` step in workflow)
- [ ] **Image alt text** — Pollinations.ai images need descriptive alt text for accessibility

### Frontend
- [ ] **Language hub pages** — `/articles/golang`, `/articles/rust` etc. should show a language overview card (benefits, drawbacks, when to use) before the topic list
- [ ] **"Related articles" section** at bottom of ArticlePage — show 3 articles from the same topic
- [ ] **Progress tracking** — show user how many articles they've read per topic (localStorage)
- [ ] **Article search** — full-text search across all generated articles (not just topic names)
- [ ] **Print/PDF export** of articles

### Infrastructure
- [ ] **Workflow failure notifications** — add a step to notify (email/Slack) if generation fails
- [ ] **Article count badge** — show total article count in the navbar/hero dynamically from GitHub API
- [ ] **Rate limit handling** — if Groq is down, fall back to a queue and retry next run

---

## Architecture Diagram

```
GitHub Actions (3x/day)
    │
    ▼
main.py (Python)
    │── load topics from topics/*.json
    │── pick random topic (40% DSA, 60% notes)
    │── call Groq API (Llama-3 70B)
    │── write .md file to docs/notes/<subject>/
    │── commit + push to GitHub
    │
    ▼
mkdocs gh-deploy
    │── builds static site
    │── pushes to gh-pages branch
    │
    ▼
GitHub Pages → https://baaghinitesh.github.io/dailly-notes/

launchyourconcept.com (React)
    │── useArticleTopics.ts fetches topics/*.json from GitHub raw
    │── ArticlesIndex shows topic cards
    │── ArticlePage fetches docs/notes/<topic>/<slug>.md from GitHub raw
    │── Renders with react-markdown + Mermaid + syntax highlighting
```
