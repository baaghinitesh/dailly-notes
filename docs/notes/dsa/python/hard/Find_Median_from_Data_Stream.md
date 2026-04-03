---
title: "Find Median from Data Stream"
language: "python"
difficulty: "hard"
section: "dsa"
tags: "dsa, python, hard, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/389/1200/630"
update_count: 0
---

# Find Median from Data Stream

## Problem Understanding
The problem is asking to design a data structure that can efficiently find the median of a stream of numbers as they are added. The key constraints are that the numbers are added one at a time, and the median must be calculated after each addition. What makes this problem non-trivial is that a naive approach of sorting all the numbers after each addition would result in a time complexity of O(n^2 log n), which is inefficient. The problem requires a data structure that can maintain the median in O(log n) time complexity.

## Approach
The algorithm strategy is to use two heaps, a max heap for the lower half of the numbers and a min heap for the upper half. This approach works because the max heap will always contain the smaller half of the numbers, and the min heap will always contain the larger half. The intuition behind this is that by maintaining the balance between the two heaps, we can ensure that the median is always at the top of one of the heaps. The data structures used are two heaps, which are chosen because they allow for efficient insertion and removal of elements. The approach handles the key constraints by ensuring that the size difference between the two heaps is at most 1, which allows for efficient calculation of the median.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(log n) | The time complexity is O(log n) because each insertion operation involves pushing an element into one of the heaps, which takes O(log n) time. The balancing operation also takes O(log n) time. |
| Space  | O(n) | The space complexity is O(n) because we need to store all the elements in the two heaps. |

## Algorithm Walkthrough
```
Input: [1, 2, 3]
Step 1: Initialize two empty heaps, lower_half and upper_half
lower_half = [], upper_half = []
Step 2: Add 1 to the data stream
lower_half = [-1], upper_half = []
Step 3: Add 2 to the data stream
Since 2 is greater than -1 (the max of lower_half), add 2 to upper_half
lower_half = [-1], upper_half = [2]
Step 4: Balance the heaps
Since the size difference is 1, no balancing is needed
lower_half = [-1], upper_half = [2]
Step 5: Add 3 to the data stream
Since 3 is greater than -1 (the max of lower_half), add 3 to upper_half
lower_half = [-1], upper_half = [2, 3]
Step 6: Balance the heaps
Since the size of upper_half is greater than lower_half, pop 2 from upper_half and add to lower_half
lower_half = [-1, -2], upper_half = [3]
Output: The median is 2, which is the max of the lower_half
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Is lower_half empty or num <= -lower_half[0]?}
    B -->|Yes| C[Push num to lower_half]
    B -->|No| D[Push num to upper_half]
    C --> E[Balance heaps]
    D --> E
    E --> F{Is size difference > 1?}
    F -->|Yes| G[Balance heaps]
    F -->|No| H[Return median]
```
## Key Insight
> **Tip:** The key insight is to maintain the balance between the two heaps, ensuring that the size difference is at most 1, which allows for efficient calculation of the median.

## Edge Cases
- **Empty input**: If the input stream is empty, the algorithm will return None or raise an exception, indicating that there are no numbers to calculate the median from.
- **Single element**: If the input stream contains only one number, the algorithm will return that number as the median.
- **Duplicate numbers**: If the input stream contains duplicate numbers, the algorithm will treat them as separate numbers and calculate the median accordingly.

## Common Mistakes
- **Mistake 1**: Not balancing the heaps after each insertion, which can lead to incorrect median calculations. To avoid this, ensure that the size difference between the two heaps is at most 1 after each insertion.
- **Mistake 2**: Not handling the case where the input stream is empty. To avoid this, add a check at the beginning of the findMedian method to return None or raise an exception if the input stream is empty.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly, but the time complexity will be O(n) because the heaps will not be balanced.
- "Can you do it in O(1) space?" → No, the algorithm requires O(n) space to store all the elements in the two heaps.
- "What if there are duplicates?" → The algorithm will treat duplicates as separate numbers and calculate the median accordingly.

## Python Solution

```python
# Problem: Find Median from Data Stream
# Language: python
# Difficulty: Hard
# Time Complexity: O(log n) — for each insertion, maintain two heaps 
# Space Complexity: O(n) — store all elements in two heaps
# Approach: Two heap balancing — maintain max heap for lower half and min heap for upper half

import heapq

class MedianFinder:
    def __init__(self):
        # Initialize two heaps, max heap for lower half and min heap for upper half
        self.lower_half = []  # max heap
        self.upper_half = []  # min heap

    def addNum(self, num: int) -> None:
        # If lower half is empty or num is less than the max of lower half, add to lower half
        if not self.lower_half or num <= -self.lower_half[0]:  
            # Push num to lower half (max heap), multiply by -1 to simulate max heap
            heapq.heappush(self.lower_half, -num)
        else:
            # Push num to upper half (min heap)
            heapq.heappush(self.upper_half, num)

        # Balance two heaps to ensure size difference is at most 1
        if len(self.lower_half) > len(self.upper_half) + 1:
            # Pop max from lower half and push to upper half
            heapq.heappush(self.upper_half, -heapq.heappop(self.lower_half))
        elif len(self.upper_half) > len(self.lower_half):
            # Pop min from upper half and push to lower half
            heapq.heappush(self.lower_half, -heapq.heappop(self.upper_half))

    def findMedian(self) -> float:
        # Edge case: no numbers in data stream
        if not self.lower_half and not self.upper_half:
            return None  # or raise exception

        # If total count is odd, return max of lower half
        if len(self.lower_half) > len(self.upper_half):
            return -self.lower_half[0]
        # If total count is even, return average of max of lower half and min of upper half
        else:
            return (-self.lower_half[0] + self.upper_half[0]) / 2.0

# Example usage
median_finder = MedianFinder()
median_finder.addNum(1)
median_finder.addNum(2)
print(median_finder.findMedian())  # 1.5
median_finder.addNum(3)
print(median_finder.findMedian())  # 2
```
