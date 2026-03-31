---
title: "Find Minimum in Rotated Sorted Array"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, leetcode, algorithms, coding-interview"
banner: "https://image.pollinations.ai/prompt/dsa%20Find%20Minimum%20in%20Rotated%20Sorted%20Array%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Find Minimum in Rotated Sorted Array

## Problem Understanding
The problem asks to find the minimum element in a rotated sorted array, where the array was initially sorted in ascending order but has been rotated an unknown number of times. The key constraint is that the array has been rotated, which means the minimum element could be anywhere in the array. This problem is non-trivial because a naive approach, such as scanning the entire array, would have a time complexity of O(n), whereas a more efficient solution can achieve O(log n) time complexity using a modified binary search. The rotation of the array introduces complexity because it disrupts the usual ordering, making it harder to identify the minimum without a systematic approach.

## Approach
The algorithm strategy is to use a modified binary search to find the minimum element in the rotated sorted array. The intuition behind this approach is that if the middle element is greater than the rightmost element, the minimum must be in the right half of the array, and if the middle element is less than or equal to the rightmost element, the minimum must be in the left half. This approach works because the array is initially sorted in ascending order, so the rotation will always result in a sequence where the left half is either entirely greater than the right half or the left half includes the minimum. The algorithm uses two pointers, `left` and `right`, starting at the beginning and end of the array, respectively, and iteratively narrows down the search space by adjusting these pointers based on the comparison of the middle element with the rightmost element.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(log n) | Because the algorithm uses a modified binary search, dividing the search space roughly in half with each iteration, leading to a logarithmic time complexity. The number of iterations is proportional to the number of times the array can be halved until only one element remains. |
| Space  | O(1) | The algorithm uses a constant amount of space to store the pointers (`left`, `right`, and `mid`) and does not allocate any additional data structures that scale with input size, resulting in a constant space complexity. |

## Algorithm Walkthrough
```
Input: [3, 4, 5, 1, 2]
Step 1: left = 0, right = 4, mid = 2
       Since nums[mid] = 5 > nums[right] = 2, the minimum must be in the right half.
       left = mid + 1 = 3
Step 2: left = 3, right = 4, mid = 3
       Since nums[mid] = 1 <= nums[right] = 2, the minimum must be in the left half.
       right = mid = 3
Step 3: left = 3, right = 3, since left == right, the search ends.
Output: nums[left] = nums[3] = 1
```
This walkthrough demonstrates how the algorithm efficiently finds the minimum element in a rotated sorted array.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Middle element > Rightmost element?"}
    B -->|Yes| C[Move left pointer to mid + 1]
    B -->|No| D[Move right pointer to mid]
    C --> E{"Left pointer < Right pointer?"}
    D --> E
    E -->|Yes| B
    E -->|No| F["Return nums[left"]]
    F --> G[End]
```
This flowchart illustrates the decision-making process of the algorithm, showing how it iteratively adjusts the search space based on comparisons.

## Key Insight
> **Tip:** The key insight is to recognize that the rotation of a sorted array creates a condition where the middle element's comparison with the rightmost element can reliably indicate which half of the array the minimum element is in.

## Edge Cases
- **Empty/null input**: If the input array is null or empty, the algorithm returns -1, indicating that there is no minimum element to find. This is handled by the initial check at the beginning of the function.
- **Single element**: If the array contains only one element, the function returns that element, as it is the minimum by default. This case is implicitly handled by the algorithm, as the while loop condition `left < right` will be false, and the function will return `nums[left]`, which is the only element in the array.
- **Array not rotated (sorted in ascending order)**: If the input array is already sorted in ascending order (i.e., not rotated), the algorithm still works correctly. It will compare the middle element with the rightmost element and, finding that the middle element is less than or equal to the rightmost element, it will move the right pointer to the middle. This process continues until `left` and `right` meet at the first element, which is the minimum in an unrotated, sorted array.

## Common Mistakes
- **Mistake 1: Incorrectly handling the case when the middle element equals the rightmost element**: If the middle element equals the rightmost element, it's crucial to consider which half the minimum could be in. The algorithm correctly handles this by moving the right pointer to the middle, as the middle element could potentially be the minimum.
- **Mistake 2: Failing to check for the empty input array**: Not checking for an empty input array can lead to an ArrayIndexOutOfBoundsException. The algorithm checks for this at the beginning and returns -1 to indicate an invalid input.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, finding the minimum element at the start of the array, as the while loop condition will be false, and it returns `nums[left]`.
- "Can you do it in O(1) space?" → The algorithm already uses O(1) space, as it only utilizes a constant amount of space for the pointers and does not allocate any additional data structures.
- "What if there are duplicates?" → The presence of duplicates does not affect the correctness of the algorithm, as it relies on the comparison of the middle element with the rightmost element to determine which half to search in. However, in the worst-case scenario where all elements are the same, the algorithm degrades to linear search, as it cannot effectively divide the search space based on comparisons.

## Java Solution

```java
// Problem: Find Minimum in Rotated Sorted Array
// Language: Java
// Difficulty: Medium
// Time Complexity: O(log n) — using modified binary search
// Space Complexity: O(1) — no extra space used
// Approach: Modified binary search — find the pivot where the array is rotated

public class Solution {
    public int findMin(int[] nums) {
        // Edge case: empty input → return -1
        if (nums == null || nums.length == 0) return -1;

        // Initialize two pointers, one at the start and one at the end of the array
        int left = 0; // left pointer
        int right = nums.length - 1; // right pointer

        // Continue the search until the two pointers meet
        while (left < right) {
            // Calculate the middle index
            int mid = left + (right - left) / 2; // avoid overflow

            // If the middle element is greater than the rightmost element, 
            // the minimum must be in the right half
            if (nums[mid] > nums[right]) {
                // Move the left pointer to the right of the middle
                left = mid + 1; // because mid is not the minimum
            } 
            // If the middle element is less than or equal to the rightmost element, 
            // the minimum must be in the left half
            else {
                // Move the right pointer to the left of the middle
                right = mid; // because mid could be the minimum
            }
        }

        // At this point, left and right pointers are the same, 
        // and they point to the minimum element
        return nums[left];
    }
}
```
