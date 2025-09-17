# Problem: Longest Palindrome

## Summary of Approach

The "Longest Palindrome" problem aims to find the longest palindromic substring within a given string.  Several approaches exist, but a common and efficient one uses a dynamic programming technique or a slightly optimized expansion around center approach.

**Dynamic Programming Approach:** This approach builds a table `dp` where `dp[i][j]` is true if the substring from index `i` to `j` is a palindrome, and false otherwise.  It iterates through the string, checking substrings of increasing length.  The base cases are single characters (which are palindromes) and two-character substrings.  For longer substrings, it checks if the characters at the ends are equal and if the inner substring (excluding the ends) is also a palindrome (this is checked using the `dp` table).  The longest palindrome's length is then easily determined.

**Expansion Around Center Approach:** This approach is often preferred for its slightly better space efficiency. It iterates through each character (and between each character pair) as a potential center of a palindrome. It then expands outwards from the center, checking for palindrome properties.  It keeps track of the longest palindrome found so far.  This method avoids the explicit creation of a large DP table.


## Time and Space Complexity
- **Time:** O(n^2) for both dynamic programming and expansion around center approaches.  The nested loops in the dynamic programming approach or the expanding outwards in the expansion around center approach lead to a quadratic time complexity.
- **Space:** O(n^2) for the dynamic programming approach due to the `dp` table of size n x n.  O(1) for the expansion around center approach because it only uses a few variables to track the longest palindrome found.

## Java Solution
```java
/*
Question: Longest Palindrome
Difficulty: Medium

Given a string s, find the longest palindromic substring in s.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"
*/
class LongestPalindrome {
    public String longestPalindrome(String s) {
        if (s == null || s.length() < 1) return "";
        int start = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {
            int len1 = expandAroundCenter(s, i, i);
            int len2 = expandAroundCenter(s, i, i + 1);
            int len = Math.max(len1, len2);
            if (len > end - start) {
                start = i - (len - 1) / 2;
                end = i + len / 2;
            }
        }
        return s.substring(start, end + 1);
    }

    private int expandAroundCenter(String s, int left, int right) {
        int L = left, R = right;
        while (L >= 0 && R < s.length() && s.charAt(L) == s.charAt(R)) {
            L--;
            R++;
        }
        return R - L - 1;
    }
}
```