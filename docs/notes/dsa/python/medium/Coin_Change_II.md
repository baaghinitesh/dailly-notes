---
title: "Coin Change II"
language: "python"
difficulty: "medium"
section: "dsa"
tags: "dsa, python, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/99/1200/630"
update_count: 0
---

# Coin Change II

## Problem Understanding
The Coin Change II problem asks us to find the number of combinations that sum up to a given amount using a set of coins with different denominations. The key constraint is that each coin can be used any number of times, and the order of the coins does not matter. This problem is non-trivial because a naive approach, such as trying all possible combinations, would result in exponential time complexity due to the repeated computation of the same subproblems.

## Approach
The algorithm strategy used to solve this problem is dynamic programming. The intuition behind this approach is to break down the problem into smaller subproblems, where each subproblem represents finding the number of combinations for a smaller amount. We use a dynamic programming (DP) array, `dp`, where `dp[i]` represents the number of combinations for amount `i`. We iterate through each coin and update the DP array accordingly. This approach works because it avoids the repeated computation of the same subproblems, reducing the time complexity to O(amount * len(coins)).

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(amount * len(coins)) | We have two nested loops: one for each coin and one for each amount from the coin's value to the target amount. The number of iterations is proportional to the product of the number of coins and the target amount. |
| Space  | O(amount) | We use a DP array of size `amount + 1` to store the number of combinations for each amount. The space complexity is linear with respect to the target amount. |

## Algorithm Walkthrough
```
Input: amount = 5, coins = [1, 2, 5]
Step 1: Initialize dp array with zeros: dp = [0, 0, 0, 0, 0, 0]
Step 2: Set dp[0] = 1 (base case: one way to make 0 amount)
Step 3: For coin = 1, update dp array:
  - dp[1] += dp[0] = 1
  - dp[2] += dp[1] = 1
  - dp[3] += dp[2] = 1
  - dp[4] += dp[3] = 1
  - dp[5] += dp[4] = 1
Step 4: For coin = 2, update dp array:
  - dp[2] += dp[0] = 2
  - dp[3] += dp[1] = 2
  - dp[4] += dp[2] = 3
  - dp[5] += dp[3] = 4
Step 5: For coin = 5, update dp array:
  - dp[5] += dp[0] = 5
Output: dp[5] = 5 (number of combinations for amount 5)
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize dp array}
    B --> C["Set dp[0"] = 1]
    C --> D{For each coin}
    D -->|Yes| E[Update dp array]
    E --> D
    D -->|No| F["Return dp[amount"]]
    F --> G[End]
```
## Key Insight
> **Tip:** The key insight is to use dynamic programming to avoid repeated computation of the same subproblems, reducing the time complexity from exponential to O(amount * len(coins)).

## Edge Cases
- **Empty/null input**: If the input amount is 0, the function returns 1 (one way to make 0 amount: using no coins). If the input coins array is empty, the function returns 0 (no way to make a positive amount without coins).
- **Single element**: If there is only one coin, the function returns 1 if the amount is a multiple of the coin's value, and 0 otherwise.
- **Negative amount**: If the input amount is negative, the function returns 0 (no way to make a negative amount).

## Common Mistakes
- **Mistake 1**: Not initializing the DP array correctly, leading to incorrect results. To avoid this, make sure to initialize the DP array with zeros and set the base case `dp[0] = 1`.
- **Mistake 2**: Not updating the DP array correctly, leading to incorrect results. To avoid this, make sure to update the DP array using the correct recurrence relation: `dp[i] += dp[i - coin]`.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not rely on the input being sorted, so the time complexity remains the same.
- "Can you do it in O(1) space?" → No, because we need to store the DP array to avoid repeated computation of the same subproblems.
- "What if there are duplicates?" → The algorithm treats duplicate coins as separate coins, so the time complexity remains the same. However, we can optimize the algorithm to ignore duplicates by using a set to store unique coins.

## Python Solution

```python
# Problem: Coin Change II
# Language: python
# Difficulty: Medium
# Time Complexity: O(amount * len(coins)) — two nested loops for dynamic programming
# Space Complexity: O(amount) — dp array stores at most amount elements
# Approach: Dynamic programming — for each amount, calculate the number of combinations using each coin

class Solution:
    def change(self, amount: int, coins: list[int]) -> int:
        # Initialize dp array with zeros, dp[i] represents the number of combinations for amount i
        dp = [0] * (amount + 1)  
        # Base case: there is one way to make 0 amount (using no coins)
        dp[0] = 1  

        # For each coin
        for coin in coins:
            # For each amount from coin to the target amount
            for i in range(coin, amount + 1):
                # Update dp[i] by adding the number of combinations for amount i - coin
                dp[i] += dp[i - coin]  # dp[i - coin] represents the number of combinations without using the current coin

        # Edge case: amount is 0 → return 1 (one way to make 0 amount: using no coins)
        # Edge case: amount is negative or coins is empty → return 0 (no way to make a negative amount or without coins)
        return dp[amount]  # return the number of combinations for the target amount
```
