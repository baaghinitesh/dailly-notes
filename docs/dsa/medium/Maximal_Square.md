# Problem: Maximal Square

## Summary of Approach

The Maximal Square problem aims to find the largest square submatrix containing only '1's within a given matrix of '0's and '1's.  A dynamic programming approach is highly efficient.  We create a DP table of the same size as the input matrix.  `dp[i][j]` stores the size of the largest square ending at (i, j).  If the current cell is '1', its value is 1 plus the minimum of the values above, to the left, and diagonally above and to the left in the DP table. This minimum represents the limiting factor in extending the square.  If the current cell is '0', the value is 0.  The maximum value in the DP table represents the side length of the maximal square, and its square is the maximal square's area.

## Time and Space Complexity
- Time: O(m*n) where 'm' and 'n' are the dimensions of the input matrix.  We iterate through the matrix once to build the DP table.
- Space: O(m*n) to store the DP table.  While we could potentially optimize space to O(min(m,n)) by using only one row or column of the DP table at a time, the standard DP solution uses the full table.

## Java Solution
```java
/*
Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.

Difficulty: Medium
*/
class MaximalSquare {
    public int maximalSquare(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }

        int m = matrix.length;
        int n = matrix[0].length;
        int[][] dp = new int[m + 1][n + 1];
        int maxSide = 0;

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1])) + 1;
                    maxSide = Math.max(maxSide, dp[i][j]);
                }
            }
        }

        return maxSide * maxSide;
    }
}
```