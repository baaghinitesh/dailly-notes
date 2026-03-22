---
title: "Two Sum using unordered_map"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, hash-map, leetcode"
banner: "https://picsum.photos/seed/twosum-cpp/1200/630"
update_count: 0
---

# Two Sum using unordered_map

![Two Sum C++](https://picsum.photos/seed/twosum-cpp/1200/630)

## Approach
Use `unordered_map<int,int>` to store number→index pairs. For each element, check if `target - nums[i]` exists in the map. O(1) average lookup gives O(n) overall.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n) average | unordered_map O(1) average lookup |
| Space  | O(n)         | Map stores up to n entries |

## Key Insight
> **Tip:** `unordered_map` in C++ uses hash tables — O(1) average but O(n) worst case. For competitive programming, prefer it over `map` (O(log n)) when order doesn't matter.

## Edge Cases
- Guaranteed exactly one solution per problem constraints
- Negative numbers work fine with hash maps

## C++ Solution

```cpp
#include <vector>
#include <unordered_map>
using namespace std;

class TwoSum {
    // Problem: Two Sum using unordered_map
    // Language: C++
    // Difficulty: Easy
    // Time Complexity: O(n) average
    // Space Complexity: O(n)
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen; // number -> index

        for (int i = 0; i < (int)nums.size(); i++) {
            int complement = target - nums[i];

            // Check if complement was seen before
            auto it = seen.find(complement);
            if (it != seen.end()) {
                return {it->second, i};
            }

            seen[nums[i]] = i;
        }

        return {}; // should never reach here
    }
};
```
