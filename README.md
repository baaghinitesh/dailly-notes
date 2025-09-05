<div align="center">

# 📚 Auto DSA & Tech Notes

An automated knowledge base that uses AI to generate and commit new **DSA solutions** and **tech notes** daily.

[![GitHub Actions Workflow Status](https://github.com/baaghinitesh/dailly-notes/actions/workflows/auto.yml/badge.svg)](https://github.com/baaghinitesh/dailly-notes/actions/workflows/auto.yml)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

---

## ✨ Key Features

- 🤖 **Fully Automated**: Runs twice daily at random times to mimic human behavior.  
- 💡 **Dual Content Types**:  
  - **DSA Solutions** → Java solutions for random DSA problems + Markdown explanations.  
  - **Tech Notes** → Comprehensive notes on topics like Java, React, and DSA concepts.  
- 🔄 **No Duplicates**: Automatically checks for existing files before generating new ones.  
- 📂 **Organized Structure**: Separate folders for DSA (easy/medium/hard) and notes (java/react).  
- 🧠 **Powered by AI**: Uses Google Gemini 1.5 Flash model for reliable, high-quality content.  

---

## ⚙️ How It Works

The entire process is orchestrated by a **GitHub Actions workflow**:

1. **Scheduled Trigger** → Runs twice daily with random sleep for unpredictable commit times.  
2. **Python Script Execution** → Sets up environment and runs `main.py`.  
3. **Task Selection** → Randomly picks between generating a DSA solution or a tech note.  
4. **Content Generation** → Picks a topic from `topics.json`, ensures uniqueness, sends prompt to Gemini API.  
5. **File Creation** → Saves generated content into `.java` + `.md` (DSA) or `.md` (notes).  
6. **Commit & Push** → Uses GitPython to commit and push new files automatically.  

---

<details>
<summary>📂 Repository Structure</summary>

```text
.
├── .github/workflows/
│   └── auto.yml          # 🚀 GitHub Actions workflow
├── dsa/
│   ├── easy/             # ✅ Easy DSA problems
│   ├── medium/           # 💪 Medium DSA problems
│   └── hard/             # 🔥 Hard DSA problems
├── notes/
│   ├── java/             # ☕ Java notes
│   └── react/            # ⚛️ React notes
├── main.py               # 🐍 Core Python automation script
├── topics.json           # 📋 All DSA & note topics
└── requirements.txt      # 📦 Dependencies

```
</details> 

---

## 🛠️ Tech Stack

- **Backend** → Python  
- **AI** → Google Gemini API  
- **CI/CD** → GitHub Actions  
- **Git Automation** → GitPython  

---

## 🚀 Setup & Configuration

1. **Fork this repository**.  

2. **Clone your fork**:  
   ```bash
   git clone https://github.com/<your-username>/dailly-notes.git
   cd dailly-notes
   ```
3. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```


   
