---
title: "Segment Tree with Lazy Propagation"
language: "cpp"
difficulty: "hard"
section: "dsa"
tags: "dsa, cpp, hard, segment-tree, lazy-propagation"
banner: "https://image.pollinations.ai/prompt/dsa%20Segment%20Tree%20with%20Lazy%20Propagation%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# Segment Tree with Lazy Propagation

![Lazy Segment Tree](https://image.pollinations.ai/prompt/dsa%20Segment%20Tree%20with%20Lazy%20Propagation%20programming%20abstract?width=1200&height=630&nologo=true)

## Approach
Extend the segment tree with a `lazy` array to defer range updates. When a range update is applied, mark the node as lazy instead of propagating immediately. Before accessing children, push the lazy value down. This reduces range updates from O(n) to O(log n).

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time (range update) | O(log n) | Lazy deferral |
| Time (range query)  | O(log n) | Push-down on access |
| Space               | O(n)     | Extra lazy array |

## Key Insight
> **Tip:** Always push down lazy before recursing into children. The invariant: `tree[node]` is correct for its range, but children may be stale until pushed.

## C++ Solution

```cpp
#include <vector>
using namespace std;

class LazySegTree {
    // Problem: Segment Tree with Lazy Propagation
    // Language: C++
    // Difficulty: Hard
    // Time Complexity: O(log n) per update/query
    // Space Complexity: O(n)

    int n;
    vector<long long> tree, lazy;

    void pushDown(int node, int start, int end) {
        if (lazy[node] != 0) {
            int mid = (start + end) / 2;
            int leftLen  = mid - start + 1;
            int rightLen = end - mid;
            // Apply lazy to children
            tree[2*node]   += lazy[node] * leftLen;
            tree[2*node+1] += lazy[node] * rightLen;
            lazy[2*node]   += lazy[node];
            lazy[2*node+1] += lazy[node];
            lazy[node] = 0; // clear
        }
    }

    void build(vector<int>& arr, int node, int s, int e) {
        if (s == e) { tree[node] = arr[s]; return; }
        int mid = (s + e) / 2;
        build(arr, 2*node, s, mid);
        build(arr, 2*node+1, mid+1, e);
        tree[node] = tree[2*node] + tree[2*node+1];
    }

    void update(int node, int s, int e, int l, int r, long long val) {
        if (r < s || e < l) return;
        if (l <= s && e <= r) {
            tree[node] += val * (e - s + 1);
            lazy[node] += val;
            return;
        }
        pushDown(node, s, e);
        int mid = (s + e) / 2;
        update(2*node, s, mid, l, r, val);
        update(2*node+1, mid+1, e, l, r, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }

    long long query(int node, int s, int e, int l, int r) {
        if (r < s || e < l) return 0;
        if (l <= s && e <= r) return tree[node];
        pushDown(node, s, e);
        int mid = (s + e) / 2;
        return query(2*node, s, mid, l, r) +
               query(2*node+1, mid+1, e, l, r);
    }

public:
    LazySegTree(vector<int>& arr) {
        n = arr.size();
        tree.assign(4*n, 0);
        lazy.assign(4*n, 0);
        build(arr, 1, 0, n-1);
    }

    void rangeAdd(int l, int r, long long val) { update(1, 0, n-1, l, r, val); }
    long long rangeSum(int l, int r)           { return query(1, 0, n-1, l, r); }
};
```
