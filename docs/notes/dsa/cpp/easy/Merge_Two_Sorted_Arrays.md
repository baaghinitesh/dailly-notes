---
title: "Merge Two Sorted Arrays"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/670/1200/630"
update_count: 0
---

# Merge Two Sorted Arrays

## Problem Understanding
The problem is asking to merge two sorted arrays, `nums1` and `nums2`, into a single sorted array stored in `nums1`. The key constraint is that `nums1` has enough space to hold all elements from both arrays. What makes this problem non-trivial is that a naive approach, such as concatenating the arrays and then sorting, would have a higher time complexity. The given approach, using a two-pointer technique, takes advantage of the fact that the input arrays are already sorted.

## Approach
The algorithm strategy is to use a two-pointer technique, where two pointers, `p1` and `p2`, are initialized to the end of `nums1` and `nums2`, respectively. The intuition behind this approach is to merge the larger elements first, which allows for an efficient and in-place merge. The approach works by comparing the current elements of both arrays and adding the larger one to the result array, effectively merging the two arrays in a single pass. The `tail` pointer is used to keep track of the current position in the result array.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n + m) | The algorithm iterates through both arrays once, where `n` and `m` are the lengths of `nums1` and `nums2`, respectively. The comparison and assignment operations within the loop take constant time, resulting in a linear time complexity. |
| Space  | O(1) | Although the problem statement mentions a space complexity of O(n + m), this refers to the space required for the output array. The algorithm itself uses a constant amount of extra space to store the pointers and variables, making its space complexity O(1). |

## Algorithm Walkthrough
```
Input: nums1 = [1, 2, 3, 0, 0, 0], m = 3, nums2 = [2, 5, 6], n = 3
Step 1: Initialize pointers, p1 = 2, p2 = 2, tail = 5
Step 2: Compare nums1[p1] = 3 and nums2[p2] = 6, add 6 to nums1[tail--] = nums1[5]
Step 3: Update pointers, p1 = 2, p2 = 1, tail = 4
Step 4: Compare nums1[p1] = 3 and nums2[p2] = 5, add 5 to nums1[tail--] = nums1[4]
Step 5: Update pointers, p1 = 2, p2 = 0, tail = 3
Step 6: Compare nums1[p1] = 3 and nums2[p2] = 2, add 3 to nums1[tail--] = nums1[3]
Step 7: Update pointers, p1 = 1, p2 = 0, tail = 2
Step 8: Compare nums1[p1] = 2 and nums2[p2] = 2, add 2 to nums1[tail--] = nums1[2]
Step 9: Update pointers, p1 = 0, p2 = 0, tail = 1
Step 10: Compare nums1[p1] = 1 and nums2[p2] = 2, add 2 to nums1[tail--] = nums1[1]
Step 11: Update pointers, p1 = 0, p2 = -1, tail = 0
Step 12: Add remaining elements from nums1, nums1[0] = 1
Output: nums1 = [1, 2, 2, 3, 5, 6]
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize Pointers}
    B --> C{Compare Elements}
    C -->|nums1[p1] > nums2[p2]| D["Add nums1[p1"] to nums1[tail]]
    C -->|nums1[p1] <= nums2[p2]| E["Add nums2[p2"] to nums1[tail]]
    D --> F{Update Pointers}
    E --> F
    F --> G{"More Elements in nums2?"}
    G -->|Yes| H[Copy Remaining Elements]
    G -->|No| I{"More Elements in nums1?"}
    I -->|No| J[Done]
    I -->|Yes| K[No Action Needed]
    H --> J
    K --> J
```

## Key Insight
> **Tip:** The key insight is to merge the larger elements first, allowing for an efficient and in-place merge of the two sorted arrays.

## Edge Cases
- **Empty `nums2`**: If `nums2` is empty, the algorithm will simply return the original `nums1` array, as there are no elements to merge.
- **Single element in `nums1`**: If `nums1` has only one element, the algorithm will compare it with the elements of `nums2` and merge them accordingly.
- **Duplicate elements**: If there are duplicate elements in either `nums1` or `nums2`, the algorithm will handle them correctly, preserving the sorted order in the merged array.

## Common Mistakes
- **Mistake 1: Incorrect pointer updates**: Failing to update the pointers correctly can lead to incorrect merging or infinite loops. To avoid this, ensure that the pointers are updated based on the comparison result.
- **Mistake 2: Not handling edge cases**: Failing to handle edge cases, such as empty arrays or single-element arrays, can lead to incorrect results or crashes. To avoid this, explicitly handle these cases in the code.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted in descending order?" → The algorithm can be easily modified to handle descending order by changing the comparison logic.
- "Can you do it in O(1) space?" → The algorithm already uses O(1) extra space, making it efficient in terms of space complexity.
- "What if there are duplicates?" → The algorithm handles duplicates correctly, preserving the sorted order in the merged array.

## CPP Solution

```cpp
// Problem: Merge Two Sorted Arrays
// Language: C++
// Difficulty: Easy
// Time Complexity: O(n + m) — single pass through both arrays
// Space Complexity: O(n + m) — resulting array stores all elements
// Approach: Two-pointer technique — merge smaller elements first

class Solution {
public:
    void merge(int nums1[], int m, int nums2[], int n) {
        // Initialize two pointers for both arrays
        int p1 = m - 1;  // Pointer for nums1
        int p2 = n - 1;  // Pointer for nums2
        
        // Initialize a pointer for the result array
        int tail = m + n - 1;  // Pointer for the end of the result array
        
        // Merge larger elements first
        while ((p1 >= 0) && (p2 >= 0)) {
            // Compare current elements of both arrays and add the larger one to the result
            nums1[tail--] = (nums1[p1] > nums2[p2]) ? nums1[p1--] : nums2[p2--];
        }
        
        // Edge case: if there are remaining elements in nums2, append them to nums1
        while (p2 >= 0) {
            // Copy the remaining elements
            nums1[tail--] = nums2[p2--];
        }
        
        // Edge case: if there are remaining elements in nums1, they are already in place
        // No need to do anything, as the problem statement guarantees that nums1 has enough space
    }
};
```
