---
title: "Two Sum with Map"
language: "javascript"
difficulty: "easy"
section: "dsa"
tags: "dsa, javascript, easy, map, leetcode"
banner: "https://image.pollinations.ai/prompt/dsa%20Two%20Sum%20with%20Map%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Two Sum with Map

![Two Sum JavaScript](https://image.pollinations.ai/prompt/dsa%20Two%20Sum%20with%20Map%20programming%20abstract?width=1200&height=630&nologo=true)

## Approach
Use a JavaScript `Map` to store number→index pairs. For each element, check if `target - num` exists in the map. `Map.has()` and `Map.get()` are O(1) average.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n)  | Single pass, O(1) Map operations |
| Space  | O(n)  | Map stores up to n entries |

## Key Insight
> **Tip:** Use `Map` over plain objects `{}` for this pattern — `Map` handles all key types correctly (including numbers) and has explicit `has/get/set` methods that are clearer in intent.

## JavaScript Solution

```javascript
// Problem: Two Sum with Map
// Language: JavaScript
// Difficulty: Easy
// Time Complexity: O(n)
// Space Complexity: O(n)

/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
function twoSum(nums, target) {
    const seen = new Map(); // number -> index

    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];

        // If complement was seen before, return both indices
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }

        seen.set(nums[i], i);
    }

    return []; // guaranteed to have a solution
}
```
