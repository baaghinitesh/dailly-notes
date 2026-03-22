---
title: "Longest Substring Without Repeating Characters"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, sliding-window, leetcode"
banner: "https://picsum.photos/seed/longestsub-java/1200/630"
update_count: 0
---

# Longest Substring Without Repeating Characters

![Longest Substring](https://picsum.photos/seed/longestsub-java/1200/630)

## Approach
Sliding window with a HashMap. Maintain a window `[left, right]`. As we expand right, if the character already exists in the window, shrink from the left until the duplicate is removed. Track the maximum window size seen.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n)  | Each character is added/removed at most once |
| Space  | O(min(m,n)) | m = charset size, n = string length |

## Key Insight
> **Tip:** Store the character's latest index in the map. When a duplicate is found, jump `left` directly to `map.get(c) + 1` — no need to shrink one step at a time.

## Edge Cases
- Empty string → return 0
- All same characters → return 1
- All unique characters → return n

## Java Solution

```java
class LongestSubstringWithoutRepeating {
    // Problem: Longest Substring Without Repeating Characters
    // Language: Java
    // Difficulty: Medium
    // Time Complexity: O(n)
    // Space Complexity: O(min(m, n))

    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int maxLen = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);

            // If char seen and its index is within current window, shrink left
            if (map.containsKey(c) && map.get(c) >= left) {
                left = map.get(c) + 1;
            }

            // Update latest index of this character
            map.put(c, right);

            // Update max window size
            maxLen = Math.max(maxLen, right - left + 1);
        }

        return maxLen;
    }
}
```
