---
title: "Decode Ways JS DP"
language: "javascript"
difficulty: "medium"
section: "dsa"
tags: "dsa, javascript, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/340/1200/630"
update_count: 0
---

# Decode Ways JS DP

## Problem Understanding
The problem is asking us to find the number of ways to decode a given string where each character can be either a single digit or a combination of two digits. The key constraints are that a single digit can only be decoded if it is not zero, and a combination of two digits can only be decoded if the number formed by the two digits is between 10 and 26. This problem is non-trivial because a naive approach that simply checks all possible combinations would result in exponential time complexity. The problem requires a dynamic programming approach to efficiently calculate the number of ways to decode the string.

## Approach
The algorithm strategy used here is dynamic programming, where we calculate the number of ways to decode each substring of the input string. The intuition behind this approach is that the number of ways to decode a substring depends on the number of ways to decode its smaller substrings. We use a DP array to store the number of ways to decode each substring, and we fill up this array iteratively. The mathematical reasoning behind this approach is that the number of ways to decode a substring is the sum of the number of ways to decode its smaller substrings, taking into account the constraints on single digits and combinations of two digits. We use an array of size `s.length + 1` to store the DP values, where `dp[i]` represents the number of ways to decode the substring `s[0..i-1]`.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We make a single pass through the input string, where n is the length of the string. For each character, we perform a constant amount of work to update the DP array. |
| Space  | O(n)  | We use a DP array of size n+1 to store the number of ways to decode each substring. This is the maximum amount of space used by the algorithm. |

## Algorithm Walkthrough
```
Input: s = "226"
Step 1: Initialize DP array dp = [0, 0, 0, 0] (since s.length = 3)
Step 2: Set dp[0] = 1 (base case: one way to decode an empty string)
Step 3: Set dp[1] = 1 (since s[0] = '2', which is not zero)
Step 4: For i = 2:
  * s[i-1] = '2', which is not zero, so dp[2] += dp[1] = 1
  * s[i-2] = '2' and s[i-1] = '2', which forms a valid number, so dp[2] += dp[0] = 1
  * dp[2] = 2
Step 5: For i = 3:
  * s[i-1] = '6', which is not zero, so dp[3] += dp[2] = 2
  * s[i-2] = '2' and s[i-1] = '6', which forms a valid number, so dp[3] += dp[1] = 1
  * dp[3] = 3
Output: dp[3] = 3 (number of ways to decode the entire string)
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Empty string?"}
    B -->|Yes| C["Set dp[0"] = 1]
    B -->|No| D{"First character is zero?"}
    D -->|Yes| E["Set dp[1"] = 0]
    D -->|No| F["Set dp[1"] = 1]
    F --> G["Iterate through string from i=2 to end"]
    G --> H{"Current character is not zero?"}
    H -->|Yes| I["Add dp[i-1"] to dp[i]]
    H -->|No| J{"Last two characters form a valid number?"}
    J -->|Yes| K["Add dp[i-2"] to dp[i]]
    J -->|No| L[Continue to next iteration]
    L --> M["Return dp[s.length"]]
```
## Key Insight
> **Tip:** The key insight here is to recognize that the number of ways to decode a substring depends on the number of ways to decode its smaller substrings, and that we can use dynamic programming to efficiently calculate this.

## Edge Cases
- **Empty input**: If the input string is empty, the function returns 0, since there are no ways to decode an empty string.
- **Single element**: If the input string has only one character, the function returns 1 if the character is not zero, and 0 if it is zero, since a single digit can only be decoded if it is not zero.
- **Leading zeros**: If the input string has leading zeros, the function returns 0, since a leading zero cannot be decoded.

## Common Mistakes
- **Mistake 1**: Not initializing the DP array correctly, leading to incorrect results. To avoid this, make sure to initialize the DP array with the correct size and base cases.
- **Mistake 2**: Not considering the constraints on single digits and combinations of two digits, leading to incorrect results. To avoid this, make sure to check the constraints correctly in the algorithm.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, since it only depends on the local properties of the input string.
- "Can you do it in O(1) space?" → No, since we need to store the DP array to calculate the number of ways to decode the string.
- "What if there are duplicates?" → The algorithm still works correctly, since it only depends on the local properties of the input string, and duplicates do not affect the result.

## Javascript Solution

```javascript
// Problem: Decode Ways
// Language: javascript
// Difficulty: Medium
// Time Complexity: O(n) — single pass through string using DP
// Space Complexity: O(n) — DP array stores at most n elements
// Approach: Dynamic Programming — for each character, calculate the number of ways to decode

/**
 * @param {string} s
 * @return {number}
 */
var numDecodings = function(s) {
    // Edge case: empty input → return 0
    if (!s) return 0;

    // Initialize DP array with size s.length + 1
    let dp = new Array(s.length + 1).fill(0);

    // Base case: there is one way to decode an empty string
    dp[0] = 1;

    // If the first character is not zero, there is one way to decode it
    dp[1] = s[0] === '0' ? 0 : 1;

    // Iterate through the string from the second character to the end
    for (let i = 2; i <= s.length; i++) {
        // If the current character is not zero, we can decode it separately
        if (s[i - 1] !== '0') {
            dp[i] += dp[i - 1]; // decode the current character separately
        }

        // If the last two characters form a valid number (10-26), we can decode them together
        if (s[i - 2] === '1' || (s[i - 2] === '2' && s[i - 1] <= '6')) {
            dp[i] += dp[i - 2]; // decode the last two characters together
        }
    }

    // The number of ways to decode the entire string is stored in dp[s.length]
    return dp[s.length];
};
```
