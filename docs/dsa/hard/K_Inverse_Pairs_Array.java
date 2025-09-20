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