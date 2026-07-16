---
title: "Maximal Square DP"
language: "cpp"
difficulty: "medium"
section: "dsa"
tags: "dsa, cpp, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/505/1200/630"
update_count: 0
---

# Maximal Square DP

## Problem Understanding
The problem is asking to find the area of the largest square that can be formed within a given binary matrix, where each cell can either be '0' (empty) or '1' (filled). The key constraint is that the square must be formed by connecting adjacent '1' cells. The problem becomes non-trivial because a naive approach, such as checking all possible sub-matrices, would have an exponential time complexity. The dynamic programming approach is used to efficiently build up a table that stores the size of the largest square that can be formed at each cell.

## Approach
The algorithm strategy is to use dynamic programming (DP) to build up a table, `dp`, where `dp[row][col]` represents the size of the largest square that can be formed with the cell at `(row, col)` as the bottom-right corner. The intuition behind this approach is to break down the problem into smaller sub-problems and store the solutions to these sub-problems in the `dp` table. The `dp` table is filled up row by row, and for each cell, the size of the largest square is determined by the minimum size of the squares above, to the left, and diagonally above-left, plus 1. The `dp` table is used to keep track of the maximum size of the square found so far.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(m*n) | The algorithm uses two nested loops to fill up the `dp` table, where `m` is the number of rows and `n` is the number of columns. Each cell is visited once, resulting in a time complexity of O(m*n). |
| Space  | O(m*n) | The algorithm uses a `dp` table with the same size as the input matrix to store the sizes of the largest squares that can be formed at each cell, resulting in a space complexity of O(m*n). |

## Algorithm Walkthrough
```
Input: 
[
  ["1","0","1","0","0"],
  ["1","0","1","1","1"],
  ["1","1","1","1","1"],
  ["1","0","0","1","0"]
]
Step 1: Initialize the dp table with zeros
dp = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
]
Step 2: Fill up the dp table row by row
  - For the first row:
    - dp[0][0] = 1 (since matrix[0][0] is '1')
    - dp[0][1] = 0 (since matrix[0][1] is '0')
    - dp[0][2] = 1 (since matrix[0][2] is '1')
    - dp[0][3] = 0 (since matrix[0][3] is '0')
    - dp[0][4] = 0 (since matrix[0][4] is '0')
  - For the second row:
    - dp[1][0] = 1 (since matrix[1][0] is '1')
    - dp[1][1] = 0 (since matrix[1][1] is '0')
    - dp[1][2] = 1 (since matrix[1][2] is '1')
    - dp[1][3] = 1 (since matrix[1][3] is '1' and dp[0][2] is 1)
    - dp[1][4] = 1 (since matrix[1][4] is '1' and dp[0][3] is 0)
Step 3: Update the maximum size of the square
maxSize = max(maxSize, dp[1][3]) = 1
Step 4: Continue filling up the dp table and updating the maximum size
...
Output: 4 (since the maximum size of the square is 2)
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is the current cell '1'?"}
    B -->|Yes| C[Update dp table]
    B -->|No| D[Move to the next cell]
    C --> E{"Is the current cell in the first row or column?"}
    E -->|Yes| F["Set dp[row"][col] to 1]
    E -->|No| G["Set dp[row"][col] to min("dp[\"row-1\"][col], dp[row][col-1], dp[\"row-1\"][col-1]") + 1]
    F --> H[Update the maximum size of the square]
    G --> H
    D --> I["Is the end of the matrix reached?"]
    I -->|Yes| J[Return the area of the maximal square]
    I -->|No| A
```
## Key Insight
> **Tip:** The key insight is to use the `dp` table to store the sizes of the largest squares that can be formed at each cell, and to update the maximum size of the square as we fill up the `dp` table.

## Edge Cases
- **Empty/null input**: If the input matrix is empty or null, the function returns 0, since there are no cells to form a square.
- **Single element**: If the input matrix has only one element, the function returns 1 if the element is '1', and 0 if the element is '0'.
- **Matrix with all zeros**: If the input matrix has all zeros, the function returns 0, since there are no cells to form a square.

## Common Mistakes
- **Mistake 1**: Not initializing the `dp` table with zeros, which can lead to incorrect results.
- **Mistake 2**: Not updating the maximum size of the square correctly, which can lead to incorrect results.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not rely on the input being sorted, so it will still work correctly.
- "Can you do it in O(1) space?" → No, the algorithm requires O(m*n) space to store the `dp` table, where `m` is the number of rows and `n` is the number of columns.
- "What if there are duplicates?" → The algorithm can handle duplicates correctly, since it only cares about the presence or absence of '1' cells.

## CPP Solution

```cpp
// Problem: Maximal Square DP
// Language: cpp
// Difficulty: Medium
// Time Complexity: O(m*n) — two nested loops to fill up the dp table
// Space Complexity: O(m*n) — dp table to store the sizes of maximal squares
// Approach: Dynamic Programming (DP) — build up the dp table row by row

class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        // Edge case: empty input matrix → return 0
        if (matrix.empty() || matrix[0].empty()) return 0;

        int rows = matrix.size();  // get the number of rows
        int cols = matrix[0].size();  // get the number of columns

        // create a dp table with the same size as the input matrix
        vector<vector<int>> dp(rows, vector<int>(cols, 0));

        int maxSize = 0;  // initialize the maximum size of the square
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                // if the current cell is '1', update the dp table
                if (matrix[row][col] == '1') {
                    // for the first row or column, the size is 1
                    if (row == 0 || col == 0) {
                        dp[row][col] = 1;
                    } else {
                        // for other cells, the size is the minimum size of the top, left, and top-left cells plus 1
                        dp[row][col] = min(min(dp[row-1][col], dp[row][col-1]), dp[row-1][col-1]) + 1;
                    }
                    // update the maximum size
                    maxSize = max(maxSize, dp[row][col]);
                }
            }
        }
        // return the area of the maximal square
        return maxSize * maxSize;
    }
};
```
