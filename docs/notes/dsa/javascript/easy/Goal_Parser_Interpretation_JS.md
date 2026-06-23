---
title: "Goal Parser Interpretation JS"
language: "javascript"
difficulty: "easy"
section: "dsa"
tags: "dsa, javascript, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/552/1200/630"
update_count: 0
---

# Goal Parser Interpretation JS

## Problem Understanding
The problem requires interpreting a given command string by replacing specific patterns with corresponding characters. The command string can contain "()", "(al)", and other characters. The goal is to replace "()" with "o" and "(al)" with "al" and return the resulting string. The key constraints are that the input string can be empty or contain multiple occurrences of the patterns to be replaced. What makes this problem non-trivial is the need to handle the replacement of patterns in a single pass through the string while maintaining the correct order of characters.

## Approach
The algorithm strategy is to iterate through the command string and check for the presence of "()" or "(al)" patterns. When a pattern is found, it is replaced with the corresponding character ("o" or "al"). The approach works by maintaining a current index and moving it forward based on the pattern found. A result string is used to store the interpreted command. The data structure used is a simple string, which is sufficient to store the result. The approach handles the key constraints by checking for the patterns in a single pass through the string and appending the corresponding characters to the result string.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through the command string once, where n is the length of the string. Each character is processed in constant time. |
| Space  | O(n)  | The algorithm uses a result string to store the interpreted command, which can be at most n characters long in the worst case. |

## Algorithm Walkthrough
```
Input: "G()(al)"
Step 1: Initialize result = "" and i = 0
Step 2: i = 0, command[0] = "G", result = "G", i = 1
Step 3: i = 1, command[1] = "(", command[2:4] = "()", result = "Go", i = 3
Step 4: i = 3, command[3] = "(", command[4:6] = "(al)", result = "Goal", i = 7
Step 5: i = 7, i >= command.length, return result = "Goal"
Output: "Goal"
```
This example demonstrates the interpretation of the command string "G()(al)".

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Current character is \"(\""}
    B -->|Yes| C{Next two characters are "al"}
    C -->|Yes| D[Append "al" to result and move index 4 steps forward]
    C -->|No| E[Append "o" to result and move index 2 steps forward]
    B -->|No| F[Append current character to result and move index 1 step forward]
    D --> G{End of string reached}
    E --> G
    F --> G
    G -->|Yes| H[Return result]
    G -->|No| A
```
This flowchart illustrates the decision-making process in the algorithm.

## Key Insight
> **Tip:** The key insight is to use a simple string replacement approach, iterating through the command string and checking for patterns to replace, allowing for efficient interpretation of the command.

## Edge Cases
- **Empty input**: The algorithm returns an empty string because there are no characters to process.
- **Single element**: The algorithm returns the single element as is, because there are no patterns to replace.
- **No patterns to replace**: The algorithm returns the original string, because no replacements are made.

## Common Mistakes
- **Mistake 1**: Not checking for the "(al)" pattern before replacing "()" can lead to incorrect results. To avoid this, always check for "(al)" before replacing "()".
- **Mistake 2**: Not moving the index correctly after replacing a pattern can lead to incorrect results. To avoid this, move the index based on the length of the pattern replaced.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works in O(n) time because it only needs to iterate through the string once.
- "Can you do it in O(1) space?" → No, because the algorithm needs to store the result string, which can be at most n characters long.
- "What if there are duplicates?" → The algorithm still works correctly, replacing each occurrence of the patterns with the corresponding characters.

## Javascript Solution

```javascript
// Problem: Goal Parser Interpretation
// Language: javascript
// Difficulty: easy
// Time Complexity: O(n) — single pass through string
// Space Complexity: O(n) — output string can be at most n characters
// Approach: simple string replacement — replace "()" and "(al)" with "o" and "al" respectively

class Solution {
    /**
     * @param {string} command
     * @return {string}
     */
    interpret(command) {
        // Initialize an empty string to store the result
        let result = "";

        // Initialize a variable to keep track of the current index
        let i = 0;

        // Loop through the command string
        while (i < command.length) {
            // If the current character is an opening parenthesis
            if (command[i] === "(") {
                // If the next two characters are "al"
                if (command.substring(i + 1, i + 3) === "al") {
                    // Append "al" to the result and move the index 4 steps forward
                    result += "al"; // Append "al" to the result
                    i += 4; // Move the index 4 steps forward
                } else {
                    // If the next character is a closing parenthesis, append "o" to the result and move the index 2 steps forward
                    result += "o"; // Append "o" to the result
                    i += 2; // Move the index 2 steps forward
                }
            } else {
                // If the current character is not an opening parenthesis, append it to the result and move the index 1 step forward
                result += command[i]; // Append the current character to the result
                i += 1; // Move the index 1 step forward
            }
        }

        // Return the result
        return result;
    }
}

// Test the function
let solution = new Solution();
console.log(solution.interpret("G()(al)")); // Expected output: "Goal"
console.log(solution.interpret("G()()()()(al)")); // Expected output: "Gooooal"
console.log(solution.interpret("(al)G(al)")); // Expected output: "alGal"
console.log(solution.interpret("")); // Expected output: ""
console.log(solution.interpret("G")); // Expected output: "G"
```
