---
title: "Unique Binary Search Trees Catalan Numbers"
language: "cpp"
difficulty: "medium"
section: "dsa"
tags: "dsa, cpp, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/40/1200/630"
update_count: 0
---

# Unique Binary Search Trees Catalan Numbers

## Problem Understanding
The problem asks us to find the number of unique binary search trees that can be constructed from a sequence of numbers from 1 to n. The key constraint is that each tree must be a binary search tree, meaning that for any given node, all elements in the left subtree must be less than the node, and all elements in the right subtree must be greater than the node. This problem is non-trivial because the number of possible trees grows rapidly with the size of the input, and a naive approach would involve generating all possible trees and checking if they are valid binary search trees.

## Approach
The algorithm strategy used here is dynamic programming, where we build up the solution iteratively by computing the Catalan numbers. The intuition behind this approach is that the number of unique binary search trees for a given size n can be computed by summing the products of smaller Catalan numbers. We use an array to store the Catalan numbers, and we initialize the base cases where the number of unique trees for sizes 0 and 1 is 1. We then compute the Catalan numbers iteratively using two nested loops, where the outer loop iterates over the size of the trees, and the inner loop iterates over the possible root nodes of the trees.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n^2) | The algorithm has two nested loops, where the outer loop runs from 2 to n, and the inner loop runs from 0 to i-1. The total number of iterations is therefore proportional to the sum of the first n-1 integers, which is n*(n-1)/2, resulting in a time complexity of O(n^2). |
| Space  | O(n) | The algorithm uses an array of size n+1 to store the Catalan numbers, resulting in a space complexity of O(n). |

## Algorithm Walkthrough
```
Input: n = 4
Step 1: Initialize catalanNumbers array with size n+1 = 5
         catalanNumbers = [0, 0, 0, 0, 0]
Step 2: Set base cases catalanNumbers[0] = catalanNumbers[1] = 1
         catalanNumbers = [1, 1, 0, 0, 0]
Step 3: Compute catalanNumbers[2]
         catalanNumbers[2] = catalanNumbers[0] * catalanNumbers[1] + catalanNumbers[1] * catalanNumbers[0] = 2
         catalanNumbers = [1, 1, 2, 0, 0]
Step 4: Compute catalanNumbers[3]
         catalanNumbers[3] = catalanNumbers[0] * catalanNumbers[2] + catalanNumbers[1] * catalanNumbers[1] + catalanNumbers[2] * catalanNumbers[0] = 5
         catalanNumbers = [1, 1, 2, 5, 0]
Step 5: Compute catalanNumbers[4]
         catalanNumbers[4] = catalanNumbers[0] * catalanNumbers[3] + catalanNumbers[1] * catalanNumbers[2] + catalanNumbers[2] * catalanNumbers[1] + catalanNumbers[3] * catalanNumbers[0] = 14
         catalanNumbers = [1, 1, 2, 5, 14]
Output: catalanNumbers[4] = 14
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is n <= 1?"}
    B -->|Yes| C[Return 1]
    B -->|No| D[Initialize catalanNumbers array]
    D --> E[Compute catalanNumbers iteratively]
    E --> F{"Is i <= n?"}
    F -->|Yes| G["Compute catalanNumbers[i"]]
    G --> F
    F -->|No| H["Return catalanNumbers[n"]]
```
## Key Insight
> **Tip:** The key insight is that the number of unique binary search trees for a given size n can be computed by summing the products of smaller Catalan numbers, which can be done iteratively using dynamic programming.

## Edge Cases
- **Empty input (n = 0)**: The function returns 1, because there is only one way to construct an empty binary search tree.
- **Single element (n = 1)**: The function returns 1, because there is only one way to construct a binary search tree with one element.
- **Large input (n > 10)**: The function may take a long time to compute the result, because the time complexity is O(n^2). However, the function will still return the correct result.

## Common Mistakes
- **Mistake 1: Not initializing the base cases correctly**: If the base cases are not initialized correctly, the function will not compute the correct Catalan numbers.
- **Mistake 2: Not using dynamic programming**: If the function does not use dynamic programming, it will have a high time complexity and may not be able to handle large inputs.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The function will still return the correct result, because the function does not assume that the input is sorted.
- "Can you do it in O(1) space?" → No, the function cannot be done in O(1) space, because it needs to store the Catalan numbers in an array.
- "What if there are duplicates?" → The function will still return the correct result, because it does not assume that the input is unique.

## CPP Solution

```cpp
// Problem: Unique Binary Search Trees Catalan Numbers
// Language: cpp
// Difficulty: Medium
// Time Complexity: O(n^2) — two nested loops to compute Catalan numbers
// Space Complexity: O(n) — array to store Catalan numbers
// Approach: Dynamic Programming — build up Catalan numbers iteratively

class Solution {
public:
    int numTrees(int n) {
        // Edge case: n is 0 or 1 → return 1
        if (n <= 1) return 1;
        
        // Initialize array to store Catalan numbers
        int catalanNumbers[n + 1];
        
        // Base cases: C(0) = C(1) = 1
        catalanNumbers[0] = catalanNumbers[1] = 1;
        
        // Compute Catalan numbers iteratively
        for (int i = 2; i <= n; i++) {
            // For each i, compute the sum of products of smaller Catalan numbers
            catalanNumbers[i] = 0;
            for (int j = 0; j < i; j++) {
                // For each j, add the product of C(j) and C(i - j - 1) to the sum
                catalanNumbers[i] += catalanNumbers[j] * catalanNumbers[i - j - 1];
            }
        }
        
        // Return the nth Catalan number
        return catalanNumbers[n];
    }
};
```
