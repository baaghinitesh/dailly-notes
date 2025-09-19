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