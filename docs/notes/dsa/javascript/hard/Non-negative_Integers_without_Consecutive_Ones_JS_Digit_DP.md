---
title: "Non-negative Integers without Consecutive Ones JS Digit DP"
language: "javascript"
difficulty: "hard"
section: "dsa"
tags: "dsa, javascript, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/474/1200/630"
update_count: 0
---

# Non-negative Integers without Consecutive Ones JS Digit DP

## Problem Understanding
The problem is asking us to find the number of non-negative integers less than or equal to a given number `n` that do not have consecutive ones in their binary representation. The key constraint is that the integers should not have consecutive ones, which means that the binary representation of the integers should not have two consecutive bits set to 1. This problem is non-trivial because a naive approach would involve generating all possible integers and checking each one for consecutive ones, which would result in a time complexity of O(2^n), making it inefficient for large values of `n`.

## Approach
The algorithm strategy used here is dynamic programming, where we break down the problem into smaller subproblems and store their results in a `dp` array. The intuition behind this approach is that the number of ways to form a binary number of length `i` without consecutive ones is the sum of the number of ways to form a binary number of length `i-1` and the number of ways to form a binary number of length `i-2`. This is because we can append either 0 or 1 to the previous bits to avoid consecutive ones. We use a `dp` array of size 33 to store the results of subproblems, where `dp[i]` represents the number of ways to form a binary number of length `i` without consecutive ones.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | We iterate over the bits of `n` from most significant to least significant, and for each bit, we perform a constant amount of work. The size of the `dp` array is also constant (33), so the overall time complexity is O(n). |
| Space  | O(n)  | We use a `dp` array of size 33 to store the results of subproblems, so the space complexity is O(n). However, since the size of the `dp` array is constant, the space complexity can be considered as O(1) in practice. |

## Algorithm Walkthrough
```javascript
Input: n = 5
Step 1: Initialize dp array: dp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Step 2: Fill dp array using recurrence relation: dp = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 985, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887]
Step 3: Initialize result and current bit position: result = 0, bitPosition = 31
Step 4: Iterate over bits of n: bitPosition = 2 (since 5 is 101 in binary)
Step 5: Check if current bit is 1: (5 & (1 << 2)) !== 0, so result += dp[2] = 3
Step 6: Check if current bit is 1 and previous bit is also 1: (5 & (1 << 2)) !== 0 && (5 & (1 << 1)) !== 0, so return result + dp[1] - 1 = 3 + 2 - 1 = 4
Output: 5
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n 0 or 1?"}
    B -->|Yes| C[Return 1 or 2]
    B -->|No| D[Initialize dp array]
    D --> E[Fill dp array using recurrence relation]
    E --> F[Initialize result and current bit position]
    F --> G{"Is current bit 1?"}
    G -->|Yes| H["Add dp[current bit position"] to result]
    G -->|No| I[Move to next bit position]
    H --> J{"Is current bit 1 and previous bit 1?"}
    J -->|Yes| K["Return result + dp[previous bit position"] - 1]
    J -->|No| I
    I --> L{"Is current bit position 0?"}
    L -->|Yes| M["Return result + 1"]
    L -->|No| G
```
## Key Insight
> **Tip:** The key insight to this problem is that the number of ways to form a binary number of length `i` without consecutive ones is the sum of the number of ways to form a binary number of length `i-1` and the number of ways to form a binary number of length `i-2`, which can be stored in a `dp` array to avoid redundant calculations.

## Edge Cases
- **Empty/null input**: If `n` is null or undefined, the function will throw an error. To handle this, we can add a check at the beginning of the function to return 0 or throw a custom error.
- **Single element**: If `n` is 0 or 1, the function will return 1 or 2, respectively. This is because there is only one way to form 0 (no bits) and two ways to form 1 (either as a single bit or as a number with two bits, 0 and 1).
- **Large input**: If `n` is very large, the function may take a long time to execute or run out of memory. To handle this, we can use a more efficient algorithm or optimize the existing one.

## Common Mistakes
- **Mistake 1**: Not initializing the `dp` array correctly, leading to incorrect results. To avoid this, make sure to initialize the `dp` array with the correct base cases (e.g., `dp[0] = 1` and `dp[1] = 2`).
- **Mistake 2**: Not handling the edge case where `n` is 0 or 1 correctly. To avoid this, make sure to add checks at the beginning of the function to return the correct result for these cases.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The input `n` is not sorted, and the algorithm does not depend on the input being sorted. However, if the input were sorted, the algorithm would still work correctly.
- "Can you do it in O(1) space?" → No, the algorithm uses a `dp` array of size 33 to store the results of subproblems, which requires O(n) space. However, the space complexity can be considered as O(1) in practice since the size of the `dp` array is constant.
- "What if there are duplicates?" → The algorithm does not assume that the input `n` is unique, and it will work correctly even if there are duplicates. However, if there are duplicates, the algorithm may return incorrect results because it is designed to count the number of non-negative integers less than or equal to `n` that do not have consecutive ones in their binary representation.

## Javascript Solution

```javascript
// Problem: Non-negative Integers without Consecutive Ones JS Digit DP
// Language: javascript
// Difficulty: Hard
// Time Complexity: O(n) — using dynamic programming to store results of subproblems
// Space Complexity: O(n) — storing results of subproblems in dp array
// Approach: Dynamic Programming — breaking down problem into smaller subproblems and storing their results

class Solution {
    /**
     * @param {number} n
     * @return {number}
     */
    findIntegers(n) {
        // Initialize dp array to store results of subproblems
        let dp = new Array(33).fill(0);

        // Base cases: there's one way to form 0 (no bits) and 1 (single bit)
        dp[0] = 1;
        dp[1] = 2;

        // Fill dp array using recurrence relation
        for (let i = 2; i <= 32; i++) {
            // For each bit position, consider two cases: 
            // 1. The current bit is 0, in which case we can append either 0 or 1 to the previous bits
            // 2. The current bit is 1, in which case we can only append 0 to the previous bits to avoid consecutive ones
            dp[i] = dp[i - 1] + dp[i - 2];
        }

        // Initialize result and current bit position
        let result = 0;
        let bitPosition = 31;

        // Iterate over bits of n from most significant to least significant
        while (bitPosition >= 0) {
            // If current bit is 1, add number of ways to form number with this bit and all less significant bits set to 0
            if ((n & (1 << bitPosition)) !== 0) {
                result += dp[bitPosition];
            }

            // If current bit is 1 and previous bit is also 1, return -1 because we have consecutive ones
            if (bitPosition > 0 && (n & (1 << bitPosition)) !== 0 && (n & (1 << (bitPosition - 1))) !== 0) {
                return result + dp[bitPosition - 1] - 1; // subtract 1 to exclude the case where all remaining bits are 1
            }

            // Move to next bit position
            bitPosition--;
        }

        // Edge case: n is 0
        if (n === 0) {
            return 1; // there's only one way to form 0
        }

        // Edge case: n is 1
        if (n === 1) {
            return 2; // there are two ways to form 1: either as a single bit or as a number with two bits (0 and 1)
        }

        // Return result
        return result + 1; // add 1 to include the case where all bits are 0
    }
}
```
