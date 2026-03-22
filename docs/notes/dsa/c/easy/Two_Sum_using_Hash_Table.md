---
title: "Two Sum using Hash Table"
language: "c"
difficulty: "easy"
section: "dsa"
tags: "dsa, c, easy, hash-table, arrays"
banner: "https://picsum.photos/seed/twosum-c/1200/630"
update_count: 0
---

# Two Sum using Hash Table

![Two Sum C](https://picsum.photos/seed/twosum-c/1200/630)

## Approach
In C, implement a simple hash table with open addressing. For each element, compute `target - nums[i]` and check the hash table. If found, return both indices. Otherwise, insert the current number.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n) average | Hash table O(1) average lookup |
| Space  | O(n)         | Hash table entries |

## Key Insight
> **Tip:** In C, there's no built-in hash map. Use a fixed-size array as a hash table with modular hashing. Handle collisions with linear probing or chaining.

## C Solution

```c
// Problem: Two Sum using Hash Table
// Language: C
// Difficulty: Easy
// Time Complexity: O(n) average
// Space Complexity: O(n)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 20011  // prime number for better distribution

typedef struct {
    int key;
    int index;
    int used;
} Entry;

static Entry table[TABLE_SIZE];

static void table_clear() {
    memset(table, 0, sizeof(table));
}

static int hash(int key) {
    return ((long long)key % TABLE_SIZE + TABLE_SIZE) % TABLE_SIZE;
}

static void table_insert(int key, int idx) {
    int h = hash(key);
    while (table[h].used && table[h].key != key)
        h = (h + 1) % TABLE_SIZE;
    table[h].key   = key;
    table[h].index = idx;
    table[h].used  = 1;
}

static int table_find(int key) {
    int h = hash(key);
    while (table[h].used) {
        if (table[h].key == key) return table[h].index;
        h = (h + 1) % TABLE_SIZE;
    }
    return -1;
}

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    table_clear();
    int* result = (int*)malloc(2 * sizeof(int));
    *returnSize = 2;

    for (int i = 0; i < numsSize; i++) {
        int complement = target - nums[i];
        int found = table_find(complement);

        if (found != -1) {
            result[0] = found;
            result[1] = i;
            return result;
        }

        table_insert(nums[i], i);
    }

    *returnSize = 0;
    return result;
}
```
