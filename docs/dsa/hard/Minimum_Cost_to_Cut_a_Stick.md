# Problem: Minimum Cost to Cut a Stick

## Summary of Approach

The "Minimum Cost to Cut a Stick" problem involves finding the minimum cost to cut a stick of length `n` into smaller pieces at specified cut points.  The approach typically uses dynamic programming.  We can represent the problem recursively:  The minimum cost to cut a stick from `i` to `j` is the minimum of cutting at each possible point `k` between `i` and `j`, plus the cost of that cut (which is the length of the stick from `i` to `j`), plus the minimum cost to cut the two resulting sub-sticks (`i` to `k` and `k` to `j`).  

A dynamic programming solution avoids redundant calculations by storing the minimum cost for each sub-problem (cutting a sub-stick from `i` to `j`). We iterate through possible cut points and build up the solution from smaller sub-problems to larger ones, finally arriving at the minimum cost to cut the entire stick.  Memoization (top-down) or tabulation (bottom-up) can be employed to efficiently store and reuse these results.


## Time and Space Complexity
- Time: O(n^3)  or O(n^2) depending on implementation
- Space: O(n^2)

**Explanation:**

* **Time Complexity:** The naive recursive approach without memoization would have exponential time complexity due to repeated subproblems.  With dynamic programming, we solve each subproblem only once.  The number of subproblems is O(n^2) because we consider all possible pairs of indices `i` and `j` to define the sub-sticks. For each subproblem, we iterate through all possible cut points `k`, which takes at most O(n) time in the worst case. Therefore, the total time complexity is O(n^3).  However, if we optimize the cut point search, for example, only considering cuts at the pre-defined cut points, the time complexity can be reduced to O(n^2).

* **Space Complexity:** The space complexity comes primarily from the DP table used to store the minimum costs for each subproblem.  This table has dimensions n x n, resulting in O(n^2) space complexity.  The recursive approach with memoization also uses O(n^2) space for the memoization table.

## Java Solution
```java
// Minimum Cost to Cut a Stick
// Difficulty: Medium

import java.util.Arrays;

class MinimumCostToCutAStick {
    public int minCost(int n, int[] cuts) {
        Arrays.sort(cuts);
        int[] newCuts = new int[cuts.length + 2];
        newCuts[0] = 0;
        System.arraycopy(cuts, 0, newCuts, 1, cuts.length);
        newCuts[newCuts.length - 1] = n;

        int len = newCuts.length;
        int[][] dp = new int[len][len];

        for (int i = len - 1; i >= 0; i--) {
            for (int j = i + 1; j < len; j++) {
                int minCost = Integer.MAX_VALUE;
                for (int k = i + 1; k < j; k++) {
                    minCost = Math.min(minCost, dp[i][k] + dp[k][j] + newCuts[j] - newCuts[i]);
                }
                dp[i][j] = minCost;
            }
        }
        return dp[0][len - 1];
    }
}
```