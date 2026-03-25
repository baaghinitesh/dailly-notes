---
title: "Climbing Stairs DP"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/811/1200/630"
update_count: 0
---

# Climbing Stairs DP

## Problem Understanding
The problem "Climbing Stairs DP" asks us to find the number of distinct ways to climb a staircase with `n` steps, given that we can either climb one or two steps at a time. The key constraint is that we can only climb one or two steps at a time, and we cannot revisit any steps. This problem becomes non-trivial because a naive approach, such as using recursion without memoization, would lead to exponential time complexity due to the overlapping subproblems. The problem requires us to find an efficient solution that avoids redundant computations.

## Approach
The algorithm strategy used here is Dynamic Programming (DP), where we build a table `dp` to store the number of ways to reach each step from `1` to `n`. The intuition behind this approach is that the number of ways to reach a step `i` depends on the number of ways to reach the previous steps `i-1` and `i-2`, since we can only climb one or two steps at a time. We use a bottom-up approach to fill up the DP table, starting from the base cases `dp[1]` and `dp[2]`. This approach works because it avoids redundant computations by storing the results of subproblems in the DP table.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We make a single pass through the array of size `n` to fill up the DP table, resulting in linear time complexity. |
| Space  | O(n)  | We use a DP table of size `n+1` to store the number of ways to reach each step, resulting in linear space complexity. |

## Algorithm Walkthrough
```
Input: n = 4
Step 1: Initialize DP table with base cases
    dp = [0, 1, 2, 0, 0]  # dp[i] represents the number of ways to reach the i-th step
Step 2: Fill up the DP table
    For i = 3:
        dp[3] = dp[2] + dp[1] = 2 + 1 = 3
    For i = 4:
        dp[4] = dp[3] + dp[2] = 3 + 2 = 5
Output: dp[4] = 5
```
In this example, there are 5 distinct ways to climb a staircase with 4 steps: [1,1,1,1], [1,1,2], [1,2,1], [2,1,1], [2,2].

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Initialize DP table with base cases]
    B --> C[Fill up DP table]
    C --> D[Return dp[n]]
    D --> E[End]
```
This flowchart shows the high-level decision flow of the algorithm.

## Key Insight
> **Tip:** The key insight is that the number of ways to reach a step `i` only depends on the number of ways to reach the previous steps `i-1` and `i-2`, allowing us to use Dynamic Programming to avoid redundant computations.

## Edge Cases
- **Empty/null input**: If `n` is `None` or an empty value, the function should raise an error or return an error message, as it is not a valid input.
- **Single element**: If `n` is 1, the function returns 1, as there is only one way to climb a staircase with one step.
- **Two steps**: If `n` is 2, the function returns 2, as there are two ways to climb a staircase with two steps.

## Common Mistakes
- **Mistake 1**: Not initializing the DP table with base cases, leading to incorrect results.
- **Mistake 2**: Not updating the DP table correctly, leading to incorrect results.

## Interview Follow-ups
> **Interview:** 
- "What if the input is sorted?" → The input `n` is not a sorted array, but a single integer representing the number of steps. However, if we are given a sorted array of step sizes, we can still use Dynamic Programming to solve the problem.
- "Can you do it in O(1) space?" → No, we cannot solve this problem in O(1) space, as we need to store the number of ways to reach each step in the DP table.
- "What if there are duplicates?" → In this problem, duplicates do not matter, as we are counting distinct ways to climb the staircase. However, if we are counting ways to climb a staircase with duplicate steps, we would need to modify the problem statement and the solution accordingly.

## Python Solution

```python
# Problem: Climbing Stairs DP
# Language: python
# Difficulty: Easy
# Time Complexity: O(n) — single pass through array using DP table
# Space Complexity: O(n) — DP table stores at most n elements
# Approach: Dynamic Programming — for each step, calculate the number of ways to reach it

class Solution:
    def climbStairs(self, n: int) -> int:
        # Edge case: n is less than or equal to 2 → return n
        if n <= 2:
            return n
        
        # Initialize DP table with base cases
        dp = [0] * (n + 1)  # dp[i] represents the number of ways to reach the i-th step
        dp[1] = 1  # there is one way to reach the first step (one step)
        dp[2] = 2  # there are two ways to reach the second step (one step + one step or two steps)

        # Fill up the DP table
        for i in range(3, n + 1):  # for each step from 3 to n
            # the number of ways to reach the i-th step is the sum of the number of ways to reach the (i-1)-th and (i-2)-th steps
            dp[i] = dp[i - 1] + dp[i - 2]  # because we can reach the i-th step from either the (i-1)-th or (i-2)-th step

        # return the number of ways to reach the n-th step
        return dp[n]
```
