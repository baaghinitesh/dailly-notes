---
title: "Divisor Game Math/DP"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/718/1200/630"
update_count: 0
---

# Divisor Game Math/DP

## Problem Understanding
The Divisor Game is a mathematical problem where two players, Alice and Bob, take turns playing a game. The game starts with a number `n`, and in each turn, the current player chooses a divisor `x` of `n`, and the next player must play with `n - x`. The game ends when `n` becomes 0 or 1, and the last player to play wins. The problem is asking whether Alice can win the game if she plays first. The key constraint is that the game starts with a number `n`, and the players must choose divisors of `n` in each turn. This problem is non-trivial because it requires analyzing all possible moves and their outcomes, making it challenging to determine the winning strategy without a systematic approach.

## Approach
The algorithm strategy is to use dynamic programming with memoization to solve the problem. The intuition behind this approach is to break down the problem into smaller subproblems, solve each subproblem only once, and store the results to avoid redundant computation. The approach works by iterating over all numbers from 2 to `n`, trying all possible divisors of each number, and determining whether Alice can win by checking the outcome of each possible move. The `dp` array is used to store the result of each subproblem, where `dp[i]` represents whether Alice can win when the current number is `i`. This approach handles the key constraint by ensuring that each player chooses a divisor of the current number in each turn.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n*sqrt(n)) | The outer loop iterates over all numbers from 2 to `n`, and the inner loop tries all possible divisors of each number, which takes O(sqrt(n)) time in the worst case. Therefore, the total time complexity is O(n*sqrt(n)). |
| Space  | O(n) | The `dp` array stores the result of each subproblem, and its size is at most `n+1`, which requires O(n) space. |

## Algorithm Walkthrough
```
Input: n = 4
Step 1: Initialize dp array, dp[1] = false
Step 2: Iterate over all numbers from 2 to n (i = 2)
  - Try all possible divisors of i (j = 1), i % j == 0, !dp[i - j] = !dp[1] = true
  - dp[2] = true
Step 3: Iterate over all numbers from 2 to n (i = 3)
  - Try all possible divisors of i (j = 1), i % j == 0, !dp[i - j] = !dp[2] = false
  - Try all possible divisors of i (j = 3), i % j == 0, !dp[i - j] = !dp[0] = true (assuming dp[0] = false)
  - dp[3] = false
Step 4: Iterate over all numbers from 2 to n (i = 4)
  - Try all possible divisors of i (j = 1), i % j == 0, !dp[i - j] = !dp[3] = true
  - dp[4] = true
Output: dp[n] = dp[4] = true
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n <= 1?"}
    B -->|Yes| C[Return False]
    B -->|No| D[Initialize dp array]
    D --> E[Iterate over all numbers from 2 to n]
    E --> F{Try all possible divisors of i}
    F -->|Found a divisor| G["Update dp[i"]]
    F -->|No divisors found| H[Move to next number]
    G --> E
    H --> I{"Is i == n?"}
    I -->|Yes| J["Return dp[n"]]
    I -->|No| E
```
## Key Insight
> **Tip:** The key to solving this problem is to use dynamic programming to store the results of subproblems and avoid redundant computation.

## Edge Cases
- **Empty/null input**: If the input `n` is not provided or is null, the function will throw an error or return an incorrect result. To handle this case, we need to add input validation to ensure that `n` is a positive integer.
- **Single element**: If `n` is 1, the function will return false, as there are no divisors of 1 that can be used to win the game.
- **Large input**: If `n` is very large, the function may take a long time to compute the result due to the O(n*sqrt(n)) time complexity. To handle this case, we can use a more efficient algorithm or optimize the existing algorithm to reduce its time complexity.

## Common Mistakes
- **Mistake 1**: Not initializing the `dp` array correctly, leading to incorrect results. To avoid this mistake, we need to ensure that the `dp` array is initialized with the correct base case values.
- **Mistake 2**: Not trying all possible divisors of each number, leading to incorrect results. To avoid this mistake, we need to ensure that the inner loop tries all possible divisors of each number.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not rely on the input being sorted, so it will work correctly regardless of the input order.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n) space to store the `dp` array, which is necessary to solve the problem using dynamic programming.
- "What if there are duplicates?" → The algorithm does not handle duplicates explicitly, but it will work correctly even if there are duplicates in the input. However, we may need to add additional logic to handle duplicates if the problem statement requires it.

## CPP Solution

```cpp
// Problem: Divisor Game
// Language: cpp
// Difficulty: Easy
// Time Complexity: O(n) — dynamic programming with memoization
// Space Complexity: O(n) — dp array stores at most n elements
// Approach: Dynamic Programming — for each number, try all possible divisors and determine the best move

class Solution {
public:
    bool divisorGame(int n) {
        // Edge case: n is less than or equal to 1
        if (n <= 1) return false; 

        // Create a dp array to store the result of subproblems
        bool dp[n + 1]; 
        // Base case: if n is 1, Alice cannot make a move
        dp[1] = false; 

        // Iterate over all numbers from 2 to n
        for (int i = 2; i <= n; i++) {
            // Assume Alice will lose
            dp[i] = false; 
            // Try all possible divisors of i
            for (int j = 1; j * j <= i; j++) {
                // If j is a divisor of i and Alice will win after this move
                if (i % j == 0 && !dp[i - j]) {
                    // Then Alice can win
                    dp[i] = true; 
                    // No need to try other divisors
                    break; 
                }
            }
        }

        // Return the result for n
        return dp[n]; 
    }
};
```
