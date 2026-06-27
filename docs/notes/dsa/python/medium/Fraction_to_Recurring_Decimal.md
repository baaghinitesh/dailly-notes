---
title: "Fraction to Recurring Decimal"
language: "python"
difficulty: "medium"
section: "dsa"
tags: "dsa, python, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/525/1200/630"
update_count: 0
---

# Fraction to Recurring Decimal

## Problem Understanding
The problem asks us to convert a fraction to a recurring decimal. Given two integers, a numerator and a denominator, we need to return a string representing the decimal representation of the fraction. The key constraints are that we need to handle recurring decimals and that the input integers can be negative. What makes this problem non-trivial is that naive approaches, such as simply dividing the numerator by the denominator, will not work because they do not handle recurring decimals.

## Approach
Our algorithm strategy is to use a hash map to track the remainders we've seen before to detect recurring decimals. This approach works because if we see a remainder that we've seen before, it means that the decimal part of the fraction is recurring. We use a hash map to store the remainders and their corresponding indices in the decimal part of the fraction. We also use a list to store the decimal part of the fraction. Our approach handles the key constraints by checking for negative input integers and handling recurring decimals.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(1)  | Although the time complexity appears to be O(1), it's actually O(log(n)) or O(b) where n is the numerator and b is the number of digits in the denominator, because in the worst-case scenario, we need to iterate through all the digits of the numerator and denominator. However, since the number of digits in the numerator and denominator are limited by the size of an integer in Python, we can consider it as a constant. |
| Space  | O(1)  | Similarly, the space complexity appears to be O(1), but it's actually O(log(n)) or O(b) for the same reason as the time complexity, because we need to store the remainders and their indices in the hash map and the decimal part in the list. |

## Algorithm Walkthrough
```
Input: numerator = 1, denominator = 2
Step 1: result = ["-"] (no, because both are positive), result = ["0"]
Step 2: remainder = 1, result = ["0"], decimal_part = []
Step 3: remainder_map = {1: 0}, decimal_part = ["5"], remainder = 0
Step 4: result = ["0", "."], result = ["0", ".", "5"]
Output: "0.5"

Input: numerator = 1, denominator = 3
Step 1: result = ["0"]
Step 2: remainder = 1, result = ["0"], decimal_part = []
Step 3: remainder_map = {1: 0}, decimal_part = ["3"], remainder = 1
Step 4: remainder_map = {1: 0, 10: 1}, decimal_part = ["3", "3"], remainder = 1
Step 5: Since remainder is already in remainder_map, start_index = 0, decimal_part = ["3", "(", "3", ")"]
Step 6: result = ["0", ".", "3", "(", "3", ")"]
Output: "0.(3)"
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is numerator 0?"}
    B -->|Yes| C[Return "0"]
    B -->|No| D{"Are numerator and denominator negative?"}
    D -->|Yes| E[Add negative sign to result]
    D -->|No| E
    E --> F[Append integer part to result]
    F --> G{"Is remainder 0?"}
    G -->|Yes| H[Return result]
    G -->|No| I[Append decimal point to result]
    I --> J[Track remainders using hash map]
    J --> K{"Is remainder recurring?"}
    K -->|Yes| L[Insert parentheses around recurring part]
    K -->|No| M[Continue tracking remainders]
    L --> N[Return final result]
    M --> J
```

## Key Insight
> **Tip:** The key insight to solving this problem is to use a hash map to track the remainders we've seen before to detect recurring decimals, which allows us to efficiently handle recurring decimals and avoid infinite loops.

## Edge Cases
- **Empty/null input**: This is not a valid input, as we need two integers to represent the numerator and denominator.
- **Single element**: This is not a valid input, as we need two integers to represent the numerator and denominator.
- **Division by zero**: If the denominator is zero, we should raise a ZeroDivisionError, as division by zero is undefined.

## Common Mistakes
- **Mistake 1**: Not handling negative input integers correctly. To avoid this, we need to check if the numerator and denominator are negative and add a negative sign to the result if necessary.
- **Mistake 2**: Not handling recurring decimals correctly. To avoid this, we need to use a hash map to track the remainders we've seen before and insert parentheses around the recurring part when we detect a recurring decimal.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → This is not relevant to this problem, as we are dealing with fractions and decimals.
- "Can you do it in O(1) space?" → No, we cannot do it in O(1) space, as we need to use a hash map to track the remainders we've seen before, which requires O(log(n)) or O(b) space.
- "What if there are duplicates?" → This is not relevant to this problem, as we are dealing with fractions and decimals, and duplicates do not affect the result.

## Python Solution

```python
# Problem: Fraction to Recurring Decimal
# Language: python
# Difficulty: Medium
# Time Complexity: O(1) — because we use a fixed-size hash map to track remainders
# Space Complexity: O(1) — because we use a fixed-size hash map to track remainders
# Approach: HashMap remainder tracking — we use a hash map to track remainders we've seen before to detect recurring decimals

class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        # Edge case: numerator is 0 → return "0"
        if numerator == 0:
            return "0"

        result = []
        # If the result is negative, we need to add a negative sign to the result
        if (numerator < 0) ^ (denominator < 0):
            result.append("-")

        # Convert both numerator and denominator to positive
        numerator, denominator = abs(numerator), abs(denominator)

        # Append the integer part of the fraction to the result
        result.append(str(numerator // denominator))

        # If there is no remainder, we can return the result as is
        remainder = numerator % denominator
        if remainder == 0:
            return "".join(result)

        # Add a decimal point to the result
        result.append(".")

        # Use a hash map to track the remainders we've seen before
        remainder_map = {}
        decimal_part = []

        # While there is still a remainder
        while remainder != 0:
            # If we've seen this remainder before, it means the decimal part is recurring
            if remainder in remainder_map:
                # Find the index where the recurring part starts
                start_index = remainder_map[remainder]
                # Insert parentheses around the recurring part
                decimal_part.insert(start_index, "(")
                decimal_part.append(")")
                break

            # Otherwise, we add the remainder to the hash map and continue
            remainder_map[remainder] = len(decimal_part)
            remainder *= 10
            decimal_part.append(str(remainder // denominator))
            remainder %= denominator

        # Add the decimal part to the result
        result.extend(decimal_part)

        # Return the final result
        return "".join(result)
```
