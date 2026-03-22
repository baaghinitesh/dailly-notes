---
title: "Big O Notation: Measuring Time and Space Complexity"
topic: "Big O Notation: Measuring Time and Space Complexity"
section: "dsa"
tags: "dsa, complexity, big-o, algorithms, notes"
banner: "https://picsum.photos/seed/bigo-dsa/1200/630"
update_count: 0
---

![Big O Notation](https://picsum.photos/seed/bigo-dsa/1200/630)

## Introduction

Big O notation is the universal language for describing algorithm efficiency. It answers: *how does runtime or memory usage grow as input size grows?* Every serious programmer needs to internalize this — it's the first thing interviewers ask and the foundation of every optimization decision.

## Core Concepts

Big O describes the **upper bound** of growth rate, ignoring constants and lower-order terms.

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | Array index access, hash map lookup |
| O(log n) | Logarithmic | Binary search, balanced BST ops |
| O(n) | Linear | Single loop, linear search |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Recursive Fibonacci, subset generation |
| O(n!) | Factorial | Permutation generation |

### Growth Rate Visualization

```
n=10:    O(1)=1, O(log n)=3, O(n)=10, O(n²)=100, O(2ⁿ)=1024
n=100:   O(1)=1, O(log n)=7, O(n)=100, O(n²)=10000, O(2ⁿ)=huge
n=1000:  O(1)=1, O(log n)=10, O(n)=1000, O(n²)=1M, O(2ⁿ)=∞
```

## Code Examples

### O(1) — Constant Time

```java
// Array access is always O(1) regardless of array size
int getFirst(int[] arr) {
    return arr[0]; // one operation, always
}

// HashMap lookup is O(1) average
String getValue(Map<String, String> map, String key) {
    return map.get(key); // hash computed, bucket accessed
}
```

### O(log n) — Logarithmic

```java
// Binary search: halves the search space each step
int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2; // avoid overflow
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
// After each step: n → n/2 → n/4 → ... → 1
// Steps needed: log₂(n)
```

### O(n²) — Quadratic

```java
// Nested loops — classic O(n²)
boolean hasDuplicate(int[] arr) {
    for (int i = 0; i < arr.length; i++) {
        for (int j = i + 1; j < arr.length; j++) {
            if (arr[i] == arr[j]) return true; // O(n²) comparisons
        }
    }
    return false;
}
// Better: use HashSet → O(n)
```

## Space Complexity

Space complexity measures **extra memory** used (auxiliary space), not counting the input.

```java
// O(1) space — only a few variables
int sum(int[] arr) {
    int total = 0;          // O(1)
    for (int x : arr) total += x;
    return total;
}

// O(n) space — new array proportional to input
int[] doubled(int[] arr) {
    int[] result = new int[arr.length]; // O(n) extra space
    for (int i = 0; i < arr.length; i++) result[i] = arr[i] * 2;
    return result;
}

// O(n) space — recursion stack depth
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1); // n stack frames
}
```

## Common Pitfalls

> **Warning:** Don't confuse O(n) loops with O(n²). A loop inside a loop is O(n²) only if both iterate over n. If the inner loop is constant, it's still O(n).

```java
// This is O(n), NOT O(n²) — inner loop is constant (always 3 iterations)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < 3; j++) { // constant!
        process(i, j);
    }
}
```

> **Warning:** Recursive algorithms can have hidden space complexity from the call stack. A recursive DFS on a tree of depth h uses O(h) stack space.

## Summary / Key Takeaways

- Big O is about **growth rate**, not exact time — constants are dropped
- **O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)**
- Always analyze both **time** and **space** complexity
- For interviews: state complexity before coding, then verify after
- Aim for O(n) or O(n log n) — O(n²) is usually too slow for n > 10⁴
