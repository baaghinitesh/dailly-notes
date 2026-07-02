---
title: "Assign Cookies"
language: "java"
difficulty: "easy"
section: "dsa"
tags: "dsa, java, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/192/1200/630"
update_count: 0
---

# Assign Cookies

## Problem Understanding
The problem "Assign Cookies" is asking to find the maximum number of children that can be satisfied with a given set of cookies, where each child has a certain satisfaction level and each cookie has a certain size. The key constraint is that a child can only be satisfied if the size of the cookie is greater than or equal to their satisfaction level. This problem is non-trivial because a naive approach of simply assigning cookies to children in the order they are given would not guarantee the maximum number of satisfied children. The greedy approach of sorting both the satisfaction levels and cookie sizes is necessary to ensure the optimal solution.

## Approach
The algorithm strategy used here is the two-pointer technique, where we iterate through the sorted satisfaction levels and cookie sizes in ascending order. The intuition behind this approach is to greedily match the largest cookie to the child with the highest satisfaction level. By sorting both arrays, we ensure that we are always considering the smallest possible cookie that can satisfy the current child, thus maximizing the number of satisfied children. The data structures used are arrays to store the satisfaction levels and cookie sizes, which are chosen for their simplicity and efficiency. This approach handles the key constraint by only assigning a cookie to a child if the cookie's size is greater than or equal to the child's satisfaction level.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n log n + m log m) | The time complexity is dominated by the sorting of the satisfaction levels and cookie sizes, where n is the number of children and m is the number of cookies. The subsequent while loop has a time complexity of O(n + m), but this is dwarfed by the sorting operation. |
| Space  | O(1) | The space complexity is O(1) because we are not using any extra space that scales with the input size, excluding the input arrays themselves. |

## Algorithm Walkthrough
```
Input: g = [1, 2, 3], s = [1, 2]
Step 1: Sort g and s, resulting in g = [1, 2, 3] and s = [1, 2]
Step 2: Initialize childIndex = 0 and cookieIndex = 0
Step 3: Compare g[childIndex] (1) with s[cookieIndex] (1), since 1 >= 1, increment childIndex to 1
Step 4: Increment cookieIndex to 1
Step 5: Compare g[childIndex] (2) with s[cookieIndex] (2), since 2 >= 2, increment childIndex to 2
Step 6: Increment cookieIndex to 2, but since cookieIndex is now out of bounds of s, the loop ends
Output: childIndex = 2, meaning 2 children can be satisfied
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize childIndex and cookieIndex}
    B --> C{"Compare g[childIndex] with s[cookieIndex]"}
    C -->|s[cookieIndex] >= g[childIndex]| D[Increment childIndex]
    C --> E{Increment cookieIndex}
    D --> E
    E -->|cookieIndex < s.length and childIndex < g.length| C
    E -->|Otherwise| F[Return childIndex]
```
## Key Insight
> **Tip:** The key insight here is to sort both the satisfaction levels and cookie sizes before applying the two-pointer technique, ensuring the maximum number of children are satisfied by greedily matching the largest cookie to the child with the highest satisfaction level.

## Edge Cases
- **Empty/null input**: If either the satisfaction levels array `g` or the cookie sizes array `s` is empty, the function returns 0, as there are no children to satisfy or no cookies to assign.
- **Single element**: If either array has a single element, the function will still work correctly. For example, if `g = [1]` and `s = [1]`, the function will return 1, indicating that the single child can be satisfied.
- **All children have higher satisfaction levels than all cookies**: In this case, the function will return 0, as no child can be satisfied with the available cookies.

## Common Mistakes
- **Mistake 1**: Not sorting the arrays before applying the two-pointer technique. This can lead to incorrect results because the algorithm relies on the sorted order to greedily match cookies to children.
- **Mistake 2**: Incorrectly incrementing the indices. For example, incrementing `childIndex` without checking if the current cookie satisfies the current child can lead to incorrect results.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm would still work correctly, but the time complexity would improve to O(n + m) because the sorting step would be unnecessary.
- "Can you do it in O(1) space?" → Yes, the current implementation already achieves O(1) space complexity, excluding the input arrays.
- "What if there are duplicates?" → The algorithm would still work correctly, as it only cares about the relative order of the satisfaction levels and cookie sizes, not their actual values.

## Java Solution

```java
// Problem: Assign Cookies
// Language: Java
// Difficulty: Easy
// Time Complexity: O(n log n) — sorting and two-pointer technique
// Space Complexity: O(1) — no extra space used (excluding input arrays)
// Approach: Two-pointer technique — assign cookies based on greedily matching largest cookie to child's satisfaction

import java.util.Arrays;

public class Solution {
    /**
     * Assign cookies to children based on their satisfaction levels.
     * 
     * @param g an array of integers representing the satisfaction levels of the children
     * @param s an array of integers representing the sizes of the cookies
     * @return the maximum number of children that can be satisfied
     */
    public int findContentChildren(int[] g, int[] s) {
        // Edge case: empty input → return 0
        if (g.length == 0 || s.length == 0) {
            return 0;
        }

        // Sort the satisfaction levels and cookie sizes in ascending order
        Arrays.sort(g); // sort satisfaction levels
        Arrays.sort(s); // sort cookie sizes

        int childIndex = 0; // index for the current child
        int cookieIndex = 0; // index for the current cookie

        // Iterate through the children and cookies
        while (childIndex < g.length && cookieIndex < s.length) {
            // If the current cookie satisfies the current child, move to the next child
            if (s[cookieIndex] >= g[childIndex]) {
                childIndex++; // move to the next child
            }
            // Move to the next cookie
            cookieIndex++; // move to the next cookie
        }

        // Return the number of satisfied children
        return childIndex; // return the number of satisfied children
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] g = {1, 2, 3};
        int[] s = {1, 2};
        System.out.println(solution.findContentChildren(g, s)); // Output: 2
    }
}
```
