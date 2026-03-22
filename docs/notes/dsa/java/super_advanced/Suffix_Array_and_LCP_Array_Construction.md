---
title: "Suffix Array and LCP Array Construction"
language: "java"
difficulty: "super_advanced"
section: "dsa"
tags: "dsa, java, super-advanced, suffix-array, string-algorithms"
banner: "https://picsum.photos/seed/suffixarray-java/1200/630"
update_count: 0
---

# Suffix Array and LCP Array Construction

![Suffix Array](https://picsum.photos/seed/suffixarray-java/1200/630)

## Approach
Build a suffix array in O(n log n) using prefix doubling (Manber-Myers). Then compute the LCP (Longest Common Prefix) array in O(n) using Kasai's algorithm. The suffix array sorts all suffixes lexicographically; the LCP array stores the length of the longest common prefix between consecutive suffixes in sorted order.

## Complexity Analysis
| Metric | Value | Reason |
|--------|-------|--------|
| Time   | O(n log n) | Prefix doubling with radix sort |
| Space  | O(n)       | Suffix array, rank, and LCP arrays |

## Key Insight
> **Tip:** Kasai's algorithm exploits the property that if `LCP[rank[i]] = k`, then `LCP[rank[i+1]] >= k-1`. This lets you compute the entire LCP array in a single O(n) pass.

## Edge Cases
- Single character string → suffix array = [0], LCP = [0]
- All same characters → LCP values are n-1, n-2, ..., 0
- Empty string → handle separately

## Java Solution

```java
import java.util.Arrays;

class SuffixArray {
    // Problem: Suffix Array and LCP Array Construction
    // Language: Java
    // Difficulty: Super Advanced
    // Time Complexity: O(n log n)
    // Space Complexity: O(n)

    // Build suffix array using O(n log n) prefix doubling
    public static int[] buildSuffixArray(String s) {
        int n = s.length();
        Integer[] sa = new Integer[n];
        int[] rank = new int[n];
        int[] tmp = new int[n];

        // Initialize: rank by first character
        for (int i = 0; i < n; i++) {
            sa[i] = i;
            rank[i] = s.charAt(i);
        }

        for (int gap = 1; gap < n; gap *= 2) {
            final int[] r = rank.clone();
            final int g = gap;

            // Sort by (rank[i], rank[i+gap])
            Arrays.sort(sa, (a, b) -> {
                if (r[a] != r[b]) return r[a] - r[b];
                int ra = a + g < n ? r[a + g] : -1;
                int rb = b + g < n ? r[b + g] : -1;
                return ra - rb;
            });

            // Recompute ranks
            tmp[sa[0]] = 0;
            for (int i = 1; i < n; i++) {
                tmp[sa[i]] = tmp[sa[i - 1]];
                int prev = sa[i - 1], curr = sa[i];
                int rPrev = prev + g < n ? r[prev + g] : -1;
                int rCurr = curr + g < n ? r[curr + g] : -1;
                if (r[prev] != r[curr] || rPrev != rCurr) tmp[sa[i]]++;
            }
            System.arraycopy(tmp, 0, rank, 0, n);
        }

        int[] result = new int[n];
        for (int i = 0; i < n; i++) result[i] = sa[i];
        return result;
    }

    // Build LCP array using Kasai's O(n) algorithm
    public static int[] buildLCP(String s, int[] sa) {
        int n = s.length();
        int[] rank = new int[n];
        int[] lcp = new int[n];

        // Inverse suffix array
        for (int i = 0; i < n; i++) rank[sa[i]] = i;

        int h = 0;
        for (int i = 0; i < n; i++) {
            if (rank[i] > 0) {
                int j = sa[rank[i] - 1]; // previous suffix in sorted order
                // Extend common prefix
                while (i + h < n && j + h < n && s.charAt(i + h) == s.charAt(j + h)) h++;
                lcp[rank[i]] = h;
                if (h > 0) h--; // key: LCP can only decrease by 1
            }
        }
        return lcp;
    }

    public static void main(String[] args) {
        String s = "banana";
        int[] sa = buildSuffixArray(s);
        int[] lcp = buildLCP(s, sa);

        System.out.println("Suffix Array:");
        for (int i : sa) System.out.print(i + " "); // 5 3 1 0 4 2
        System.out.println("\nLCP Array:");
        for (int l : lcp) System.out.print(l + " "); // 0 1 3 0 0 2
    }
}
```
