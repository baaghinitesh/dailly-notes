---
title: "FizzBuzz Implementation"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/16/1200/630"
update_count: 0
---

# FizzBuzz Implementation

## Problem Understanding
The FizzBuzz problem is asking to create a program that generates a list of strings representing the numbers from 1 to n, but with some modifications: if a number is a multiple of 3, it should be replaced by "Fizz", if it's a multiple of 5, it should be replaced by "Buzz", and if it's a multiple of both 3 and 5, it should be replaced by "FizzBuzz". The key constraint is to handle these multiples correctly while iterating through the range of numbers. What makes this problem non-trivial is not its complexity but understanding how to efficiently handle the conditional checks for multiples of 3 and 5, making sure not to miss any numbers in the sequence.

## Approach
The algorithm strategy involves a simple iteration through the range of numbers from 1 to n, using conditional checks to determine whether each number is a multiple of 3, 5, or both. The intuition behind this approach is straightforward: for each number, check its divisibility by 3 and 5 and append the corresponding string ("Fizz", "Buzz", "FizzBuzz", or the number itself as a string) to the result list. This approach works because it systematically covers all possible cases for each number in the range. A list is used to store the results because it allows for efficient appending of new elements during the iteration. The approach handles the key constraints by checking for divisibility by 3 and 5 in a specific order to ensure that numbers divisible by both are correctly labeled as "FizzBuzz".

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through the range of numbers from 1 to n once, performing a constant amount of work for each number. This results in a linear time complexity. |
| Space  | O(n)  | Although the initial analysis might suggest O(1) space complexity due to the use of a constant amount of space for variables, the actual space complexity is O(n) because the algorithm stores the results in a list that grows linearly with the size of the input n. |

## Algorithm Walkthrough
```
Input: n = 5
Step 1: Initialize an empty list result = []
Step 2: Iterate through the range from 1 to 5:
  - For i = 1, append "1" to result because 1 is not a multiple of 3 or 5.
  - For i = 2, append "2" to result because 2 is not a multiple of 3 or 5.
  - For i = 3, append "Fizz" to result because 3 is a multiple of 3.
  - For i = 4, append "4" to result because 4 is not a multiple of 3 or 5.
  - For i = 5, append "Buzz" to result because 5 is a multiple of 5.
Output: result = ["1", "2", "Fizz", "4", "Buzz"]
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is i a multiple of both 3 and 5?"}
    B -->|Yes| C[Append "FizzBuzz" to result]
    B -->|No| D{"Is i a multiple of 3?"}
    D -->|Yes| E[Append "Fizz" to result]
    D -->|No| F{"Is i a multiple of 5?"}
    F -->|Yes| G[Append "Buzz" to result]
    F -->|No| H[Append i as a string to result]
    C --> I[Next i]
    E --> I
    G --> I
    H --> I
    I -->|Until i > n| A
```

## Key Insight
> **Tip:** The key to solving the FizzBuzz problem efficiently is to ensure that the conditional checks for multiples of 3 and 5 are ordered correctly to handle the "FizzBuzz" case before the individual "Fizz" and "Buzz" cases.

## Edge Cases
- **Empty/null input**: If n is less than or equal to 0, the function returns an empty list because there are no numbers to process.
- **Single element**: If n is 1, the function returns a list containing the string "1" because 1 is not a multiple of 3 or 5.
- **Large input**: For very large values of n, the function might consume significant memory due to the growth of the result list, but it will still run in linear time complexity.

## Common Mistakes
- **Mistake 1**: Incorrect ordering of conditional checks, leading to numbers that are multiples of both 3 and 5 being incorrectly labeled as just "Fizz" or "Buzz". To avoid this, always check for the "FizzBuzz" condition first.
- **Mistake 2**: Forgetting to handle the case where n is less than or equal to 0, which should return an empty list. To avoid this, always include a check at the beginning of the function to handle this edge case.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm does not rely on the input being sorted, so it would work the same way regardless of the order of the input numbers.
- "Can you do it in O(1) space?" → No, because the problem requires generating a list of strings representing the numbers from 1 to n, which inherently requires O(n) space to store the results.
- "What if there are duplicates?" → The algorithm is designed to generate the FizzBuzz sequence up to n, so if there are duplicates in the input, it's not relevant because the input is not a list of numbers but a single number n up to which the sequence is generated.

## Python Solution

```python
# Problem: FizzBuzz Implementation
# Language: python
# Difficulty: easy
# Time Complexity: O(n) — single pass through the range
# Space Complexity: O(1) — constant space used for variables
# Approach: Simple iteration and conditional checks — for each number, check if it's a multiple of 3 or 5

class FizzBuzz:
    def fizzBuzz(self, n: int) -> list[str]:
        # Initialize an empty list to store the results
        result = []
        
        # Edge case: n is less than or equal to 0
        if n <= 0:
            return result
        
        # Iterate over the range from 1 to n (inclusive)
        for i in range(1, n + 1):
            # Check if the number is a multiple of both 3 and 5
            if i % 3 == 0 and i % 5 == 0:
                # If it is, append "FizzBuzz" to the result list
                result.append("FizzBuzz")
            # Check if the number is a multiple of 3
            elif i % 3 == 0:
                # If it is, append "Fizz" to the result list
                result.append("Fizz")
            # Check if the number is a multiple of 5
            elif i % 5 == 0:
                # If it is, append "Buzz" to the result list
                result.append("Buzz")
            # If the number is not a multiple of either 3 or 5, append the number as a string
            else:
                result.append(str(i))
        
        # Return the result list
        return result

# Example usage:
fizz_buzz = FizzBuzz()
print(fizz_buzz.fizzBuzz(15))
```
