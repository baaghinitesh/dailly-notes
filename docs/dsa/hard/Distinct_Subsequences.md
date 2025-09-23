# Problem: Distinct Subsequences

## Summary of Approach

The Distinct Subsequences problem aims to count the number of distinct subsequences of a given string `s` that are equal to another given string `t`.  A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

A dynamic programming approach is efficient for solving this. We create a 2D array `dp` where `dp[i][j]` represents the number of distinct subsequences of `s[0...i-1]` that are equal to `t[0...j-1]`.

- We initialize `dp[i][0] = 1` for all `i` because the empty subsequence is always a subsequence.
- We initialize `dp[0][j] = 0` for all `j > 0` because an empty string cannot form any non-empty subsequence.

Then, we iterate through the strings `s` and `t`.  If `s[i-1]` is equal to `t[j-1]`, it means we can extend the subsequences ending at `t[j-2]` by appending `s[i-1]`.  Therefore, `dp[i][j] = dp[i-1][j] + dp[i-1][j-1]`.  If they are not equal, we only consider the subsequences that don't use `s[i-1]`, so `dp[i][j] = dp[i-1][j]`.


Finally, `dp[s.length()][t.length()]` contains the total number of distinct subsequences of `s` that are equal to `t`.

## Time and Space Complexity
- Time: O(s.length() * t.length())  The dynamic programming approach iterates through the entire `dp` table.
- Space: O(s.length() * t.length()) We use a 2D array to store the results of subproblems.  This could be optimized to O(min(s.length(), t.length())) using space optimization techniques that only store the previous row.

## Java Solution
```java
// Question: Given two strings s and t, return the number of distinct subsequences of s which equals t.
// Difficulty: Hard

class DistinctSubsequences {
    public int numDistinct(String s, String t) {
        int m = s.length();
        int n = t.length();

        if (m < n) {
            return 0;
        }

        long[][] dp = new long[m + 1][n + 1];

        for (int i = 0; i <= m; i++) {
            dp[i][0] = 1;
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (s.charAt(i - 1) == t.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
                } else {
                    dp[i][j] = dp[i - 1][j];
                }
            }
        }

        return (int) dp[m][n];
    }
}
```