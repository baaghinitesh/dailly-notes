<div align="center">
  <!-- Auto-Generate Content Badge -->
  <a href="https://github.com/baaghinitesh/dailly-notes/actions/workflows/auto.yml">
    <img src="https://github.com/baaghinitesh/dailly-notes/actions/workflows/auto.yml/badge.svg" alt="Auto-Generate Content"/>
  </a>

  <!-- Build and Deploy Site Badge -->
  <a href="https://github.com/baaghinitesh/dailly-notes/actions/workflows/deploy.yml">
    <img src="https://github.com/baaghinitesh/dailly-notes/actions/workflows/deploy.yml/badge.svg" alt="Build and Deploy Site"/>
  </a>

  <!-- License Badge -->
  <img src="https://img.shields.io/github/license/baaghinitesh/dailly-notes" alt="License" />

  <!-- Python Version Badge -->
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python Version" />
</div>


# Auto DSA & Tech Notes

An automated knowledge base that uses the **Gemini AI** to generate and publish new DSA solutions and tech notes daily to a live website, complete with CI/CD for deployment.

<p align="center">
  <a href="https://baaghinitesh.github.io/dailly-notes/"><strong>Visit the Live Site »</strong></a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <a href="https://baaghinitesh.github.io/dailly-notes/notes/"><strong>Browse the Notes »</strong></a>
</p>

---

## 1. Introduction

This project automates content creation and website deployment for a personal knowledge base. It leverages a Python script to interact with the **Google Gemini API**, generating high-quality educational content on Data Structures & Algorithms (DSA) and various tech topics. The entire workflow, from content generation to deployment on **GitHub Pages**, is managed by **GitHub Actions**, ensuring the site is always up-to-date.

**Key Goals:**

- **Automate Learning:** Consistently generate new learning material.
- **Demonstrate CI/CD:** Showcase a fully automated content pipeline.
- **Leverage AI:** Utilize a powerful language model for content generation.
- **Provide a Public Resource:** Share generated notes and solutions via a clean, accessible website.

---

## 2. Features

| Feature | Description |
|---------|-------------|
| **Automation Engine** | Python script orchestrated by GitHub Actions runs twice daily to generate and commit new files. |
| **AI Content Source** | Uses Google Gemini 1.5 Flash model to generate code (`.java`) and explanatory text (`.md`). |
| **Content Types** | Generates DSA Solutions and in-depth Tech Notes (Java, React, etc.). |
| **Website Generation** | Uses MkDocs with Material theme to build a static website from Markdown files. |
| **Deployment** | CI/CD pipeline deploys the site to GitHub Pages on every push to `main`. |
| **Scalability** | New content topics can be added via `topics.json`, no changes to core script needed. |
| **Uniqueness** | Avoids duplicate content; every run adds a unique file. |

---

## 3. Core Concepts & Architecture

### Content Generation (`auto.yml`)

- **main.py**: Core automation script.
  1. Initializes Gemini API client and Git configuration.
  2. Randomly chooses to generate a DSA solution or a tech note.
  3. Picks a new topic from `topics.json`.
  4. Generates content using Gemini API.
  5. Saves content into `.md` and `.java` files.
  6. Commits and pushes files to the `main` branch.

- **Trigger**: Runs twice daily or can be triggered manually via `workflow_dispatch`.

### Website Deployment (`deploy.yml`)

- **MkDocs Build**: Converts all Markdown files in `/docs` to a static HTML website.
- **Theme**: Material for MkDocs provides responsive, searchable interface.
- **gh-deploy**: Pushes built site to `gh-pages` branch (served by GitHub Pages).
- **Trigger**: Runs automatically on every push to `main`.

---

## 4. Repository Structure
```
.
├── .github/workflows/
│   ├── auto.yml          # Content generation
│   └── deploy.yml        # Website deployment
├── docs/
│   ├── dsa/
│   │   ├── easy/
│   │   ├── medium/
│   │   └── hard/
│   ├── notes/
│   │   ├── java/
│   │   └── react/
│   └── index.md          # Homepage
├── main.py               # Core automation script
├── mkdocs.yml            # MkDocs configuration
├── requirements.txt      # Python dependencies
└── topics.json           # Source of content ideas
```
---

## 4. Conclusion & Getting Started

This repository serves as a powerful example of modern automation, combining **AI**, **CI/CD**, and **static site generation** to create a self-updating knowledge base.

To set up a similar project, follow these steps:

### Fork the Repository

Create your own copy of this project.

### Clone Your Fork Locally

```bash
git clone https://github.com/<your-username>/dailly-notes.git
cd dailly-notes
```
Install Dependencies
```bash
pip install -r requirements.txt
```

Configure GitHub Secrets
```

In your forked repository's settings, go to Secrets and variables → Actions.

Create a new repository secret named GEMINI_API_KEY.

Paste your Google Gemini API key as the value.

Run Workflows
```

Once configured, the GitHub Actions workflows will run automatically. You can also trigger the auto.yml workflow manually to see it in action immediately.


This preserves proper headings, code blocks, and lists for a clean GitHub rendering.  

Do you want me to **merge this with your tree structure and previous sections** into a comple
