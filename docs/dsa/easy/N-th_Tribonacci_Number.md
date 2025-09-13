# Problem: N-th Tribonacci Number

## Summary of Approach

The N-th Tribonacci number can be calculated iteratively or recursively.  A recursive approach directly implements the Tribonacci definition (T(n) = T(n-1) + T(n-2) + T(n-3) with base cases T(0)=0, T(1)=1, T(2)=1), but suffers from significant redundancy in calculations.  An iterative approach avoids this redundancy by building up the Tribonacci sequence from the base cases, storing only the necessary previous three values at any given time. This iterative method is far more efficient for larger values of N.  Dynamic programming can also be used to store previously computed values to avoid redundant calculations, effectively mirroring the iterative approach's efficiency.

## Time and Space Complexity
- Time: O(n) - The iterative approach iterates through the sequence once, performing a constant amount of work at each step.  The recursive approach is O(3<sup>n</sup>) due to its exponential branching factor.
- Space: O(1) - The iterative approach uses a constant amount of extra space to store the three necessary previous values. The recursive approach's space complexity is O(n) due to the recursive call stack in the worst case.  A dynamic programming approach that stores all values up to n would have O(n) space complexity.

## Java Solution
```java
/*
N-th Tribonacci Number

Given an integer n, return the nth Tribonacci number.

The Tribonacci sequence Tn is defined as follows:

T0 = 0, T1 = 1, T2 = 1, and Tn+3 = Tn + Tn+1 + Tn+2 for n >= 0.

For example:
Input: n = 4
Output: 4
Explanation:
T_3 = 0 + 1 + 1 = 2
T_4 = 1 + 1 + 2 = 4

Difficulty: Easy
*/
class NthTribonacciNumber {
    public int tribonacci(int n) {
        if (n == 0) return 0;
        if (n == 1 || n == 2) return 1;

        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        dp[2] = 1;

        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3];
        }
        return dp[n];
    }
}
```