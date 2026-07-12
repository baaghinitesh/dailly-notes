---
title: "Climbing Stairs DP"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/722/1200/630"
update_count: 0
---

# Climbing Stairs DP

## Problem Understanding
The problem is asking us to find the number of distinct ways to climb a staircase with n steps, where we can either climb 1 or 2 steps at a time. The key constraint is that we can only climb 1 or 2 steps, and we need to find the total number of ways to reach the nth step. This problem is non-trivial because a naive approach, such as trying all possible combinations of steps, would result in an exponential time complexity due to the overlapping subproblems.

## Approach
The algorithm strategy used here is Dynamic Programming (DP), where we break down the problem into smaller subproblems and store the solutions to these subproblems to avoid redundant computation. The intuition behind this approach is that the number of ways to reach the ith step is the sum of the number of ways to reach the (i-1)th step and the (i-2)th step, since we can either come from the (i-1)th step or the (i-2)th step. We use a DP array to store the number of ways to reach each step, and we fill up this array using the recurrence relation. This approach works because it avoids the overlapping subproblems and has a linear time complexity.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We make a single pass through the array, and for each step, we perform a constant amount of work. The loop iterates from 3 to n, and the operations inside the loop take constant time. |
| Space  | O(n)  | We use a DP array of size n+1 to store the number of ways to reach each step. The space complexity is linear because the size of the DP array grows linearly with the input size n. |

## Algorithm Walkthrough
```
Input: n = 4
Step 1: Initialize DP array with base cases: dp[1] = 1, dp[2] = 2
Step 2: Fill up the DP array using the recurrence relation:
        - dp[3] = dp[2] + dp[1] = 2 + 1 = 3
        - dp[4] = dp[3] + dp[2] = 3 + 2 = 5
Output: dp[4] = 5
```
In this example, the output is 5, which means there are 5 distinct ways to climb a staircase with 4 steps: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, and 2+2.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n == 1?"}
    B -->|Yes| C[Return 1]
    B -->|No| D{"Is n == 2?"}
    D -->|Yes| E[Return 2]
    D -->|No| F[Initialize DP array]
    F --> G[Fill up DP array using recurrence relation]
    G --> H["Return dp[n"]]
```
This flowchart shows the decision flow of the algorithm, including the base cases and the recurrence relation.

## Key Insight
> **Tip:** The key insight is that the number of ways to reach the ith step is the sum of the number of ways to reach the (i-1)th step and the (i-2)th step, which allows us to use Dynamic Programming to solve the problem efficiently.

## Edge Cases
- **Empty/null input**: If the input is null or empty, the algorithm will throw an error, since we cannot climb a staircase with no steps.
- **Single element**: If there is only one step, there is only one way to climb it, which is to take one step.
- **Two steps**: If there are only two steps, there are two ways to climb them: 1+1 or 2.

## Common Mistakes
- **Mistake 1**: Forgetting to handle the base cases (n == 1 and n == 2) correctly, which can lead to incorrect results.
- **Mistake 2**: Using a naive approach that tries all possible combinations of steps, which can result in an exponential time complexity.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The input is not sorted, and we need to find the number of ways to climb a staircase with n steps.
- "Can you do it in O(1) space?" → No, we need to use a DP array to store the number of ways to reach each step, which requires O(n) space.
- "What if there are duplicates?" → The problem statement does not mention duplicates, and we assume that each step is unique.

## CPP Solution

```cpp
// Problem: Climbing Stairs DP
// Language: cpp
// Difficulty: Easy
// Time Complexity: O(n) — single pass through array using DP
// Space Complexity: O(n) — DP array stores at most n elements
// Approach: Dynamic Programming — for each step, calculate the number of ways to reach it

class Solution {
public:
    int climbStairs(int n) {
        // Edge case: if there's only one step, there's only one way to climb it
        if (n == 1) return 1;
        
        // Initialize DP array with base cases
        int dp[n + 1];  // dp[i] represents the number of ways to reach the i-th step
        dp[1] = 1;     // there's one way to reach the first step
        dp[2] = 2;     // there are two ways to reach the second step: 1+1 or 2
        
        // Fill up the DP array using the recurrence relation
        for (int i = 3; i <= n; i++) {
            // for each step, the number of ways to reach it is the sum of the number of ways to reach the previous two steps
            dp[i] = dp[i - 1] + dp[i - 2];  // because we can either come from the (i-1)-th step or the (i-2)-th step
        }
        
        // the answer is the number of ways to reach the n-th step
        return dp[n];
    }
};
```
