---
title: "Two Sum"
language: "java"
difficulty: "easy"
section: "dsa"
tags: "dsa, java, easy, leetcode, algorithms"
banner: "https://image.pollinations.ai/prompt/dsa%20Two%20Sum%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Two Sum

![Two Sum](https://image.pollinations.ai/prompt/dsa%20Two%20Sum%20programming%20abstract?width=1200&height=630&nologo=true)

## Approach
Use a HashMap to store each number and its index as we iterate. For each element, check if its complement (`target - num`) already exists in the map. This gives us O(n) time instead of the brute-force O(n²).

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n)  | Single pass through the array |
| Space  | O(n)  | HashMap stores up to n elements |

## Key Insight
> **Tip:** Store the number as the key and its index as the value. When you find the complement, you immediately have both indices.

## Edge Cases
- No solution exists (problem guarantees exactly one solution)
- Same element used twice (use index check: `map.get(complement) != i`)

## Java Solution

```java
class TwoSum {
    // Problem: Two Sum
    // Language: Java
    // Difficulty: Easy
    // Time Complexity: O(n)
    // Space Complexity: O(n)

    public int[] twoSum(int[] nums, int target) {
        // Map: number -> index
        Map<Integer, Integer> map = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];

            // If complement already seen, we found our pair
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }

            // Store current number with its index
            map.put(nums[i], i);
        }

        return new int[]{}; // guaranteed to have a solution
    }
}
```
