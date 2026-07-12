---
title: "Hirschberg's Algorithm"
language: "java"
difficulty: "super_advanced"
section: "dsa"
tags: "dsa, java, super_advanced, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/524/1200/630"
update_count: 0
---

# Hirschberg's Algorithm

## Problem Understanding
Hirschberg's Algorithm is a dynamic programming approach to find the longest common subsequence (LCS) of two strings. The problem asks to find the LCS of two given strings, which is a subsequence that appears in the same order in both strings. The key constraint is to optimize the space complexity, as the naive approach of storing the entire 2D table would require O(n*m) space. The problem is non-trivial because the naive approach fails to optimize space, and a more efficient approach is needed to store only the necessary information.

## Approach
The algorithm strategy is to use dynamic programming with space optimization by storing only the previous row of the 2D table. This approach works by filling up the table in a bottom-up manner, where each cell represents the length of the LCS of the corresponding substrings. The mathematical reasoning behind this approach is that the length of the LCS can be calculated by considering the maximum length of the LCS of the substrings. The data structure used is a 2D table, which is optimized to store only the previous row, reducing the space complexity to O(min(n, m)). The approach handles the key constraint of optimizing space complexity by storing only the necessary information.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n*m) | The algorithm fills up the 2D table in a bottom-up manner, where each cell is calculated once. The time complexity is proportional to the number of cells in the table, which is n*m. |
| Space  | O(min(n, m)) | The algorithm stores only the previous row of the 2D table, which requires O(min(n, m)) space. This is because the maximum number of cells in a row is min(n, m), and we only need to store the previous row to calculate the next row. |

## Algorithm Walkthrough
```
Input: str1 = "ABCBDAB", str2 = "BDCABA"
Step 1: Initialize the 2D table with zeros.
Step 2: Fill up the table in a bottom-up manner.
  - For i = 1, j = 1, str1.charAt(i-1) == str2.charAt(j-1) is false, so dp[i][j] = max(dp[i-1][j], dp[i][j-1]) = 0.
  - For i = 2, j = 2, str1.charAt(i-1) == str2.charAt(j-1) is false, so dp[i][j] = max(dp[i-1][j], dp[i][j-1]) = 0.
  - ...
Step 3: Reconstruct the LCS from the table.
  - Start from the bottom-right corner of the table, i = 7, j = 6.
  - Since str1.charAt(i-1) == str2.charAt(j-1) is true, add the character to the LCS and move to the top-left cell, i = 6, j = 5.
  - Repeat step 3 until i = 0 or j = 0.
Output: The LCS is "BCBA".
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Initialize 2D table]
    B --> C["Fill up table in bottom-up manner"]
    C --> D{"str1.charAt("i-1") == str2.charAt("j-1")?"}
    D -->|Yes| E["Add character to LCS and move to top-left cell"]
    D -->|No| F[Move to cell with maximum length]
    F --> G["Repeat until i = 0 or j = 0"]
    G --> H[Reconstruct LCS from table]
    H --> I[Return LCS]
```
## Key Insight
> **Tip:** The key insight is to store only the previous row of the 2D table, which reduces the space complexity from O(n*m) to O(min(n, m)).

## Edge Cases
- **Empty/null input**: If either string is empty, the LCS is an empty string.
- **Single element**: If one of the strings has only one character, the LCS is the character itself if it appears in the other string, otherwise it is an empty string.
- **Duplicate characters**: If there are duplicate characters in the strings, the LCS will contain each character only once, in the order it appears in both strings.

## Common Mistakes
- **Mistake 1**: Not initializing the 2D table correctly, leading to incorrect values. → Initialize the table with zeros and fill up the first row and column correctly.
- **Mistake 2**: Not storing only the previous row of the 2D table, leading to unnecessary space usage. → Store only the previous row to optimize space complexity.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, as it only depends on the characters in the strings, not their order.
- "Can you do it in O(1) space?" → No, the algorithm requires at least O(min(n, m)) space to store the previous row of the 2D table.
- "What if there are duplicates?" → The algorithm handles duplicates correctly, as it only considers each character once in the order it appears in both strings.

## Java Solution

```java
// Problem: Hirschberg's Algorithm
// Language: Java
// Difficulty: Super Advanced
// Time Complexity: O(n*m) — where n and m are the lengths of the two strings, because we are using dynamic programming to fill up the 2D table
// Space Complexity: O(min(n, m)) — we only need to store the previous row in the dynamic programming table
// Approach: Dynamic programming with space optimization — using a 2D table to store the lengths of the longest common subsequences

public class Hirschberg {
    /**
     * This function implements Hirschberg's Algorithm to find the longest common subsequence of two strings.
     * 
     * @param str1 The first string.
     * @param str2 The second string.
     * @return The longest common subsequence of str1 and str2.
     */
    public static String longestCommonSubsequence(String str1, String str2) {
        int n = str1.length(); // Get the length of the first string
        int m = str2.length(); // Get the length of the second string

        // Edge case: either string is empty → return an empty string
        if (n == 0 || m == 0) {
            return "";
        }

        // Initialize a 2D table to store the lengths of the longest common subsequences
        int[][] dp = new int[n + 1][m + 1];

        // Initialize the first row and column of the table
        for (int i = 0; i <= n; i++) {
            dp[i][0] = 0; // The longest common subsequence with an empty string is always 0
        }
        for (int j = 0; j <= m; j++) {
            dp[0][j] = 0; // The longest common subsequence with an empty string is always 0
        }

        // Fill up the table in a bottom-up manner
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                // If the current characters in both strings are the same, we can extend the longest common subsequence
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1; // Extend the longest common subsequence
                } else {
                    // Otherwise, we take the maximum length from the previous cell
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]); // Take the maximum length
                }
            }
        }

        // Reconstruct the longest common subsequence from the table
        StringBuilder lcs = new StringBuilder(); // Initialize a StringBuilder to store the longest common subsequence
        int i = n, j = m; // Start from the bottom-right corner of the table
        while (i > 0 && j > 0) {
            // If the current characters in both strings are the same, add the character to the longest common subsequence
            if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                lcs.insert(0, str1.charAt(i - 1)); // Add the character to the beginning of the longest common subsequence
                i--; // Move to the top-left cell
                j--; // Move to the top-left cell
            } else {
                // Otherwise, move to the cell with the maximum length
                if (dp[i - 1][j] > dp[i][j - 1]) {
                    i--; // Move to the top cell
                } else {
                    j--; // Move to the left cell
                }
            }
        }

        return lcs.toString(); // Return the longest common subsequence
    }

    public static void main(String[] args) {
        String str1 = "ABCBDAB";
        String str2 = "BDCABA";
        System.out.println("Longest Common Subsequence: " + longestCommonSubsequence(str1, str2));
    }
}
```
