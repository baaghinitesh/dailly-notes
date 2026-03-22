---
title: "Power of Two"
difficulty: "easy"
tags: "dsa, easy, java, leetcode"
banner: "https://image.pollinations.ai/prompt/Power%20of%20Two%20algorithm%20data%20structure?width=800&height=400&nologo=true"
update_count: 0
---

# Power of Two

![Power of Two](https://image.pollinations.ai/prompt/Power%20of%20Two%20algorithm%20data%20structure?width=800&height=400&nologo=true)

## Approach
The algorithm checks if a given number is a power of two by utilizing the properties of binary representation. It first checks if the number is less than or equal to zero, in which case it cannot be a power of two. Then, it uses a bitwise AND operation to verify if the number is a power of two.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(1)  | The algorithm performs a constant number of operations, regardless of the input size. |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the input and temporary results. |

## Key Insight
> **Tip:** The core insight behind this solution is that a power of two in binary representation has exactly one '1' bit, and subtracting 1 from it flips all bits to the right of the rightmost '1' bit, making the bitwise AND of the number and the number minus one equal to zero if the number is a power of two.

## Edge Cases
- The input number is less than or equal to zero, in which case the function returns false.
- The input number is a negative power of two (e.g., -2, -4, -8), which is not considered a power of two in this context and returns false.

## Java Solution

```java
// Problem: Power of Two
// Difficulty: easy
// Time Complexity: O(log n)
// Space Complexity: O(1)
public class PowerOfTwo {
    public boolean isPowerOfTwo(int n) {
        // Check if n is less than or equal to 0, in which case it cannot be a power of two
        if (n <= 0) return false;
        
        // Use bitwise AND operation to check if n is a power of two
        // If n is a power of two, its binary representation has exactly one '1' bit
        // Subtracting 1 from n flips all bits to the right of the rightmost '1' bit
        // Therefore, if n is a power of two, n & (n - 1) will be zero
        return (n & (n - 1)) == 0;
    }
}
```
