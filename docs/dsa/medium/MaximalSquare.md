## Summary of Approach

The "Maximal Square" problem aims to find the largest square submatrix containing only '1's within a given matrix of '0's and '1's.  A dynamic programming approach is highly efficient.  We create a DP table of the same dimensions as the input matrix.  `dp[i][j]` stores the size of the largest square ending at position `(i, j)`.

The DP table is populated iteratively.  If the current cell `matrix[i][j]` is '1', the size of the square ending at this cell is 1 plus the minimum of the sizes of squares ending at the cells directly above, to the left, and diagonally above-left (`dp[i-1][j]`, `dp[i][j-1]`, `dp[i-1][j-1]`).  If `matrix[i][j]` is '0', then `dp[i][j]` is 0. The maximum value in the `dp` table represents the side length of the maximal square, and its square is the maximal square's area.


## Time and Space Complexity
- Time: O(m*n) where 'm' and 'n' are the dimensions of the input matrix.  We iterate through the matrix once to populate the DP table.
- Space: O(m*n)  The space is dominated by the DP table we create, which has the same dimensions as the input matrix.  We could potentially optimize space to O(n) if we only keep track of the previous row, but this would make the code slightly more complex.