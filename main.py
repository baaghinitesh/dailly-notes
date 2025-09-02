import os
import random
import sys
import json
import git
import google.generativeai as genai
import datetime

# ------------------ Get config from environment variables ------------------
API_KEY = os.environ.get("API_KEY")
AUTHOR_NAME = os.environ.get("AUTHOR_NAME")
AUTHOR_EMAIL = os.environ.get("AUTHOR_EMAIL")

if not API_KEY or not AUTHOR_NAME or not AUTHOR_EMAIL:
    print("Error: Make sure to set API_KEY, AUTHOR_NAME, and AUTHOR_EMAIL environment variables.")
    sys.exit(1)

# ------------------ Gemini setup ------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ------------------ Load topics ------------------
def load_topics():
    with open("topics.json", "r", encoding="utf-8") as f:
        return json.load(f)

topics = load_topics()

# ------------------ AI Content Generator ------------------
def generate_content(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No response generated."
    except Exception as e:
        return f"Error generating content: {e}"

# ------------------ Pickers ------------------
def pick_dsa_question():
    difficulty = random.choice(["easy", "medium", "hard"])
    question = random.choice(topics[difficulty])
    return difficulty, question

def pick_note_topic():
    section = random.choice(list(topics["notes"].keys()))
    note = random.choice(topics["notes"][section])
    return section, note

# ------------------ File + Git ------------------
def save_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def commit_and_push(file_paths: list, message: str):
    repo = git.Repo(".")
    for file_path in file_paths:
        repo.git.add(file_path)
    repo.index.commit(message, author=git.Actor(AUTHOR_NAME, AUTHOR_EMAIL))
    origin = repo.remote(name="origin")
    origin.push()

# ------------------ Task ------------------
def daily_task():
    if random.choice([True, False]):
        difficulty, question = pick_dsa_question()
        
        # Prompt for Java solution
        java_prompt = (
            f"/*\n"
            f"Question: {question}\n"
            f"Difficulty: {difficulty.capitalize()}\n"
            f"*/\n\n"
            f"// Please provide a well-formatted Java solution for the problem above.\n"
            f"// The class name should be the problem name in CamelCase (e.g., TwoSum).\n"
            f"public class {question.replace(' ', '')} {{\n"
            f"    // Your solution here\n"
            f"}}\n"
        )
        java_solution = generate_content(java_prompt)
        
        # Prompt for summary
        summary_prompt = (
            f"Provide a brief summary and complexity analysis for the Java solution to the following problem:\n"
            f"Problem: {question}\n\n"
            f"Format your answer as follows:\n\n"
            f"## Summary of Approach\n"
            f"...\n\n"
            f"## Time and Space Complexity\n"
            f"- **Time Complexity**: O(...)\n"
            f"- **Space Complexity**: O(...)\n"
        )
        summary_content = generate_content(summary_prompt)
        
        # File names and paths
        file_name_base = question.replace(' ', '')
        java_file_name = f"dsa/{difficulty}/{file_name_base}.java"
        summary_file_name = f"dsa/{difficulty}/{file_name_base}.md"
        
        # Save files
        save_file(java_file_name, java_solution)
        save_file(summary_file_name, summary_content)
        
        # Commit and push
        commit_and_push([java_file_name, summary_file_name], f"Added DSA solution: {question}")
        print(f"✅ DSA solution added: {question}")
        
    else:
        section, note = pick_note_topic()
        
        # Prompt for premium notes
        prompt = (
            f"# In-Depth Study Notes: {note}\n\n"
            "Please provide a comprehensive, well-structured, and premium-quality note on the topic above. "
            "The notes should be easy to understand for both beginners and intermediate learners. "
            "Include the following sections:\n\n"
            "## 1. Introduction\n"
            "- A brief, engaging overview of the topic.\n\n"
            "## 2. Core Concepts\n"
            "- Detailed explanations of the fundamental concepts.\n"
            "- Use bullet points, bold text, and code snippets for clarity.\n\n"
            "## 3. Practical Examples\n"
            "- Provide at least two real-world code examples with clear explanations.\n"
            "- Use code blocks with syntax highlighting.\n\n"
            "## 4. Advanced Topics (Optional)\n"
            "- Briefly touch upon any advanced aspects or best practices related to the topic.\n\n"
            "## 5. Conclusion\n"
            "- A concise summary of the key takeaways.\n"
        )
        content = generate_content(prompt)
        file_name = f"notes/{section}/{note.replace(' ', '_')}.md"
        save_file(file_name, content)
        commit_and_push([file_name], f"Added notes: {note}")
        print(f"✅ Notes added: {note}")


# ------------------ Run ------------------
if __name__ == "__main__":
    daily_task()