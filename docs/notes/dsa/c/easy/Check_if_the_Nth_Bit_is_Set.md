---
title: "Check if the Nth Bit is Set"
language: "c"
difficulty: "easy"
section: "dsa"
tags: "dsa, c, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/356/1200/630"
update_count: 0
---

# Check if the Nth Bit is Set

## Problem Understanding
The problem asks to determine if the Nth bit of a given integer is set (1) or not (0). The key constraints are that the input integer `num` and the bit position `n` should be valid, where `n` should be greater than 0 and not exceed the number of bits in an integer. This problem is non-trivial because a naive approach might involve converting the integer to a binary string and checking the character at the Nth position, which would be inefficient. The bitwise operation approach is more efficient and accurate.

## Approach
The algorithm strategy is to use a bitwise AND operation to check if the Nth bit is set. The intuition behind this is that the bitwise AND of a number with a mask (created by shifting 1 to the left by `n-1` positions) will result in a non-zero value if the Nth bit is set. This approach works because the bitwise AND operation compares each bit of the first operand to the corresponding bit of the second operand. If both bits are 1, the corresponding result bit is set to 1. Otherwise, the corresponding result bit is set to 0. The data structure used is a simple integer variable, which is sufficient to store the input number and the result.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(1)  | The algorithm performs a constant number of operations, including a bitwise AND operation and a comparison, regardless of the input size. The time complexity is constant because the number of operations does not grow with the input size. |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the input number, the bit position, and the result, regardless of the input size. No additional data structures that scale with the input size are used. |

## Algorithm Walkthrough
```
Input: num = 10 (binary: 1010), n = 2
Step 1: Check if n is valid (n > 0) → n = 2 is valid
Step 2: Check if n is greater than the number of bits in the integer → n = 2 is not greater than 32 bits
Step 3: Create a mask by shifting 1 to the left by n-1 positions → mask = 1 << (2-1) = 2 (binary: 10)
Step 4: Perform bitwise AND operation between num and mask → result = 10 & 2 = 2 (non-zero)
Step 5: Check if the result is non-zero → result = 2 is non-zero
Output: The 2th bit is set
```
This walkthrough demonstrates how the algorithm checks if the 2nd bit of the number 10 is set.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n valid?"}
    B -->|Yes| C{"Is n greater than the number of bits?"}
    C -->|No| D["Create mask by shifting 1 to the left by n-1 positions"]
    D --> E[Perform bitwise AND operation between num and mask]
    E --> F{"Is result non-zero?"}
    F -->|Yes| G[Return "set"]
    F -->|No| H[Return "not set"]
    B -->|No| I["Return -1 (invalid input)"]
    C -->|Yes| I
```
This flowchart illustrates the decision flow of the algorithm, including the checks for valid input and the bitwise AND operation.

## Key Insight
> **Tip:** The key insight is to use a bitwise AND operation with a mask created by shifting 1 to the left by `n-1` positions to check if the Nth bit is set.

## Edge Cases
- **Empty/null input**: This is not applicable to this problem, as the input is an integer and a bit position.
- **Single element**: If the input number is a power of 2 (e.g., 1, 2, 4, 8), the algorithm will correctly identify the set bit.
- **Bit position greater than the number of bits**: The algorithm checks if the bit position is greater than the number of bits in an integer and returns -1 in this case.

## Common Mistakes
- **Mistake 1**: Not checking if the bit position is valid (greater than 0) → To avoid this, add a check at the beginning of the algorithm to return -1 if the bit position is invalid.
- **Mistake 2**: Not using a bitwise AND operation to check if the Nth bit is set → To avoid this, use the bitwise AND operation with a mask created by shifting 1 to the left by `n-1` positions.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → This is not applicable to this problem, as the input is an integer and a bit position.
- "Can you do it in O(1) space?" → Yes, the algorithm already uses O(1) space, as it only uses a constant amount of space to store the input number, the bit position, and the result.
- "What if there are duplicates?" → This is not applicable to this problem, as the input is an integer and a bit position.

## C Solution

```c
// Problem: Check if the Nth Bit is Set
// Language: C
// Difficulty: Easy
// Time Complexity: O(1) — constant time using bitwise operations
// Space Complexity: O(1) — no extra space used
// Approach: Bitwise AND operation — use (1 << (n - 1)) to check if the nth bit is set

#include <stdio.h>

int checkNthBit(int num, int n) {
    // Check if n is valid (should be greater than 0)
    if (n <= 0) { 
        // Edge case: invalid n → return -1
        return -1; 
    }

    // Check if n is greater than the number of bits in the integer
    if (n > sizeof(int) * 8) { 
        // Edge case: n is greater than the number of bits → return -1
        return -1; 
    }

    // Use bitwise AND operation to check if the nth bit is set
    return (num & (1 << (n - 1))) != 0; 
}

int main() {
    int num = 10;  // Binary representation: 1010
    int n = 2;

    int result = checkNthBit(num, n);

    if (result == -1) {
        printf("Invalid input\n");
    } else {
        printf("The %dth bit is %s\n", n, result ? "set" : "not set");
    }

    return 0;
}
```
