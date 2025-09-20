# Problem: K Inverse Pairs Array

## Summary of Approach

The K Inverse Pairs Array problem aims to find the number of permutations of integers from 1 to n that have exactly k inverse pairs.  An inverse pair is a pair (i, j) such that i < j but P[i] > P[j], where P is a permutation.  A dynamic programming approach is efficient for solving this.

We can build a DP table `dp[i][j]` where `dp[i][j]` represents the number of permutations of integers from 1 to `i` with exactly `j` inverse pairs.  The base case is `dp[1][0] = 1` (one permutation of 1 element has 0 inversions).

We can iteratively compute `dp[i][j]` by considering the placement of the element `i`. When we add `i` to a permutation of `i-1` elements with `k` inversions, we can add `0` to `i-1` new inversions.  The number of inversions added depends on where `i` is placed in the existing permutation.  Therefore, the recurrence relation becomes:

`dp[i][j] = sum(dp[i-1][j-k])` for k from 0 to min(j, i-1)

This means we sum up the number of permutations of `i-1` elements with `j-k` inversions for all possible values of `k` (number of new inversions added by placing `i`).  The result `dp[i][j]` gives the number of permutations of `i` elements with `j` inverse pairs. Finally, we return `dp[n][k]`.  Optimization can be achieved by using modulo arithmetic to avoid integer overflow.


## Time and Space Complexity
- Time: O(n*k*n) or O(n*k) depending on implementation.  The naive approach is O(n*k*n) as there is a nested loop structure (outer loop iterates n times, inner loops iterate up to k times each, and the inner most summation has an upper bound of n). A space optimized approach using only two rows can reduce this to O(n*k).
- Space: O(n*k) for the DP table.  Can be reduced to O(k) using space optimization.

## Java Solution
```java
/*
K Inverse Pairs Array
Hard

Given an integer n and an integer k, return the number of arrays of length n such that the number of inverse pairs is equal to k.

An inverse pair is a pair of integers (i, j) such that i < j and a[i] > a[j].

Since the answer can be very large, return it modulo 109 + 7.


Example 1:

Input: n = 3, k = 0
Output: 1
Explanation: Only the array [1,2,3] has 0 inverse pairs.
Example 2:

Input: n = 3, k = 1
Output: 2
Explanation: The arrays [1,3,2] and [2,1,3] have 1 inverse pair.


Constraints:

1 <= n <= 1000
0 <= k <= 1000
*/
class KInversePairsArray {
    private static final int MOD = 1000000007;

    public int kInversePairs(int n, int k) {
        int[][] dp = new int[n + 1][k + 1];
        dp[0][0] = 1;

        for (int i = 1; i <= n; i++) {
            for (int j = 0; j <= k; j++) {
                for (int p = 0; p <= j && p < i; p++) {
                    dp[i][j] = (dp[i][j] + dp[i - 1][j - p]) % MOD;
                }
            }
        }
        return dp[n][k];
    }
}
```