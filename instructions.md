# Instructions

This project automatically generates DSA practice questions + solutions and notes using the Gemini API, 
and pushes them to GitHub twice daily at random times.

## Features
- DSA problems (Easy/Medium/Hard)
- Notes for selected topic of the day
- Two commits per day (1 file per commit)
- File names are topic-related, not by timestamp
- Supports separate React, Java, and DSA notes folders

## Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your GitHub repository remote.
4. Run the automation with:
   ```bash
   python main.py
   ```

## Notes
- Uses Gemini API (your API key is already embedded in `config.py`).
- DSA questions source: LeetCode + curated list (you can extend `topics.json`).
- Notes are saved in `.txt` format inside `/notes`.

