---
title: "Regular Expression Matching (DP)"
language: "c"
difficulty: "hard"
section: "dsa"
tags: "dsa, c, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/247/1200/630"
update_count: 0
---

# Regular Expression Matching (DP)

## Problem Understanding
The problem is asking to determine whether a given string matches a regular expression pattern. The pattern can contain two special characters: '.' which matches any single character, and '*' which matches zero or more of the preceding character. The key constraint is that the '*' character can only appear after a character, and it must match zero or more occurrences of that character. What makes this problem non-trivial is that the '*' character can match zero or more characters, which means we need to consider all possible matches of the preceding character. The naive approach of simply checking if the string matches the pattern from left to right fails because it does not consider all possible matches of the '*' character.

## Approach
The algorithm strategy is to use dynamic programming to build a 2D table that stores the matches between substrings and subpatterns. The intuition behind this approach is that we can break down the problem into smaller subproblems and store the results of these subproblems in a table. We can then use this table to compute the final result. The approach works because it considers all possible matches of the '*' character and uses the results of the subproblems to compute the final result. The data structure used is a 2D boolean array, where each cell represents whether the corresponding substring matches the corresponding subpattern. The approach handles the key constraints by considering all possible matches of the '*' character and using the results of the subproblems to compute the final result.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n*m) | The algorithm has two nested loops, each of which iterates over the string and the pattern, resulting in a time complexity of O(n*m), where n and m are the lengths of the string and pattern respectively. The operations inside the loops are constant time, so the overall time complexity is O(n*m). |
| Space  | O(n*m) | The algorithm uses a 2D boolean array of size (n+1) x (m+1) to store the dynamic programming results, resulting in a space complexity of O(n*m). The space complexity is dominated by the space required to store the dynamic programming table. |

## Algorithm Walkthrough
```
Input: s = "aa", p = "a*"
Step 1: Initialize the base case: dp[2][2] = true (empty string matches empty pattern)
Step 2: Handle the case where the pattern is not empty but the string is: dp[2][1] = dp[2][2] = true (since '*' matches zero characters)
Step 3: Fill in the rest of the table using dynamic programming:
    - dp[1][1] = dp[2][2] = true (since 'a' matches 'a')
    - dp[1][0] = false (since 'a' does not match empty string)
    - dp[0][1] = dp[1][2] || (dp[1][1] && (s[0] == p[0] || p[0] == '.')) = true (since '*' matches one or more 'a's)
Step 4: The result is stored in the top-left corner of the table: dp[0][0] = true
Output: 1 (true)
```
This walkthrough demonstrates how the algorithm fills in the dynamic programming table and computes the final result.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is string empty?"}
    B -->|Yes| C{"Is pattern empty?"}
    C -->|Yes| D["dp[n"][m] = true]
    C -->|No| E{"Is pattern character '*'?"}
    E -->|Yes| F["dp[n"][i] = dp[n][i + 1]]
    E -->|No| G["dp[n"][i] = false]
    B -->|No| H{"Is pattern character '*'?"}
    H -->|Yes| I["dp[i"][j] = dp[i][j + 1] || (dp["i + 1"][j] && (s[i] == p["j - 1"] || p["j - 1"] == '.'))]
    H -->|No| J{"Is string character equal to pattern character or '.'?"}
    J -->|Yes| K["dp[i"][j] = dp["i + 1"][j + 1]]
    J -->|No| L["dp[i"][j] = false]
    A --> M[Fill in rest of table using dynamic programming]
    M --> N["Return dp[0"][0]]
```
This flowchart illustrates the decision flow of the algorithm and how it fills in the dynamic programming table.

## Key Insight
> **Tip:** The key insight is to use dynamic programming to store the matches between substrings and subpatterns, and to consider all possible matches of the '*' character by checking two possibilities: the '*' matches zero characters, or the '*' matches one or more characters.

## Edge Cases
- **Empty/null input**: If the input string or pattern is empty, the algorithm will handle it correctly by initializing the base case and filling in the rest of the table using dynamic programming.
- **Single element**: If the input string or pattern has only one character, the algorithm will handle it correctly by checking if the characters match or if the pattern character is '.'.
- **Pattern with consecutive '*' characters**: If the pattern has consecutive '*' characters, the algorithm will handle it correctly by considering all possible matches of the '*' characters.

## Common Mistakes
- **Mistake 1**: Not considering all possible matches of the '*' character. To avoid this, make sure to check two possibilities: the '*' matches zero characters, or the '*' matches one or more characters.
- **Mistake 2**: Not initializing the base case correctly. To avoid this, make sure to initialize the base case by setting dp[n][m] = true (empty string matches empty pattern).

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not assume the input is sorted, so it will still work correctly even if the input is not sorted.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n*m) space to store the dynamic programming table, so it is not possible to do it in O(1) space.
- "What if there are duplicates?" → The algorithm will handle duplicates correctly by considering all possible matches of the '*' character and using the results of the subproblems to compute the final result.

## C Solution

```c
// Problem: Regular Expression Matching (DP)
// Language: C
// Difficulty: Hard
// Time Complexity: O(n*m) — where n and m are lengths of string and pattern respectively
// Space Complexity: O(n*m) — for the 2D dynamic programming table
// Approach: Dynamic Programming — build a 2D table to store matches between substrings and subpatterns

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

bool isMatch(char * s, char * p) {
    int n = strlen(s);
    int m = strlen(p);
    
    // Create a 2D table to store dynamic programming results
    bool **dp = (bool **)malloc((n + 1) * sizeof(bool *));
    for (int i = 0; i <= n; i++) {
        dp[i] = (bool *)malloc((m + 1) * sizeof(bool));
    }
    
    // Initialize the base case: empty string matches empty pattern
    dp[n][m] = true; // Empty string matches empty pattern
    
    // Handle the case where the pattern is not empty but the string is
    for (int i = m - 1; i >= 0; i--) {
        // If the current character in the pattern is '*', the pattern can still match an empty string
        if (p[i] == '*') {
            dp[n][i] = dp[n][i + 1];
        } else {
            dp[n][i] = false; // Non-empty pattern cannot match empty string
        }
    }
    
    // Fill in the rest of the table using dynamic programming
    for (int i = n - 1; i >= 0; i--) {
        for (int j = m - 1; j >= 0; j--) {
            // If the current characters in the string and pattern match, or the pattern character is '.'
            if (s[i] == p[j] || p[j] == '.') {
                dp[i][j] = dp[i + 1][j + 1]; // Match the rest of the string and pattern
            } else if (p[j] == '*') {
                // If the pattern character is '*', check two possibilities:
                // 1. The '*' matches zero characters in the string
                // 2. The '*' matches one or more characters in the string
                dp[i][j] = dp[i][j + 1] || (dp[i + 1][j] && (s[i] == p[j - 1] || p[j - 1] == '.'));
            } else {
                dp[i][j] = false; // Characters do not match
            }
        }
    }
    
    bool result = dp[0][0]; // The result is stored in the top-left corner of the table
    
    // Free the dynamically allocated memory
    for (int i = 0; i <= n; i++) {
        free(dp[i]);
    }
    free(dp);
    
    return result; // Edge case: return false if no match is found
}

int main() {
    char s[] = "aa";
    char p[] = "a*";
    printf("%d\n", isMatch(s, p)); // Expected output: 1 (true)
    return 0;
}
```
