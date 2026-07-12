---
title: "N-Queens II JS Backtracking"
language: "javascript"
difficulty: "hard"
section: "dsa"
tags: "dsa, javascript, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/936/1200/630"
update_count: 0
---

# N-Queens II JS Backtracking

## Problem Understanding
The N-Queens II problem asks to find the total number of distinct solutions to the N-Queens puzzle, where the goal is to place N queens on an NxN chessboard such that no two queens attack each other. The key constraint is that each queen must be placed in a unique column and row, and no two queens can be on the same diagonal. This problem is non-trivial because the number of possible configurations grows exponentially with the size of the board, making a naive approach of checking all possible configurations impractical. The problem requires a more efficient algorithm that can prune the search space effectively.

## Approach
The approach used to solve this problem is backtracking with constraint checking. The algorithm tries to place queens in each column and backtracks when a conflict is found. The `isValid` function checks if a queen can be placed at a given position by iterating over all previously placed queens and checking for column and diagonal conflicts. The `placeQueens` function uses recursion to try placing queens in each column, and the `board` array is used to keep track of the current configuration. This approach works because it systematically explores all possible configurations while avoiding duplicate work by backtracking when a conflict is found.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(N!) | The algorithm generates all possible board configurations using backtracking, resulting in a time complexity of O(N!), where N is the size of the board. This is because there are N choices for the first row, N-1 choices for the second row, and so on, resulting in a total of N! possible configurations. |
| Space  | O(N)  | The space complexity is O(N) due to the recursion stack and the board representation, which requires O(N) space to store the current configuration. The recursion stack can grow up to a depth of N in the worst case, resulting in a space complexity of O(N). |

## Algorithm Walkthrough
```
Input: n = 4
Step 1: Initialize count = 0 and board = [-1, -1, -1, -1]
Step 2: Call placeQueens(0)
Step 3: Try placing a queen in each column:
  - Column 0: isValid(0, 0) = true, so place queen at (0, 0) and call placeQueens(1)
  - Column 1: isValid(0, 1) = true, so place queen at (0, 1) and call placeQueens(1)
  - ...
Step 4: Recursively try placing the remaining queens:
  - placeQueens(1): try placing a queen in each column
  - placeQueens(2): try placing a queen in each column
  - ...
Step 5: When a valid configuration is found, increment count and backtrack
Output: count = 2
```
This walkthrough shows how the algorithm systematically explores all possible configurations and backtracks when a conflict is found.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize count and board}
    B --> C["Call placeQueens(0)"]
    C --> D{Try placing a queen in each column}
    D -->|yes| E[Check if queen can be placed at current position]
    E -->|yes| F[Place queen at current position]
    F --> G["Call placeQueens("row + 1")"]
    G --> H{"All queens placed?"}
    H -->|yes| I[Increment count and backtrack]
    H -->|no| D
    I --> J[Return count]
```
This flowchart shows the main logic path of the algorithm, including the recursive calls to `placeQueens` and the backtracking when a conflict is found.

## Key Insight
> **Tip:** The key insight is to use a recursive approach with backtracking to systematically explore all possible configurations while avoiding duplicate work.

## Edge Cases
- **Empty/null input**: If the input is null or empty, the algorithm will not work correctly. To handle this, we can add a simple check at the beginning of the `totalNQueens` function to return 0 if the input is null or empty.
- **Single element**: If the input is 1, the algorithm will return 1, which is correct because there is only one way to place a single queen on a 1x1 board.
- **Large input**: If the input is very large, the algorithm may take a long time to run due to the exponential time complexity. To handle this, we can consider using a more efficient algorithm or optimizing the current algorithm to reduce the time complexity.

## Common Mistakes
- **Mistake 1**: Not checking for diagonal conflicts when placing a queen. To avoid this, we need to add a check in the `isValid` function to ensure that the queen is not on the same diagonal as any previously placed queens.
- **Mistake 2**: Not backtracking correctly when a conflict is found. To avoid this, we need to make sure that we are correctly resetting the board and count variables when backtracking.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not rely on the input being sorted, so it will work correctly regardless of the input order.
- "Can you do it in O(1) space?" → No, the algorithm requires O(N) space to store the board and recursion stack, so it is not possible to reduce the space complexity to O(1).
- "What if there are duplicates?" → The algorithm does not handle duplicates explicitly, but it will correctly count each distinct configuration only once. If duplicates are allowed, we would need to modify the algorithm to count each duplicate configuration separately.

## Javascript Solution

```javascript
// Problem: N-Queens II JS Backtracking
// Language: javascript
// Difficulty: hard
// Time Complexity: O(N!) — generating all possible board configurations using backtracking
// Space Complexity: O(N) — recursion stack and board representation
// Approach: Backtracking with constraint checking — try placing queens in each column and backtrack when a conflict is found

class Solution {
    /**
     * @param {number} n
     * @return {number}
     */
    totalNQueens(n) {
        // Initialize count of valid configurations
        let count = 0;
        
        // Create a board representation as an array of column indices
        let board = new Array(n).fill(-1);

        // Define a helper function to check if a queen can be placed at a given position
        function isValid(row, col) {
            // Check all previously placed queens
            for (let i = 0; i < row; i++) {
                // Check if the queen is in the same column or on the same diagonal
                if (board[i] === col || board[i] - i === col - row || board[i] + i === col + row) {
                    return false;
                }
            }
            return true;
        }

        // Define a helper function to place queens using backtracking
        function placeQueens(row) {
            // Edge case: all queens have been placed
            if (row === n) {
                count++; // Increment count of valid configurations
                return;
            }

            // Try placing a queen in each column
            for (let col = 0; col < n; col++) {
                // Check if the queen can be placed at the current position
                if (isValid(row, col)) {
                    // Place the queen at the current position
                    board[row] = col;
                    
                    // Recursively try placing the remaining queens
                    placeQueens(row + 1);
                }
            }
        }

        // Start placing queens from the first row
        placeQueens(0);

        // Return the total count of valid configurations
        return count;
    }
}

// Example usage
let solution = new Solution();
console.log(solution.totalNQueens(4)); // Output: 2
```
