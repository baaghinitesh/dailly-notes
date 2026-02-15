// Maximize Score After N Operations
// Difficulty: Hard

import java.util.*;

class MaximizeScoreAfterNOperations {
    public int maximizeScore(int[] nums) {
        int n = nums.length;
        if (n == 0) return 0;
        int m = n / 2;
        int[] pairs = new int[1 << n];
        int pairCount = 0;
        for (int i = 0; i < (1 << n); i++) {
            List<Integer> subset = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if ((i >> j) % 2 == 1) {
                    subset.add(j);
                }
            }
            if (subset.size() % 2 == 0 && subset.size() > 0) {
                pairs[pairCount++] = i;
            }
        }
        
        int[][] dp = new int[m + 1][1 << n];
        
        for(int i = 1; i <= m; ++i){
            for(int j = 0; j < pairCount; ++j){
                int mask = pairs[j];
                int score = 0;
                List<Integer> subset = new ArrayList<>();
                for(int k = 0; k < n; ++k){
                    if((mask >> k) % 2 == 1){
                        subset.add(k);
                    }
                }
                
                int gcd = 0;
                for(int k = 0; k < subset.size(); k+=2){
                    int a = nums[subset.get(k)];
                    int b = nums[subset.get(k+1)];
                    gcd = gcd(a,b);
                    score += gcd;
                }
                
                for(int prevMask = 0; prevMask < (1 << n); ++prevMask){
                    if((prevMask & mask) == 0){
                        dp[i][mask] = Math.max(dp[i][mask], dp[i-1][prevMask] + score);
                    }
                }
            }
        }
        
        int maxScore = 0;
        for(int i = 0; i < (1 << n); ++i){
            maxScore = Math.max(maxScore, dp[m][i]);
        }
        return maxScore;
    }
    
    private int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }
}