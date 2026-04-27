---
title: "Two Pointers Technique"
language: "python"
difficulty: "medium"
section: "dsa"
tags: "dsa, python, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/682/1200/630"
update_count: 0
---

# Two Pointers Technique

## Problem Understanding
The problem is asking us to find a pair of elements in a list that add up to zero using the two pointers technique. The key constraint here is that the input list can be empty, and if it is, we should return -1. What makes this problem non-trivial is that the naive approach of checking every pair of elements would result in a time complexity of O(n^2), which is inefficient for large lists. The two pointers technique provides a more efficient solution with a time complexity of O(n).

## Approach
The algorithm strategy used here is the two pointers technique, where we initialize two pointers, one at the start and one at the end of the list. We then enter a loop where we check if the current pair of elements meet the condition (i.e., their sum is zero). If they do, we return the pair. If the sum is less than zero, we move the left pointer to the right to increase the sum, and if the sum is greater than zero, we move the right pointer to the left to decrease the sum. This approach works because it allows us to efficiently search for a pair of elements that meet the condition without having to check every possible pair. We use a simple while loop and conditional statements to implement this approach.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through the list once, using two pointers that move towards each other. In the worst-case scenario, the pointers will meet in the middle of the list, resulting in a time complexity of O(n). |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the two pointers and the current pair of elements, resulting in a space complexity of O(1). |

## Algorithm Walkthrough
```
Input: [-2, -1, 0, 1, 2]
Step 1: Initialize two pointers, left = 0 and right = 4
Step 2: Check if the current pair of elements meet the condition: nums[left] + nums[right] = -2 + 2 = 0
Step 3: Since the sum is equal to zero, return the pair: [-2, 2]
Output: [-2, 2]
```
Note: This example demonstrates the algorithm's ability to find a pair of elements that add up to zero.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Initialize Pointers}
    B --> C["Left = 0, Right = len(nums) - 1"]
    C --> D{While Left < Right}
    D -->|Yes| E["Check Pair: nums[left"] + nums[right]]
    E --> F{"Sum == 0?"}
    F -->|Yes| G[Return Pair]
    F -->|No| H{"Sum < 0?"}
    H -->|Yes| I["Left += 1"]
    H -->|No| J["Right -= 1"]
    I --> D
    J --> D
    D -->|No| K["Return -1"]
```
This flowchart represents the algorithm's decision flow and data transformation.

## Key Insight
> **Tip:** The key insight here is to use the two pointers technique to efficiently search for a pair of elements that add up to zero, taking advantage of the fact that moving the pointers towards each other reduces the search space.

## Edge Cases
- **Empty/null input**: If the input list is empty, the algorithm will return -1, as there are no pairs to check.
- **Single element**: If the input list contains only one element, the algorithm will return -1, as there are no pairs to check.
- **Duplicate elements**: If the input list contains duplicate elements, the algorithm will still work correctly, as it only checks each pair of elements once.

## Common Mistakes
- **Mistake 1**: Not checking for the edge case where the input list is empty, resulting in an incorrect result or an error.
- **Mistake 2**: Not moving the pointers correctly based on the sum of the current pair of elements, resulting in an incorrect result or an infinite loop.

## Interview Follow-ups
> **Interview:** 
- "What if the input is sorted?" → The algorithm will still work correctly, as it only relies on the relative positions of the pointers, not the absolute values of the elements.
- "Can you do it in O(1) space?" → The algorithm already uses O(1) space, as it only stores a constant amount of information.
- "What if there are duplicates?" → The algorithm will still work correctly, as it only checks each pair of elements once, and duplicates will not affect the result.

## Python Solution

```python
# Problem: Two Pointers Technique
# Language: python
# Difficulty: medium
# Time Complexity: O(n) — two pointers iterating through the list
# Space Complexity: O(1) — constant space used
# Approach: two pointers technique — for each pair of elements, check if they meet the condition

class Solution:
    def twoPointers(self, nums): 
        # Edge case: empty input → return -1
        if not nums: 
            return -1
        
        # Initialize two pointers, one at the start and one at the end of the list
        left = 0  # left pointer
        right = len(nums) - 1  # right pointer
        
        # Continue the loop until the two pointers meet
        while left < right: 
            # Check if the current pair of elements meet the condition
            if nums[left] + nums[right] == 0: 
                return [nums[left], nums[right]]  # return the pair if condition is met
            # If the sum is less than 0, move the left pointer to the right to increase the sum
            elif nums[left] + nums[right] < 0: 
                left += 1  # move left pointer to the right
            # If the sum is greater than 0, move the right pointer to the left to decrease the sum
            else: 
                right -= 1  # move right pointer to the left
        
        # If no pair is found, return -1
        return -1

    # Example usage:
    def main(self):
        print(self.twoPointers([-2, -1, 0, 1, 2]))  # Output: [-1, 1]
        print(self.twoPointers([1, 2, 3, 4, 5]))  # Output: -1

if __name__ == "__main__":
    solution = Solution()
    solution.main()
```
