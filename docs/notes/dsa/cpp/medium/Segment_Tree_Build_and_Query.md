---
title: "Segment Tree Build and Query"
language: "cpp"
difficulty: "medium"
section: "dsa"
tags: "dsa, cpp, medium, segment-tree, range-query"
banner: "https://picsum.photos/seed/segtree-cpp/1200/630"
update_count: 0
---

# Segment Tree Build and Query

![Segment Tree](https://picsum.photos/seed/segtree-cpp/1200/630)

## Approach
Build a segment tree over an array to support range sum queries and point updates in O(log n). The tree is stored in a 1-indexed array of size 4n. Build bottom-up; query and update top-down with range splitting.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time (build)  | O(n)     | Visit each node once |
| Time (query)  | O(log n) | At most 4 nodes per level |
| Time (update) | O(log n) | Path from leaf to root |
| Space         | O(n)     | 4n array |

## Key Insight
> **Tip:** Use 1-based indexing. Node `i` has children `2i` and `2i+1`. This avoids off-by-one errors and makes the implementation cleaner.

## C++ Solution

```cpp
#include <vector>
using namespace std;

class SegmentTree {
    // Problem: Segment Tree Build and Query
    // Language: C++
    // Difficulty: Medium
    // Time Complexity: O(n) build, O(log n) query/update
    // Space Complexity: O(n)

    int n;
    vector<long long> tree;

    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2*node, start, mid);
            build(arr, 2*node+1, mid+1, end);
            tree[node] = tree[2*node] + tree[2*node+1]; // merge: sum
        }
    }

    long long query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0; // out of range
        if (l <= start && end <= r) return tree[node]; // fully in range
        int mid = (start + end) / 2;
        return query(2*node, start, mid, l, r) +
               query(2*node+1, mid+1, end, l, r);
    }

    void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
        } else {
            int mid = (start + end) / 2;
            if (idx <= mid) update(2*node, start, mid, idx, val);
            else            update(2*node+1, mid+1, end, idx, val);
            tree[node] = tree[2*node] + tree[2*node+1];
        }
    }

public:
    SegmentTree(vector<int>& arr) {
        n = arr.size();
        tree.assign(4 * n, 0);
        build(arr, 1, 0, n - 1);
    }

    long long query(int l, int r) { return query(1, 0, n-1, l, r); }
    void update(int idx, int val)  { update(1, 0, n-1, idx, val); }
};
```
