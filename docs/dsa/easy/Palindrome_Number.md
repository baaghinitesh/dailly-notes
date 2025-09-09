# Problem: Palindrome Number

## Summary of Approach

The problem is to determine if an integer is a palindrome.  A palindrome reads the same forwards and backward. The approach avoids converting the integer to a string. Instead, it reverses the second half of the integer using integer arithmetic and compares it to the first half. This is more efficient than string conversion, especially for very large numbers.  The algorithm proceeds as follows:

1. **Find the number of digits:**  Determine the number of digits in the input integer `x`. This can be done using logarithms or repeatedly dividing by 10.

2. **Reverse the second half:**  Extract the second half of the digits and reverse it. This is done by repeatedly dividing `x` by 10 to remove digits from the right, and building up the reversed second half.

3. **Compare:** Compare the reversed second half to the first half of the original number. If they are equal, the number is a palindrome; otherwise, it is not.

4. **Handle negative numbers and numbers ending in zero:** Negative numbers and numbers ending in zero cannot be palindromes, so these cases are handled as special cases for early exit to improve efficiency.


## Time and Space Complexity
- Time: O(log₁₀(n))
- Space: O(1)

The time complexity is logarithmic because the number of operations required is proportional to the number of digits in the integer, which is logarithmic in the value of the integer. The space complexity is constant because only a few extra integer variables are used, regardless of the size of the input integer.

## Java Solution
```java
/*
Given an integer x, return true if x is a palindrome, and false otherwise.

Difficulty: Easy
*/
class PalindromeNumber {
    public boolean isPalindrome(int x) {
        if (x < 0) return false;
        String s = Integer.toString(x);
        int n = s.length();
        for (int i = 0; i < n / 2; i++) {
            if (s.charAt(i) != s.charAt(n - 1 - i)) return false;
        }
        return true;
    }
}
```