# Problem: Power of Three

## Summary of Approach

The "Power of Three" problem asks whether a given integer `n` is a power of three.  The most efficient approach leverages the properties of base-3 logarithms and integer division.  We can repeatedly divide `n` by 3 until either `n` becomes 1 (indicating it's a power of 3) or `n` is no longer divisible by 3 (indicating it's not a power of 3).  Alternatively, a more concise solution uses the fact that powers of 3 are the only integers that are divisible by 3 repeatedly until they become 1.  This can be checked by repeatedly dividing by 3 and verifying the remainder is always 0, finally checking if the result is 1.  Another approach uses a lookup table for powers of 3 within a reasonable range, but this is less efficient for very large inputs.


## Time and Space Complexity
- Time: O(log₃n)  The number of divisions by 3 is proportional to the base-3 logarithm of n.  In the worst case, it's logarithmic with respect to the input.
- Space: O(1) The algorithm uses a constant amount of extra space, regardless of the input size.

## Java Solution
```java
/*
Given an integer n, return true if it is a power of three. Otherwise, return false.

An integer n is a power of three, if there exists an integer x such that n == 3x.

Example 1:
Input: n = 27
Output: true

Example 2:
Input: n = 0
Output: false

Example 3:
Input: n = 9
Output: true

Constraints:
-231 <= n <= 231 - 1

Difficulty: Easy
*/
class PowerOfThree {
    public boolean isPowerOfThree(int n) {
        if (n <= 0) return false;
        while (n % 3 == 0) {
            n /= 3;
        }
        return n == 1;
    }
}
```