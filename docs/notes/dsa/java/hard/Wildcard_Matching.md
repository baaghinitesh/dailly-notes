---
title: "Wildcard Matching"
language: "java"
difficulty: "hard"
section: "dsa"
tags: "dsa, java, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/7/1200/630"
update_count: 0
---

# Wildcard Matching

## Problem Understanding
The problem of Wildcard Matching involves determining whether a given input string matches a specified pattern that can contain wildcard characters. The pattern can include two types of wildcard characters: '?' (which matches any single character) and '*' (which matches zero or more characters). The key constraint in this problem is the presence of these wildcard characters, which requires a non-trivial approach to handle the various possible matches. A naive approach would fail to account for the combinatorial complexity introduced by the '*' character, which can match any number of characters in the input string.

## Approach
The algorithm strategy employed to solve this problem is Dynamic Programming, which involves building a table to track the matches between the input string and the pattern. This approach works by breaking down the problem into smaller sub-problems and storing the solutions to these sub-problems in a table to avoid redundant computations. The table is a 2D array where each cell represents whether the corresponding substrings of the input and pattern match. The '*' character is handled by considering two possibilities: it can either match with zero characters or with one or more characters. The '?' character is handled by simply checking if the current characters in the string and pattern match.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n*m) | The algorithm uses two nested loops to fill the dynamic programming table, where n is the length of the input string and m is the length of the pattern. Each cell in the table is computed once, resulting in a time complexity of O(n*m). |
| Space  | O(n*m) | The algorithm uses a 2D array of size (n+1) x (m+1) to store the dynamic programming table, where n is the length of the input string and m is the length of the pattern. This results in a space complexity of O(n*m). |

## Algorithm Walkthrough
```
Input: s = "aa", p = "a"
Step 1: Initialize the base case: dp[s.length()][p.length()] = true
Step 2: Fill the last row of the table: dp[s.length()][j] = dp[s.length()][j + 1] if p.charAt(j) == '*'
Step 3: Fill the rest of the table:
  - For i = s.length() - 1, j = p.length() - 1: dp[i][j] = false (since 'a' != '?')
  - For i = s.length() - 2, j = p.length() - 1: dp[i][j] = false (since 'a' != '?')
Output: dp[0][0] = false

Input: s = "cb", p = "?a"
Step 1: Initialize the base case: dp[s.length()][p.length()] = true
Step 2: Fill the last row of the table: dp[s.length()][j] = dp[s.length()][j + 1] if p.charAt(j) == '*'
Step 3: Fill the rest of the table:
  - For i = s.length() - 1, j = p.length() - 1: dp[i][j] = dp[i + 1][j + 1] (since 'b' == 'a' is not true and 'b' != '?')
  - For i = s.length() - 2, j = p.length() - 1: dp[i][j] = dp[i + 1][j + 1] (since 'c' != 'a' and 'c' != '?')
Output: dp[0][0] = false
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is Input String Empty?"}
    B -->|Yes| C{"Is Pattern Empty?"}
    C -->|Yes| D[Return True]
    C -->|No| E{"Is Pattern '*'?"}
    E -->|Yes| F[Return True]
    E -->|No| G[Return False]
    B -->|No| H{"Is Pattern '*'?"}
    H -->|Yes| I["Return dp[i"][j + 1] or dp["i + 1"][j]]
    H -->|No| J{"Is Pattern '?'?"}
    J -->|Yes| K["Return dp[i + 1"][j + 1]]
    J -->|No| L{"Is String Char == Pattern Char?"}
    L -->|Yes| M["Return dp[i + 1"][j + 1]]
    L -->|No| N[Return False]
```

## Key Insight
> **Tip:** The key insight to solving this problem is to recognize that the '*' character can match with zero or more characters in the input string, and to handle this by considering two possibilities: '*' matches with zero characters, or '*' matches with one or more characters.

## Edge Cases
- **Empty/null input**: If the input string or pattern is null, the algorithm throws a NullPointerException. If both are empty, the algorithm returns true.
- **Single element**: If the input string has a single character and the pattern has a single character, the algorithm checks if they match or if the pattern character is '?'.
- **Pattern with only '*'**: If the pattern consists only of '*' characters, the algorithm returns true for any input string.

## Common Mistakes
- **Mistake 1**: Not handling the '*' character correctly → To avoid this, consider the two possibilities: '*' matches with zero characters, or '*' matches with one or more characters.
- **Mistake 2**: Not initializing the base case correctly → To avoid this, make sure to initialize the base case where the input string is empty and the pattern is empty.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not rely on the input being sorted, so it would still work correctly.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n*m) space to store the dynamic programming table.
- "What if there are duplicates?" → The algorithm handles duplicates correctly by considering all possible matches between the input string and the pattern.

## Java Solution

```java
// Problem: Wildcard Matching
// Language: Java
// Difficulty: Hard
// Time Complexity: O(n*m) — dynamic programming with two nested loops
// Space Complexity: O(n*m) — 2D array to store dynamic programming table
// Approach: Dynamic Programming — build a table to track matches between string and pattern

public class Solution {
    /**
     * Returns true if the input string matches the given pattern.
     * @param s The input string.
     * @param p The pattern string.
     * @return True if the input string matches the pattern, false otherwise.
     */
    public boolean isMatch(String s, String p) {
        // Edge case: empty input string and pattern → return true if both are empty
        if (s == null || p == null) {
            throw new NullPointerException("Input string and pattern cannot be null");
        }

        // Create a 2D array to store the dynamic programming table
        boolean[][] dp = new boolean[s.length() + 1][p.length() + 1];

        // Initialize the base case: empty string matches with empty pattern
        dp[s.length()][p.length()] = true;

        // Fill the last row of the table: empty string can only match with '*' in the pattern
        for (int j = p.length() - 1; j >= 0; j--) {
            // If the current character in the pattern is '*', it can match with zero or more characters in the string
            if (p.charAt(j) == '*') {
                dp[s.length()][j] = dp[s.length()][j + 1];
            }
        }

        // Fill the rest of the table using dynamic programming
        for (int i = s.length() - 1; i >= 0; i--) {
            for (int j = p.length() - 1; j >= 0; j--) {
                // If the current characters in the string and pattern match, or the pattern character is '?'
                if (s.charAt(i) == p.charAt(j) || p.charAt(j) == '?') {
                    dp[i][j] = dp[i + 1][j + 1]; // Move to the next characters in both string and pattern
                } 
                // If the pattern character is '*', it can match with zero or more characters in the string
                else if (p.charAt(j) == '*') {
                    // Two possibilities: '*' matches with zero characters, or '*' matches with one or more characters
                    dp[i][j] = dp[i][j + 1] || dp[i + 1][j]; 
                }
            }
        }

        // The result is stored in the top-left cell of the table
        return dp[0][0];
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.isMatch("aa", "a")); // false
        System.out.println(solution.isMatch("aa", "*")); // true
        System.out.println(solution.isMatch("cb", "?a")); // false
        System.out.println(solution.isMatch("adceb", "*a*b")); // true
        System.out.println(solution.isMatch("", "")); // true
        System.out.println(solution.isMatch("", "*")); // true
    }
}
```
