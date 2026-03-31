---
title: "Two Sum using Dictionary"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, hash-map, leetcode"
banner: "https://image.pollinations.ai/prompt/dsa%20Two%20Sum%20using%20Dictionary%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Two Sum using Dictionary

![Two Sum Python](https://image.pollinations.ai/prompt/dsa%20Two%20Sum%20using%20Dictionary%20programming%20abstract?width=1200&height=630&nologo=true)

## Approach
Use a Python dict to map each number to its index. For each element, check if `target - num` is already in the dict. Python dicts are hash tables with O(1) average lookup.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n)  | Single pass, O(1) dict lookup |
| Space  | O(n)  | Dict stores up to n entries |

## Key Insight
> **Tip:** In Python, `dict` lookups are O(1) average. The `in` operator on a dict checks keys, not values — always use `complement in seen` not `complement in seen.values()`.

## Python Solution

```python
# Problem: Two Sum using Dictionary
# Language: Python
# Difficulty: Easy
# Time Complexity: O(n)
# Space Complexity: O(n)

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # number -> index

        for i, num in enumerate(nums):
            complement = target - num

            # If complement already seen, return both indices
            if complement in seen:
                return [seen[complement], i]

            seen[num] = i

        return []  # guaranteed to have a solution
```
