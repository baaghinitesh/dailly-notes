---
title: "Majority Element"
language: "java"
difficulty: "easy"
section: "dsa"
tags: "dsa, java, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/187/1200/630"
update_count: 0
---

# Majority Element

## Problem Understanding
The problem asks to find the majority element in an array, which is the element that appears more than n/2 times where n is the size of the array. The key constraint is that the solution should use linear time complexity, O(n), and constant space complexity, O(1). What makes this problem non-trivial is that a naive approach of sorting the array and then finding the middle element would take O(n log n) time complexity.

## Approach
The algorithm strategy used here is the Boyer-Moore Majority Vote algorithm, which essentially maintains a counter for the majority element. The intuition behind this approach is that by essentially pairing up elements that are different, the majority element will be the one left standing. This approach works because if there is a majority element, it will always be the one that is left after the pairing process. The data structure used is a simple counter and a candidate variable, which are chosen because they can efficiently keep track of the majority element and its count.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm makes two passes through the array: one to find the candidate for the majority element and another to verify that it indeed occurs more than n/2 times. Each pass takes O(n) time. |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the candidate and the count, regardless of the size of the input array. |

## Algorithm Walkthrough
```
Input: [3, 2, 3]
Step 1: Initialize candidate = 3, count = 1
Step 2: For the second element (2), since it does not match the candidate, decrement count: count = 0
Step 3: Since count is 0, update candidate to the current element (2) and reset count: candidate = 2, count = 1
Step 4: For the third element (3), since it does not match the candidate (2), decrement count: count = 0
Step 5: Since count is 0, update candidate to the current element (3) and reset count: candidate = 3, count = 1
Step 6: Verification pass: count occurrences of candidate (3) in the array: occurrences = 2
Step 7: Since occurrences (2) is more than n/2 (1.5), return candidate (3) as the majority element
Output: 3
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Initialize candidate and count]
    B --> C[Iterate through array]
    C --> D{Is current element same as candidate?}
    D -->|Yes| E[Increment count]
    D -->|No| F[Decrement count]
    F --> G{Is count zero?}
    G -->|Yes| H[Update candidate and reset count]
    G -->|No| C
    C --> I[End of array]
    I --> J[Verification pass]
    J --> K{Is candidate occurrences more than n/2?}
    K -->|Yes| L[Return candidate]
    K -->|No| M[Return -1 (no majority)]
```

## Key Insight
> **Tip:** The key insight to solving this problem efficiently is recognizing that the majority element can be found by essentially cancelling out the minority elements, one by one, which is achieved through the Boyer-Moore Majority Vote algorithm.

## Edge Cases
- **Empty input**: If the input array is empty, the function should return -1 (or throw an exception, depending on the requirements) because there is no majority element in an empty array.
- **Single element**: If the array contains only one element, that element is the majority element because it occurs more than n/2 times (where n=1).
- **No majority element**: If no element occurs more than n/2 times, the function should return -1, indicating that there is no majority element.

## Common Mistakes
- **Mistake 1**: Not verifying the candidate at the end to ensure it occurs more than n/2 times. This could lead to incorrect results if no majority element exists.
- **Mistake 2**: Not handling the edge case of an empty input array properly, which could result in incorrect results or exceptions.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The Boyer-Moore Majority Vote algorithm still works in O(n) time complexity, regardless of the input being sorted.
- "Can you do it in O(1) space?" → The Boyer-Moore Majority Vote algorithm already uses O(1) space, making it optimal in terms of space complexity.
- "What if there are duplicates?" → The algorithm handles duplicates correctly by counting the occurrences of the candidate in the verification pass.

## Java Solution

```java
// Problem: Majority Element
// Language: Java
// Difficulty: Easy
// Time Complexity: O(n) — single pass through array using Boyer-Moore algorithm
// Space Complexity: O(1) — constant space used
// Approach: Boyer-Moore Majority Vote algorithm — essentially maintains a counter for the majority element

public class Solution {
    public int majorityElement(int[] nums) {
        // Edge case: empty input → return -1 (or throw exception, depending on requirements)
        if (nums.length == 0) return -1;

        // Initialize the candidate and count
        int candidate = nums[0]; // initially assume the first element is the majority
        int count = 1; // start with a count of 1 for the first element

        // Iterate through the array starting from the second element
        for (int i = 1; i < nums.length; i++) {
            // If the current element matches the candidate, increment the count
            if (nums[i] == candidate) {
                count++; // increment count for matching element
            } else {
                // If the current element does not match, decrement the count
                count--; // decrement count for non-matching element
                // If the count reaches zero, update the candidate and reset count
                if (count == 0) {
                    candidate = nums[i]; // update candidate
                    count = 1; // reset count to 1
                }
            }
        }

        // At this point, the candidate is the majority element (assuming it exists)
        // However, to be sure (especially in cases where no majority exists), we should verify
        int occurrences = 0; // count occurrences of the candidate
        for (int num : nums) {
            if (num == candidate) occurrences++; // count occurrence
        }

        // Edge case: no majority element (less than n/2 occurrences)
        if (occurrences < nums.length / 2) return -1;

        return candidate; // confirmed majority element
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] nums = {3, 2, 3};
        int majority = solution.majorityElement(nums);
        System.out.println("Majority Element: " + majority);
    }
}
```
