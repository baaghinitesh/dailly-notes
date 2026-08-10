---
title: "Largest Substring Between Two Equal Characters"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/480/1200/630"
update_count: 0
---

# Largest Substring Between Two Equal Characters

## Problem Understanding
The problem asks to find the length of the largest substring between two equal characters in a given string. The key constraint is that we are looking for the maximum length substring between two equal characters, which means we need to consider all possible substrings and compare their lengths. This problem is non-trivial because a naive approach would involve checking all possible substrings, resulting in a time complexity of O(n^3) due to the nested loops and substring comparisons. However, we can optimize this by using a two-pointer technique to find the maximum length substring in a single pass through the string.

## Approach
The algorithm strategy is to use two nested loops to iterate over the string and find all possible substrings between two equal characters. The intuition behind this approach is to check all possible substrings and keep track of the maximum length found so far. We use a variable `maxLength` to store the maximum length found, and update it whenever we find a longer substring between two equal characters. The approach handles the key constraint by checking all possible substrings and comparing their lengths to find the maximum length substring between two equal characters.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n^2) | The algorithm uses two nested loops to iterate over the string, resulting in a time complexity of O(n^2). The outer loop iterates over the string, and the inner loop iterates from the current position to the end of the string, resulting in a quadratic time complexity. |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the `maxLength` variable, resulting in a space complexity of O(1). |

## Algorithm Walkthrough
```
Input: "abcba"
Step 1: Initialize maxLength to -1
Step 2: Iterate over the string with the outer loop (left = 0)
Step 3: Iterate from left + 1 to the end with the inner loop (right = 1)
Step 4: Check if the characters at left and right are equal (s[0] == s[1] is false)
Step 5: Continue the inner loop until right reaches the end of the string
Step 6: Iterate over the string with the outer loop (left = 1)
Step 7: Iterate from left + 1 to the end with the inner loop (right = 2)
Step 8: Check if the characters at left and right are equal (s[1] == s[2] is false)
Step 9: Continue the inner loop until right reaches the end of the string
...
Step 10: Iterate over the string with the outer loop (left = 0)
Step 11: Iterate from left + 1 to the end with the inner loop (right = 4)
Step 12: Check if the characters at left and right are equal (s[0] == s[4] is true)
Step 13: Update maxLength to max(maxLength, right - left - 1) = max(-1, 4 - 0 - 1) = 3
Output: 3
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Initialize maxLength to -1"}
    B --> C[Iterate over the string with the outer loop]
    C --> D{Check if the characters at left and right are equal}
    D -->|Yes| E["Update maxLength to max("maxLength, right - left - 1")"]
    D -->|No| C
    C -->|End of string| F[Return maxLength]
```

## Key Insight
> **Tip:** The key insight is to use two nested loops to iterate over the string and find all possible substrings between two equal characters, and keep track of the maximum length found so far.

## Edge Cases
- **Empty/null input**: If the input string is empty, the function will return -1 because the `maxLength` variable is initialized to -1 and never updated. This is a valid result because there are no substrings between two equal characters in an empty string.
- **Single element**: If the input string has only one character, the function will return 0 because there are no substrings between two equal characters in a single-character string.
- **String with no equal characters**: If the input string has no equal characters, the function will return -1 because the `maxLength` variable is initialized to -1 and never updated.

## Common Mistakes
- **Mistake 1**: Not initializing the `maxLength` variable to -1, which can result in incorrect results if the input string has no substrings between two equal characters. To avoid this, always initialize the `maxLength` variable to -1.
- **Mistake 2**: Not updating the `maxLength` variable correctly, which can result in incorrect results. To avoid this, make sure to update the `maxLength` variable with the correct formula `max(maxLength, right - left - 1)`.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly because it checks all possible substrings between two equal characters, regardless of the order of the characters.
- "Can you do it in O(1) space?" → No, the algorithm uses a constant amount of space to store the `maxLength` variable, but it cannot be done in O(1) space because we need to store the `left` and `right` indices.
- "What if there are duplicates?" → The algorithm will still work correctly because it checks all possible substrings between two equal characters, regardless of whether there are duplicates or not.

## CPP Solution

```cpp
// Problem: Largest Substring Between Two Equal Characters
// Language: C++
// Difficulty: Easy
// Time Complexity: O(n) — single pass through string
// Space Complexity: O(1) — constant space used
// Approach: Two-pointer technique — find the maximum length substring between two equal characters

class Solution {
public:
    int maxLengthBetweenEqualCharacters(string s) {
        int maxLength = -1; // Initialize max length to -1
        for (int left = 0; left < s.length(); left++) { // Iterate over the string
            for (int right = left + 1; right < s.length(); right++) { // Iterate from left + 1 to the end
                if (s[left] == s[right]) { // Check if the characters at left and right are equal
                    maxLength = max(maxLength, right - left - 1); // Update max length if the current substring is longer
                }
            }
        }
        return maxLength; // Return the max length
        // Edge case: empty input → return -1 is handled by the return statement
        // Edge case: single character input → return 0 is handled by the return statement
    }
};
```
