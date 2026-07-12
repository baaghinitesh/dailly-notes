---
title: "Counting Bits"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/383/1200/630"
update_count: 0
---

# Counting Bits

## Problem Understanding
The problem of counting bits involves calculating the number of bits set (i.e., equal to 1) in the binary representation of each number from 0 to a given number n. The key constraint is to find an efficient approach that can handle large values of n. A naive approach would be to convert each number to binary and count the bits, but this would be inefficient for large n. The problem becomes non-trivial because a straightforward approach would result in a high time complexity, making it impractical for large inputs.

## Approach
The algorithm strategy used here is dynamic programming with bitwise operations. The intuition behind this approach is to calculate the bit count of each number based on its predecessor. This is achieved by using the bitwise right shift operator (>>), which effectively divides the number by 2, and the bitwise AND operator (&), which checks if a number is odd. If a number is even, it has the same bit count as its predecessor divided by 2. If a number is odd, it has one more bit than its predecessor. This approach works because the binary representation of a number is closely related to its predecessor, allowing for an efficient calculation of bit counts. The data structure used is an array to store the bit counts of numbers from 0 to n.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm makes a single pass through numbers from 0 to n, performing a constant amount of work for each number. The bitwise operations (right shift and AND) take constant time. |
| Space  | O(n)  | The algorithm uses an array of size n + 1 to store the bit counts of numbers from 0 to n. This requires linear space proportional to the input size n. |

## Algorithm Walkthrough
```
Input: n = 5
Step 1: Initialize result array with size n + 1 = 6
        result = [0, 0, 0, 0, 0, 0]
Step 2: Base case - result[0] = 0 (since 0 has 0 bits)
        result = [0, 0, 0, 0, 0, 0]
Step 3: Calculate bit count for i = 1
        result[1] = result[1 >> 1] + (1 & 1) = result[0] + 1 = 0 + 1 = 1
        result = [0, 1, 0, 0, 0, 0]
Step 4: Calculate bit count for i = 2
        result[2] = result[2 >> 1] + (2 & 1) = result[1] + 0 = 1 + 0 = 1
        result = [0, 1, 1, 0, 0, 0]
Step 5: Calculate bit count for i = 3
        result[3] = result[3 >> 1] + (3 & 1) = result[1] + 1 = 1 + 1 = 2
        result = [0, 1, 1, 2, 0, 0]
Step 6: Calculate bit count for i = 4
        result[4] = result[4 >> 1] + (4 & 1) = result[2] + 0 = 1 + 0 = 1
        result = [0, 1, 1, 2, 1, 0]
Step 7: Calculate bit count for i = 5
        result[5] = result[5 >> 1] + (5 & 1) = result[2] + 1 = 1 + 1 = 2
        result = [0, 1, 1, 2, 1, 2]
Output: result = [0, 1, 1, 2, 1, 2]
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Initialize result array]
    B --> C["Base case: result[0"] = 0]
    C --> D[Loop through numbers from 1 to n]
    D --> E{"Is i even?"}
    E -->|Yes| F["result[i"] = result["i / 2"]]
    E -->|No| G["result[i"] = result["(i - 1) / 2"] + 1]
    F --> D
    G --> D
    D --> H[Return result array]
```
## Key Insight
> **Tip:** The key insight here is to recognize that the binary representation of a number is closely related to its predecessor, allowing for an efficient calculation of bit counts using bitwise operations.

## Edge Cases
- **Empty/null input**: If the input n is null or empty, the function will throw an exception or return an error, as it expects a valid integer input.
- **Single element**: If n is 0, the function returns an array with a single element, [0], since 0 has 0 bits.
- **Large input**: For very large inputs, the function may consume more memory due to the size of the result array, but the time complexity remains linear, making it efficient for large inputs.

## Common Mistakes
- **Mistake 1**: Not handling the base case correctly, leading to incorrect results for small inputs.
- **Mistake 2**: Not using bitwise operations efficiently, resulting in slower performance.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, as it only depends on the binary representation of each number, not the order of the input.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n) space to store the result array, as it needs to store the bit counts for all numbers from 0 to n.
- "What if there are duplicates?" → The algorithm can be modified to handle duplicates by using a HashMap to store the bit counts of unique numbers, but this would require additional space and complexity.

## Java Solution

```java
// Problem: Counting Bits
// Language: Java
// Difficulty: Medium
// Time Complexity: O(n) — single pass through numbers from 0 to n
// Space Complexity: O(n) — array stores counts of bits for numbers from 0 to n
// Approach: Dynamic programming with bitwise operations — for each number, calculate bit count based on its predecessor

public class Solution {
    public int[] countBits(int n) {
        // Initialize result array with size n + 1
        int[] result = new int[n + 1];
        
        // Base case: 0 has 0 bits
        result[0] = 0;
        
        // Edge case: if n is 0, return result immediately
        if (n == 0) return result;
        
        // Iterate over numbers from 1 to n
        for (int i = 1; i <= n; i++) {
            // Calculate bit count of i based on its predecessor (i - 1) and whether i is even or odd
            // If i is even, it has the same bit count as i / 2
            // If i is odd, it has one more bit than i - 1
            result[i] = result[i >> 1] + (i & 1);
        }
        
        return result;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        int n = 5;
        int[] result = solution.countBits(n);
        // Print result
        for (int i = 0; i <= n; i++) {
            System.out.println("Number of bits in " + i + ": " + result[i]);
        }
    }
}
```
