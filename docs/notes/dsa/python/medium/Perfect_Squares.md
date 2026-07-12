---
title: "Perfect Squares"
language: "python"
difficulty: "medium"
section: "dsa"
tags: "dsa, python, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/993/1200/630"
update_count: 0
---

# Perfect Squares

## Problem Understanding
The problem is asking for the minimum number of perfect squares that sum up to a given integer `n`. The key constraint is that the numbers must be perfect squares, and the objective is to find the least number of such squares. This problem is non-trivial because a naive approach, such as trying all possible combinations of perfect squares, would be computationally expensive and inefficient. The dynamic programming approach is used to build up a solution by breaking down the problem into smaller sub-problems and storing the results to avoid redundant calculations.

## Approach
The algorithm strategy used here is dynamic programming with a nested loop structure, where the outer loop iterates over all numbers from 1 to `n`, and the inner loop iterates over all perfect squares that are less than or equal to the current number `i`. The intuition behind this approach is to build up a solution by considering all possible perfect squares that can sum up to `i` and storing the minimum number of such squares in a dynamic programming array `dp`. The `dp` array is used to store the minimum number of perfect squares for each number up to `n`, and it is updated iteratively using the inner loop. The approach handles the key constraint of using only perfect squares by only considering perfect squares in the inner loop.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n*sqrt(n)) | The time complexity is O(n*sqrt(n)) because the outer loop runs from 1 to n (O(n)) and the inner loop runs up to the square root of the current number i (O(sqrt(n))). The total number of iterations is proportional to the product of these two loops. |
| Space  | O(n) | The space complexity is O(n) because the dynamic programming array `dp` stores n elements, one for each number up to n. |

## Algorithm Walkthrough
```
Input: n = 12
Step 1: Initialize dp array with infinity for all values
    dp = [0, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
Step 2: Iterate over all numbers from 1 to n
    i = 1, j = 1
    dp[1] = min(inf, 1 + dp[0]) = 1
    dp = [0, 1, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
Step 3: i = 2, j = 1
    dp[2] = min(inf, 1 + dp[1]) = 2
    dp = [0, 1, 2, inf, inf, inf, inf, inf, inf, inf, inf, inf, inf]
Step 4: i = 3, j = 1
    dp[3] = min(inf, 1 + dp[2]) = 3
    dp = [0, 1, 2, 3, inf, inf, inf, inf, inf, inf, inf, inf, inf]
Step 5: i = 4, j = 1, 2
    dp[4] = min(inf, 1 + dp[3]) = 1 + dp[0] = 1
    dp = [0, 1, 2, 3, 1, inf, inf, inf, inf, inf, inf, inf, inf]
...
Output: dp[n] = dp[12] = 3 (because 12 = 4 + 4 + 4)
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize dp array}
    B --> C[Iterate over numbers from 1 to n]
    C --> D{"Is j^2 <= i?"}
    D -->|Yes| E["Update dp[i"] with minimum]
    D -->|No| F[Move to next i]
    E --> D
    F --> C
    C -->|End of iteration| G["Return dp[n"]]
```
## Key Insight
> **Tip:** The key insight is to use dynamic programming to build up a solution by breaking down the problem into smaller sub-problems and storing the results to avoid redundant calculations, which reduces the time complexity from exponential to O(n*sqrt(n)).

## Edge Cases
- **Empty/null input**: If the input `n` is empty or null, the function will throw an error because it expects an integer as input.
- **Single element**: If the input `n` is 1, the function will return 1 because 1 is a perfect square.
- **Perfect square**: If the input `n` is a perfect square (e.g., 4, 9, 16), the function will return 1 because `n` can be represented as a single perfect square.

## Common Mistakes
- **Mistake 1**: Not initializing the `dp` array with infinity for all values, which can lead to incorrect results.
- **Mistake 2**: Not updating the `dp` array correctly in the inner loop, which can also lead to incorrect results.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The input is not sorted, and the algorithm does not rely on the input being sorted.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n) space to store the dynamic programming array `dp`.
- "What if there are duplicates?" → The algorithm does not handle duplicates explicitly, but it will still return the correct result because it uses the minimum number of perfect squares to represent each number up to `n`.

## Python Solution

```python
# Problem: Perfect Squares
# Language: python
# Difficulty: Medium
# Time Complexity: O(n*sqrt(n)) — dynamic programming with nested loops
# Space Complexity: O(n) — dynamic programming array stores n elements
# Approach: Dynamic Programming with BFS — build up minimum number of perfect squares for each number up to n

class Solution:
    def numSquares(self, n: int) -> int:
        # Initialize dynamic programming array with infinity for all values
        dp = [float('inf')] * (n + 1)  # dp[i] stores minimum number of perfect squares that sum up to i
        dp[0] = 0  # Base case: 0 can be represented as sum of 0 perfect squares

        # Iterate over all numbers from 1 to n
        for i in range(1, n + 1):
            j = 1  # Start from smallest perfect square (1^2)
            # Iterate over all perfect squares that are less than or equal to i
            while j * j <= i:
                # Update dp[i] with minimum of current value and 1 plus minimum number of perfect squares for i - j^2
                dp[i] = min(dp[i], 1 + dp[i - j * j])  # Update dp[i] if a smaller representation is found
                j += 1  # Move to next perfect square

        # Edge case: if n is not a perfect square, return minimum number of perfect squares that sum up to n
        return dp[n] if dp[n] != float('inf') else -1  # Return -1 if no representation is found
```
