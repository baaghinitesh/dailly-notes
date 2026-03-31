---
title: "Maximum Subarray"
language: "javascript"
difficulty: "easy"
section: "dsa"
tags: "dsa, javascript, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/254/1200/630"
update_count: 0
---

# Maximum Subarray

## Problem Understanding
The problem is asking to find the maximum sum of a contiguous subarray within a given array of numbers. The key constraint is that the subarray must be contiguous, meaning that the elements must be next to each other in the original array. This problem is non-trivial because a naive approach, such as checking all possible subarrays, would have a high time complexity of O(n^2) due to the nested loops required to generate all subarrays. The problem requires an efficient algorithm that can find the maximum sum in a single pass through the array.

## Approach
The algorithm strategy used to solve this problem is Kadane's algorithm, which is a dynamic programming approach that iterates through the array and keeps track of the maximum sum of a subarray ending at each position. The intuition behind this approach is to decide, for each number, whether to include it in the current subarray or start a new one. This is achieved by maintaining two variables: `maxSum` to keep track of the maximum sum seen so far, and `currentSum` to keep track of the sum of the current subarray. The algorithm iterates through the array, updating `currentSum` and `maxSum` at each step, and finally returns the maximum sum found.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through the array once, performing a constant amount of work at each step. The loop runs from index 1 to the end of the array, resulting in a linear time complexity. |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the `maxSum` and `currentSum` variables, regardless of the size of the input array. |

## Algorithm Walkthrough
```
Input: [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Step 1: Initialize maxSum = -2, currentSum = -2
Step 2: i = 1, currentSum = max(-2 + 1, 1) = 1, maxSum = max(-2, 1) = 1
Step 3: i = 2, currentSum = max(1 + -3, -3) = -2, maxSum = max(1, -2) = 1
Step 4: i = 3, currentSum = max(-2 + 4, 4) = 4, maxSum = max(1, 4) = 4
Step 5: i = 4, currentSum = max(4 + -1, -1) = 3, maxSum = max(4, 3) = 4
Step 6: i = 5, currentSum = max(3 + 2, 2) = 5, maxSum = max(4, 5) = 5
Step 7: i = 6, currentSum = max(5 + 1, 1) = 6, maxSum = max(5, 6) = 6
Step 8: i = 7, currentSum = max(6 + -5, -5) = 1, maxSum = max(6, 1) = 6
Step 9: i = 8, currentSum = max(1 + 4, 4) = 5, maxSum = max(6, 5) = 6
Output: 6
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Initialize maxSum and currentSum]
    B --> C[Iterate through array]
    C --> D{"currentSum + nums[i] > nums[i]"}
    D -->|Yes| E["currentSum = currentSum + nums[i"]]
    D -->|No| F["currentSum = nums[i"]]
    E --> G["Update maxSum if currentSum > maxSum"]
    F --> G
    G --> H[Repeat iteration until end of array]
    H --> I[Return maxSum]
```

## Key Insight
> **Tip:** The key insight is to realize that the maximum sum of a subarray can be obtained by deciding, for each number, whether to include it in the current subarray or start a new one, which is achieved by maintaining a running sum of the current subarray and updating the maximum sum accordingly.

## Edge Cases
- **Empty/null input**: If the input array is empty or null, the algorithm returns -1 to indicate an error.
- **Single element**: If the input array contains only one element, the algorithm returns that element as the maximum sum.
- **All negative numbers**: If the input array contains only negative numbers, the algorithm returns the largest negative number (i.e., the one closest to zero) as the maximum sum.

## Common Mistakes
- **Mistake 1**: Not initializing `maxSum` and `currentSum` correctly, which can lead to incorrect results. To avoid this, make sure to initialize `maxSum` and `currentSum` with the first element of the array.
- **Mistake 2**: Not updating `maxSum` correctly, which can lead to missing the maximum sum. To avoid this, make sure to update `maxSum` whenever `currentSum` is greater than `maxSum`.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm still works correctly, with a time complexity of O(n), because it only cares about the maximum sum of a contiguous subarray.
- "Can you do it in O(1) space?" → The algorithm already uses O(1) space, so this is not a concern.
- "What if there are duplicates?" → The algorithm still works correctly, because it only cares about the maximum sum of a contiguous subarray, and duplicates do not affect this.

## Javascript Solution

```javascript
// Problem: Maximum Subarray
// Language: javascript
// Difficulty: Easy
// Time Complexity: O(n) — single pass through array
// Space Complexity: O(1) — constant space used
// Approach: Kadane's algorithm — for each number, decide whether to include it in current subarray or start a new one

class Solution {
    /**
     * Returns the maximum sum of a contiguous subarray within the given array.
     * @param {number[]} nums - The input array of numbers.
     * @returns {number} The maximum sum of a subarray.
     */
    maxSubArray(nums) {
        // Edge case: empty input → return -1 (or any other value signifying an error)
        if (!nums || nums.length === 0) return -1;

        // Initialize variables to keep track of the maximum sum and the current sum
        let maxSum = nums[0]; // Maximum sum seen so far
        let currentSum = nums[0]; // Sum of the current subarray

        // Iterate through the array starting from the second element (index 1)
        for (let i = 1; i < nums.length; i++) {
            // For each number, decide whether to include it in the current subarray or start a new one
            currentSum = Math.max(nums[i], currentSum + nums[i]); // Choose the maximum between including the current number and starting a new subarray
            maxSum = Math.max(maxSum, currentSum); // Update the maximum sum if the current sum is greater
        }

        // Return the maximum sum found
        return maxSum;
    }
}

// Test the solution
let solution = new Solution();
console.log(solution.maxSubArray([-2,1,-3,4,-1,2,1,-5,4])); // Output: 6
console.log(solution.maxSubArray([1])); // Output: 1
console.log(solution.maxSubArray([5,4,-1,7,8])); // Output: 23
```
