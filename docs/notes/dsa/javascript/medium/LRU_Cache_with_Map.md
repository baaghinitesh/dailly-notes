---
title: "LRU Cache with Map"
language: "javascript"
difficulty: "medium"
section: "dsa"
tags: "dsa, javascript, medium, lru-cache, map, design"
banner: "https://picsum.photos/seed/lrucache-js/1200/630"
update_count: 0
---

# LRU Cache with Map

![LRU Cache JavaScript](https://picsum.photos/seed/lrucache-js/1200/630)

## Approach
JavaScript's `Map` maintains insertion order, making it perfect for LRU. On `get`, delete and re-insert the key to move it to the end (most recently used). On `put`, if at capacity, delete the first key (least recently used = `map.keys().next().value`).

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time (get) | O(1) | Map lookup + delete + insert |
| Time (put) | O(1) | Map insert + optional eviction |
| Space      | O(capacity) | Map bounded by capacity |

## Key Insight
> **Tip:** JavaScript `Map` preserves insertion order. The first key is always the LRU. This eliminates the need for a doubly linked list that you'd need in Java/C++.

## JavaScript Solution

```javascript
// Problem: LRU Cache with Map
// Language: JavaScript
// Difficulty: Medium
// Time Complexity: O(1) per get/put
// Space Complexity: O(capacity)

class LRUCache {
    constructor(capacity) {
        this.capacity = capacity;
        this.cache = new Map(); // maintains insertion order
    }

    get(key) {
        if (!this.cache.has(key)) return -1;

        // Move to end (most recently used)
        const val = this.cache.get(key);
        this.cache.delete(key);
        this.cache.set(key, val);
        return val;
    }

    put(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key); // remove old position
        } else if (this.cache.size >= this.capacity) {
            // Evict LRU: first key in Map
            const lruKey = this.cache.keys().next().value;
            this.cache.delete(lruKey);
        }
        this.cache.set(key, value); // insert at end (MRU)
    }
}
```
