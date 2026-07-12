---
title: "Patching Array JS Greedy"
language: "javascript"
difficulty: "hard"
section: "dsa"
tags: "dsa, javascript, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/617/1200/630"
update_count: 0
---

# Patching Array JS Greedy

## Problem Understanding
The problem is asking to find the minimum number of patches required to cover all numbers from 1 to `n`, given an array of numbers `nums`. The key constraint is that we can only use each number in `nums` once, and we can use a patch to cover a gap in the sequence. The problem is non-trivial because a naive approach would be to simply iterate through the numbers from 1 to `n` and check if each number is covered by the `nums` array, but this approach would not consider the optimal way to use the patches. The problem requires a greedy algorithm that always chooses the smallest patch that can cover the current gap.

## Approach
The algorithm strategy is to use a greedy approach, always choosing the smallest patch that can cover the current gap. The intuition behind this approach is that using the smallest patch will leave the least amount of uncovered numbers, making it more likely to cover the remaining numbers with the next patch. The algorithm uses a while loop to iterate through the `nums` array and the `n` limit, keeping track of the current gap and the number of patches used. The algorithm uses a `reach` variable to keep track of the maximum value that can be covered, and increments it by either using a number from the `nums` array or by using a patch. The `reach` variable is updated based on whether the current number is within the current reach or not.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through the `nums` array and the `n` limit, performing a constant amount of work for each iteration. The while loop runs for at most `n` iterations, making the time complexity O(n). |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the `patchCount`, `i`, and `reach` variables, regardless of the input size. |

## Algorithm Walkthrough
```
Input: nums = [1, 3], n = 6
Step 1: patchCount = 0, i = 0, reach = 0
Step 2: since reach < 6, we enter the loop. Since i < nums.length, we check if nums[i] <= reach + 1. Since 1 <= 0 + 1, we update reach = 0 + 1 = 1 and i = 0 + 1 = 1.
Step 3: since reach < 6, we enter the loop. Since i < nums.length, we check if nums[i] <= reach + 1. Since 3 > 1 + 1, we use a patch to cover the current gap, updating reach = 1 * 2 + 1 = 3 and patchCount = 0 + 1 = 1.
Step 4: since reach < 6, we enter the loop. Since i >= nums.length, we use a patch to cover the current gap, updating reach = 3 * 2 + 1 = 7 and patchCount = 1 + 1 = 2.
Output: patchCount = 1 (since the while loop exits when reach >= 6)
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"reach < n?"}
    B -->|Yes| C{"nums[i] <= reach + 1?"}
    C -->|Yes| D["reach += nums[i"], i++]
    C -->|No| E{"nums[i] > reach + 1?"}
    E -->|Yes| F["reach = reach * 2 + 1, patchCount++"]
    E -->|No| G[End]
    B -->|No| G
    F --> B
    D --> B
```
## Key Insight
> **Tip:** The key insight is to always choose the smallest patch that can cover the current gap, which is achieved by updating the `reach` variable based on whether the current number is within the current reach or not.

## Edge Cases
- **Empty input array**: If the input array `nums` is empty, the algorithm will use patches to cover all numbers from 1 to `n`, resulting in `patchCount` being equal to the number of bits required to represent `n`.
- **Single element array**: If the input array `nums` contains a single element, the algorithm will use patches to cover all numbers from 1 to `n`, except for the single element, which will be used to cover the gap.
- **Large input array**: If the input array `nums` contains a large number of elements, the algorithm will use the elements to cover the gaps, resulting in a smaller `patchCount`.

## Common Mistakes
- **Mistake 1**: Not updating the `reach` variable correctly based on whether the current number is within the current reach or not. → To avoid this, make sure to update the `reach` variable based on the current number and the current reach.
- **Mistake 2**: Not using patches correctly to cover the current gap. → To avoid this, make sure to use patches only when necessary, and update the `patchCount` variable accordingly.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly, as the sorting of the input array does not affect the greedy approach.
- "Can you do it in O(1) space?" → Yes, the algorithm already uses O(1) space, as it only uses a constant amount of space to store the `patchCount`, `i`, and `reach` variables.
- "What if there are duplicates in the input array?" → The algorithm will still work correctly, as the duplicates will not affect the greedy approach. However, the algorithm can be optimized to remove duplicates from the input array before running the algorithm.

## Javascript Solution

```javascript
// Problem: Patching Array
// Language: javascript
// Difficulty: Hard
// Time Complexity: O(n) — iterating through the nums array and the patch array
// Space Complexity: O(1) — constant space used
// Approach: Greedy algorithm — always choose the smallest patch that can cover the current gap

/**
 * @param {number[]} nums
 * @param {number} n
 * @return {number}
 */
var minPatches = function(nums, n) {
    // Initialize variables to keep track of the current gap and the number of patches used
    let patchCount = 0; // number of patches used so far
    let i = 0; // current index in the nums array
    let reach = 0; // current reach (the maximum value we can cover)

    // Loop through the nums array
    while (reach < n) {
        // If the current index is out of bounds, it means we need to use a patch
        if (i >= nums.length) {
            // Use a patch to cover the current gap
            reach = reach * 2 + 1; // the new reach after using the patch
            patchCount++; // increment the patch count
        } else {
            // If the current number is within the current reach, we can use it to cover the gap
            if (nums[i] <= reach + 1) {
                reach += nums[i]; // update the reach
                i++; // move to the next index
            } else {
                // If the current number is not within the current reach, we need to use a patch
                reach = reach * 2 + 1; // the new reach after using the patch
                patchCount++; // increment the patch count
            }
        }
    }

    // Return the minimum number of patches used
    return patchCount;
};
```
