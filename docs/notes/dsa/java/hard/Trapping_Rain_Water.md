---
title: "Trapping Rain Water"
language: "java"
difficulty: "hard"
section: "dsa"
tags: "dsa, java, hard, two-pointers, leetcode"
banner: "https://image.pollinations.ai/prompt/dsa%20Trapping%20Rain%20Water%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Trapping Rain Water

![Trapping Rain Water](https://image.pollinations.ai/prompt/dsa%20Trapping%20Rain%20Water%20programming%20abstract?width=1200&height=630&nologo=true)

## Approach
Two-pointer approach. Maintain `left` and `right` pointers and track `maxLeft` and `maxRight`. At each step, process the side with the smaller max height — the water trapped at that position is `max - height[i]`. Move the pointer inward.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n)  | Single pass with two pointers |
| Space  | O(1)  | Only pointer and max variables |

## Key Insight
> **Tip:** Water at any position is bounded by `min(maxLeft, maxRight) - height[i]`. Process the smaller side first — you already know the limiting factor.

## Edge Cases
- Array length < 3 → no water can be trapped
- Monotonically increasing/decreasing → no water trapped
- All same height → no water trapped

## Java Solution

```java
class TrappingRainWater {
    // Problem: Trapping Rain Water
    // Language: Java
    // Difficulty: Hard
    // Time Complexity: O(n)
    // Space Complexity: O(1)

    public int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int maxLeft = 0, maxRight = 0;
        int water = 0;

        while (left < right) {
            if (height[left] <= height[right]) {
                // Left side is the bottleneck
                if (height[left] >= maxLeft) {
                    maxLeft = height[left]; // update max
                } else {
                    water += maxLeft - height[left]; // trap water
                }
                left++;
            } else {
                // Right side is the bottleneck
                if (height[right] >= maxRight) {
                    maxRight = height[right];
                } else {
                    water += maxRight - height[right];
                }
                right--;
            }
        }

        return water;
    }
}
```
