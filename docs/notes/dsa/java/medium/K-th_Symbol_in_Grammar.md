---
title: "K-th Symbol in Grammar"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/964/1200/630"
update_count: 0
---

# K-th Symbol in Grammar

## Problem Understanding
The problem asks for the K-th symbol in the N-th row of a specific grammar sequence, where each row is constructed based on the previous one. The key constraint is that the sequence is generated recursively, and the value of each symbol depends on its position in the row. The problem is non-trivial because a naive approach would require generating the entire sequence up to the N-th row, which would be inefficient. The recursive nature of the sequence and the dependence of each symbol on its position make it challenging to find a direct formula for the K-th symbol.

## Approach
The algorithm strategy is to use recursive construction of the grammar sequence, building each row based on the previous one. The intuition behind this approach is that the value of each symbol in the current row can be determined by looking at the corresponding position in the previous row. If the position is in the first half of the row, the value is the same as in the previous row; otherwise, it is the opposite of the value in the previous row. This approach works because the sequence is generated recursively, and each row is constructed based on the previous one. The recursive function uses integer parameters to keep track of the current row and position, making it efficient to calculate the K-th symbol.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The time complexity is O(n) because the recursive function makes at most n recursive calls, each of which takes constant time. The maximum recursion depth is n, which occurs when k is in the second half of each row. |
| Space  | O(n)  | The space complexity is O(n) because the maximum recursion depth is n, and each recursive call adds a layer to the call stack. Additionally, the recursive function uses a constant amount of space to store the parameters and local variables. |

## Algorithm Walkthrough
```
Input: n = 3, k = 2
Step 1: Check if n is 1 (base case) → no, proceed to calculate length
Step 2: Calculate length = 1 << (n - 1) = 1 << (3 - 1) = 2
Step 3: Check if k is in the first half of the row → no, k = 2 is in the second half
Step 4: Recursive call to get the value from the previous row: kthGrammar(2, 2 - 2 / 2) = kthGrammar(2, 1)
Step 5: Calculate the value for the previous row: kthGrammar(2, 1) → check if n is 1 → no, proceed to calculate length
Step 6: Calculate length = 1 << (2 - 1) = 1
Step 7: Check if k is in the first half of the row → yes, k = 1 is in the first half
Step 8: Recursive call to get the value from the previous row: kthGrammar(1, 1) → base case, return 0
Step 9: Return the value from the previous row: 0
Step 10: Flip the value because k is in the second half of the row: 1 - 0 = 1
Output: 1
```
This walkthrough demonstrates how the recursive function constructs the grammar sequence and calculates the K-th symbol.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n = 1?"}
    B -->|Yes| C[Return 0]
    B -->|No| D{"Is k <= length / 2?"}
    D -->|Yes| E["Recursive call: kthGrammar("n - 1, k")"]
    D -->|No| F["Recursive call: kthGrammar("n - 1, k - length / 2")"]
    F --> G["Flip the value: 1 - result"]
    E --> H[Return result]
    G --> H
```
This flowchart illustrates the decision flow of the recursive function, showing how it handles the base case and the recursive calls.

## Key Insight
> **Tip:** The key insight is that the value of each symbol in the current row can be determined by looking at the corresponding position in the previous row, allowing for an efficient recursive construction of the grammar sequence.

## Edge Cases
- **Empty/null input**: Not applicable, as the input is guaranteed to be non-empty and valid.
- **Single element**: If n = 1, the function returns 0, as there is only one symbol in the first row.
- **K = 1 or k = 2^(n-1)**: These are boundary cases where k is at the start or end of the row. The function handles these cases correctly by checking if k is in the first half of the row and making the necessary recursive calls.

## Common Mistakes
- **Mistake 1**: Not handling the base case correctly, leading to infinite recursion. To avoid this, make sure to check if n is 1 and return 0 immediately.
- **Mistake 2**: Not flipping the value when k is in the second half of the row. To avoid this, make sure to subtract k - length / 2 from the result of the recursive call and flip the value using 1 - result.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The input is not sorted, and the sequence is generated recursively. However, if the input were sorted, the function would still work correctly, as it only depends on the position of k in the row.
- "Can you do it in O(1) space?" → No, the function requires O(n) space due to the recursive calls and the maximum recursion depth.
- "What if there are duplicates?" → The sequence is generated recursively, and each symbol is determined by its position in the row. If there are duplicates, the function will still work correctly, as it only depends on the position of k in the row.

## Java Solution

```java
// Problem: K-th Symbol in Grammar
// Language: Java
// Difficulty: Medium
// Time Complexity: O(n) — recursive calls up to n levels deep
// Space Complexity: O(n) — maximum recursion depth and string concatenation
// Approach: Recursive construction of the grammar sequence — build each row based on the previous one

public class Solution {
    public int kthGrammar(int n, int k) {
        // Base case: first row of the sequence (just "0")
        if (n == 1) return 0;
        
        // Calculate the length of the current row (2^(n-1))
        int length = 1 << (n - 1);
        
        // If k is in the first half of the row, its value is the same as the corresponding position in the previous row
        if (k <= length / 2) {
            // Recursive call to get the value from the previous row
            return kthGrammar(n - 1, k);
        } else {
            // If k is in the second half of the row, its value is the opposite of the corresponding position in the previous row
            // Recursive call to get the value from the previous row and flip it
            return 1 - kthGrammar(n - 1, k - length / 2);
        }
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.kthGrammar(1, 1));  // Edge case: n = 1 → return 0
        System.out.println(solution.kthGrammar(2, 1));  // Edge case: k = 1 → return 0
        System.out.println(solution.kthGrammar(2, 2));  // Edge case: k = 2 → return 1
        System.out.println(solution.kthGrammar(3, 1));  // Example usage: n = 3, k = 1 → return 0
        System.out.println(solution.kthGrammar(3, 2));  // Example usage: n = 3, k = 2 → return 1
        System.out.println(solution.kthGrammar(4, 5));  // Example usage: n = 4, k = 5 → return 1
    }
}
```
