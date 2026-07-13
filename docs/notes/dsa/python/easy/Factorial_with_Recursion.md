---
title: "Factorial with Recursion"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/639/1200/630"
update_count: 0
---

# Factorial with Recursion

## Problem Understanding
The problem asks us to calculate the factorial of a given integer using recursion. The factorial of a number `n`, denoted as `n!`, is the product of all positive integers less than or equal to `n`. The key constraint is that the input `n` can be any integer, and we need to handle edge cases such as negative numbers and zero. What makes this problem non-trivial is that a naive approach would involve iterating from `1` to `n` and multiplying all numbers, but using recursion allows us to break down the problem into smaller sub-problems and solve them efficiently. However, a naive recursive approach without proper base cases can lead to a stack overflow for large inputs.

## Approach
Our approach involves using a recursive function to calculate the factorial of a given number `n`. The key idea is to break down the problem into smaller sub-problems by using the recursive formula `n! = n * (n-1)!`. We use a base case to handle the termination condition, where the factorial of `0` or `1` is defined as `1`. We also handle the edge case where `n` is negative by returning an error value. The recursive case involves calling the `factorial` function with the argument `n-1` and multiplying the result by `n`. We use a recursive call stack to store the intermediate results, which allows us to efficiently calculate the factorial of large numbers.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The time complexity is O(n) because we make a recursive call for each number up to n, resulting in a linear number of operations. The recursive call stack can grow up to n levels deep, but each level performs a constant amount of work. |
| Space  | O(n)  | The space complexity is O(n) because the recursive call stack can grow up to n levels deep, storing the intermediate results and function call information. This means that the memory usage increases linearly with the size of the input. |

## Algorithm Walkthrough
```
Input: n = 5
Step 1: factorial(5) = 5 * factorial(4)
Step 2: factorial(4) = 4 * factorial(3)
Step 3: factorial(3) = 3 * factorial(2)
Step 4: factorial(2) = 2 * factorial(1)
Step 5: factorial(1) = 1 (base case)
Step 6: factorial(2) = 2 * 1 = 2
Step 7: factorial(3) = 3 * 2 = 6
Step 8: factorial(4) = 4 * 6 = 24
Step 9: factorial(5) = 5 * 24 = 120
Output: 120
```
This example demonstrates how the recursive function breaks down the problem into smaller sub-problems and solves them efficiently.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n 0 or 1?"}
    B -->|Yes| C[Return 1]
    B -->|No| D{"Is n negative?"}
    D -->|Yes| E["Return -1"]
    D -->|No| F["Call factorial("n-1")"]
    F --> G[Multiply n by result]
    G --> H[Return result]
```
This flowchart illustrates the decision flow and data transformation involved in the recursive function.

## Key Insight
> **Tip:** The key insight is to recognize that the factorial of a number `n` can be broken down into smaller sub-problems using the recursive formula `n! = n * (n-1)!`, allowing for efficient calculation and termination using a base case.

## Edge Cases
- **Empty/null input**: Not applicable, as the input is an integer.
- **Single element**: If `n` is `0` or `1`, the function returns `1`, which is the base case.
- **Negative input**: If `n` is negative, the function returns `-1`, indicating that the factorial is not defined for negative numbers.

## Common Mistakes
- **Mistake 1**: Forgetting to handle the base case, leading to a stack overflow or incorrect results. To avoid this, ensure that the base case is properly defined and handled.
- **Mistake 2**: Not handling negative input correctly, leading to incorrect results or a stack overflow. To avoid this, add a check for negative input and return an error value or handle it accordingly.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → This does not affect the recursive function, as it only depends on the value of `n`.
- "Can you do it in O(1) space?" → No, the recursive function requires O(n) space due to the recursive call stack.
- "What if there are duplicates?" → This does not affect the recursive function, as it only calculates the factorial of a single number `n`.

## Python Solution

```python
# Problem: Factorial with Recursion
# Language: python
# Difficulty: Easy
# Time Complexity: O(n) — recursive call for each number up to n
# Space Complexity: O(n) — recursive call stack can go up to n
# Approach: Recursive multiplication — n! = n * (n-1)!

class Solution:
    def factorial(self, n: int) -> int:
        # Base case: factorial of 0 or 1 is 1
        if n == 0 or n == 1:
            return 1
        
        # Edge case: negative input → return -1
        if n < 0:
            return -1  # Factorial is not defined for negative numbers
        
        # Recursive case: n! = n * (n-1)!
        return n * self.factorial(n-1)  # Call factorial recursively with n-1

# Example usage:
solution = Solution()
print(solution.factorial(5))  # Output: 120
```
