<div align="center">

📚 Auto DSA & Tech Notes
An automated knowledge base that uses the Gemini AI to generate and publish new DSA solutions and tech notes daily to a live website.

Visit the Live Site ➡️

</div>

✨ Key Features
🤖 Fully Automated: A GitHub Actions workflow runs twice daily, generating new content and pushing it to the repository.

🧠 AI-Powered Content: Leverages the Google Gemini API to create high-quality, relevant DSA solutions and in-depth technical notes.

💡 Dual Content Generation:

DSA Solutions: Creates Java code for random DSA problems (Easy, Medium, Hard) along with a Markdown file explaining the approach and complexity.

Tech Notes: Generates comprehensive study notes on a wide range of topics, including Java, React, and more.

Website Publishing**: Automatically builds and deploys a static website using MkDocs and GitHub Pages, making the content easily accessible.

🔄 No Duplicates: The script intelligently picks new topics from topics.json and ensures it doesn't repeat content that has already been generated.

📂 Organized & Scalable: Content is neatly organized into docs/dsa and docs/notes, and new topics can be easily added by updating the topics.json file.

⚙️ How It Works
The project's automation is handled by two primary GitHub Actions workflows:

Content Generation (auto.yml):

Trigger: Runs on a schedule (twice a day) or can be triggered manually.

Execution: The main.py script is executed.

Topic Selection: The script randomly selects a DSA problem or a note topic from topics.json, ensuring it hasn't been created before.

AI Generation: A prompt is sent to the Google Gemini API to generate the code, explanations, or notes.

Commit & Push: The newly created files (.java and .md) are automatically committed and pushed to the main branch.

Website Deployment (deploy.yml):

Trigger: Runs automatically whenever a new push is made to the main branch.

Build: It uses MkDocs to build a static HTML website from the Markdown files in the docs directory.

Deploy: The built site is then deployed to the gh-pages branch, making it live on GitHub Pages.

<details>
<summary>📂 Repository Structure</summary>

.
├── .github/workflows/
│   ├── auto.yml          # 🤖 GitHub Actions workflow for content generation
│   └── deploy.yml        # 🚀 GitHub Actions workflow for site deployment
├── docs/                 # 📖 Contains all content for the MkDocs site
│   ├── dsa/              # 💻 DSA solutions (categorized by difficulty)
│   ├── notes/            # 📝 Tech notes (categorized by topic)
│   └── index.md          # 🏠 Home page for the site
├── main.py               # 🐍 The core Python script for AI content generation
├── mkdocs.yml            # 🔧 Configuration file for the MkDocs site
├── topics.json           # 📋 A comprehensive list of DSA & note topics
└── requirements.txt      # 📦 Python dependencies for the project

</details>

🛠️ Tech Stack
Automation: Python, GitHub Actions

AI Model: Google Gemini 1.5 Flash

Website: MkDocs (Material Theme)

Git Automation: GitPython

🚀 Local Setup & Configuration
To run this project yourself, follow these steps:

Fork this repository.

Clone your fork:

git clone [https://github.com/](https://github.com/)<your-username>/dailly-notes.git
cd dailly-notes

Install dependencies:

pip install -r requirements.txt

Set up Secrets:

Create a GitHub repository secret named GEMINI_API_KEY and add your Google Gemini API key to it. The workflow (auto.yml) requires this to authenticate with the API.

Run the script manually (optional):

# Make sure to set the environment variables locally
export API_KEY="your_gemini_api_key"
export AUTHOR_NAME="Your Name"
export AUTHOR_EMAIL="your@email.com"

python main.py

🤝 Contributing
Contributions are welcome! The easiest way to contribute is by expanding the list of topics. Feel free to add more DSA questions or note subjects to the topics.json file and submit a pull request.