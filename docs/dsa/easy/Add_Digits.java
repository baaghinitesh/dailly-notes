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