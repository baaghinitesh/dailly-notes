---
title: "Longest Palindromic Subsequence"
language: "python"
difficulty: "medium"
section: "dsa"
tags: "dsa, python, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/125/1200/630"
update_count: 0
---

# Longest Palindromic Subsequence

## Problem Understanding
The Longest Palindromic Subsequence problem asks to find the length of the longest subsequence in a given string that is a palindrome. A palindrome is a sequence that reads the same backwards as forwards. The key constraint is that the subsequence does not need to be contiguous, but it must be a subsequence of the original string. This problem is non-trivial because a naive approach, such as checking all possible subsequences, would be computationally expensive due to the exponential number of subsequences.

## Approach
The algorithm strategy is to use dynamic programming to fill a table in a bottom-up manner. The intuition behind it is to break down the problem into smaller subproblems and store the results of these subproblems to avoid redundant computation. The dynamic programming (dp) table is used to store the lengths of the longest palindromic subsequences for all possible substrings of the input string. The approach works by considering two cases for each substring: if the first and last characters are the same, they are considered as part of the palindrome, and if they are different, the maximum palindrome without the first or last character is considered.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n^2) | The algorithm has two nested loops to fill the dp table, where n is the length of the input string. The outer loop iterates over the length of the substring, and the inner loop iterates over the starting index of the substring. |
| Space  | O(n^2) | The dp table stores the lengths of the longest palindromic subsequences for all possible substrings of the input string, resulting in a space complexity of O(n^2). |

## Algorithm Walkthrough
```
Input: "bbbab"
Step 1: Initialize the dp table with zeros
dp = [[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]]
Step 2: Fill the diagonal of the dp table with 1s (all substrings with one character are palindromes)
dp = [[1, 0, 0, 0, 0],
      [0, 1, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 1, 0],
      [0, 0, 0, 0, 1]]
Step 3: Fill the dp table for substrings of length 2
dp = [[1, 2, 0, 0, 0],
      [0, 1, 2, 0, 0],
      [0, 0, 1, 2, 0],
      [0, 0, 0, 1, 2],
      [0, 0, 0, 0, 1]]
Step 4: Fill the dp table for substrings of length 3 and above
dp = [[1, 2, 3, 0, 0],
      [0, 1, 2, 3, 0],
      [0, 0, 1, 2, 3],
      [0, 0, 0, 1, 2],
      [0, 0, 0, 0, 1]]
Output: dp[0][4] = 4 (the longest palindromic subsequence is "bbbb")
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize dp table}
    B --> C[Fill diagonal with 1s]
    C --> D{Loop through substring lengths}
    D -->|Yes| E{Check if first and last characters are the same}
    E -->|Yes| F["Update dp table with dp[i + 1"][j - 1] + 2]
    E -->|No| G["Update dp table with max("dp[i + 1\"][j], dp[i][j - 1]")]
    D -->|No| H["Return dp[0"][n - 1]]
```
## Key Insight
> **Tip:** The key insight is to use dynamic programming to store the lengths of the longest palindromic subsequences for all possible substrings, avoiding redundant computation and reducing the time complexity to O(n^2).

## Edge Cases
- **Empty/null input**: If the input string is empty or null, the function returns 0, as there is no palindromic subsequence in an empty string.
- **Single element**: If the input string has only one character, the function returns 1, as a single character is always a palindrome.
- **Palindrome input**: If the input string is already a palindrome, the function returns the length of the input string, as the entire string is a palindromic subsequence.

## Common Mistakes
- **Mistake 1**: Not initializing the dp table with zeros, which can lead to incorrect results due to garbage values in the table. To avoid this, make sure to initialize the dp table with zeros before filling it.
- **Mistake 2**: Not handling the base case of substrings with one character correctly, which can lead to incorrect results. To avoid this, make sure to fill the diagonal of the dp table with 1s, as all substrings with one character are palindromes.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly, as the sorting of the input string does not affect the dynamic programming approach.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n^2) space to store the dp table, as it needs to store the lengths of the longest palindromic subsequences for all possible substrings.
- "What if there are duplicates?" → The algorithm will still work correctly, as it considers all possible substrings and handles duplicates correctly. However, the presence of duplicates can affect the time complexity, as it may increase the number of substrings to consider.

## Python Solution

```python
# Problem: Longest Palindromic Subsequence
# Language: python
# Difficulty: Medium
# Time Complexity: O(n^2) — two nested loops to fill the dp table
# Space Complexity: O(n^2) — dp table stores n^2 elements
# Approach: Dynamic Programming — fill the dp table in a bottom-up manner

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        # Edge case: empty input → return 0
        if not s:
            return 0
        
        n = len(s)
        # Initialize the dp table with zeros
        dp = [[0] * n for _ in range(n)]
        
        # All substrings with one character are palindromes
        for i in range(n):
            dp[i][i] = 1
        
        # Fill the dp table in a bottom-up manner
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                # If the first and last characters are the same, consider them as part of the palindrome
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                # Otherwise, consider the maximum palindrome without the first or last character
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        
        # The longest palindromic subsequence is stored in the top-right corner of the dp table
        return dp[0][n - 1]
```
