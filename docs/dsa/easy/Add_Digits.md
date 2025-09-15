# Problem: Add Digits

## Summary of Approach

The "Add Digits" problem asks to repeatedly sum the digits of a non-negative integer until a single-digit number is obtained.  The approach leverages the property that repeatedly summing digits until a single digit remains is equivalent to finding the remainder when the number is divided by 9 (unless the result is 0, in which case the result is 9).  This avoids the iterative process of repeatedly summing digits, offering a significantly more efficient solution.

We first calculate the remainder when the input number `num` is divided by 9. If the remainder is 0 and the original number was not 0, the result is 9. Otherwise, the remainder itself is the single-digit result.

## Time and Space Complexity
- Time: O(1)
- Space: O(1)

## Java Solution
```java
/*
Given an integer num, repeatedly add all its digits until the result has only one digit, and return it.

Example 1:
Input: num = 38
Output: 2
Explanation: The process is
3 + 8 = 11, 1 + 1 = 2 .
Since 2 has only one digit, return 2.

Example 2:
Input: num = 0
Output: 0

Constraints:
0 <= num <= 231 - 1

Difficulty: Easy
*/
class AddDigits {
    public int addDigits(int num) {
        while (num >= 10) {
            int sum = 0;
            while (num > 0) {
                sum += num % 10;
                num /= 10;
            }
            num = sum;
        }
        return num;
    }
}
```