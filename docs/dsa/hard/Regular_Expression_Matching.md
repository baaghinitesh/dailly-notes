# Problem: Regular Expression Matching

## Summary of Approach

The Regular Expression Matching problem aims to determine if a given regular expression (regex) matches a given string.  A dynamic programming approach is commonly used to solve this efficiently.  We create a DP table `dp[i][j]` where `dp[i][j]` is `True` if the first `i` characters of the string match the first `j` characters of the regex, and `False` otherwise.

The base case is `dp[0][0] = True` (empty string matches empty regex).  We then iterate through the table, considering each character of the string and each character/symbol of the regex.  The logic for filling the table involves several cases:

* **If the regex character is a literal character:** It must match the corresponding string character.
* **If the regex character is a '.' (dot):** It matches any single character.
* **If the regex character is a '*' (star):** This represents zero or more occurrences of the preceding character.  We have two choices: either the preceding character is matched zero times (we move only in the regex), or it is matched one or more times (we move in both the string and regex, and recursively check for more matches).


The final result, `dp[m][n]` (where `m` is the length of the string and `n` is the length of the regex), indicates whether the entire string matches the entire regex.


## Time and Space Complexity
- Time: O(mn) where 'm' is the length of the string and 'n' is the length of the regular expression.  This is because we iterate through an m x n DP table.
- Space: O(mn)  The space complexity is dominated by the DP table itself.  While some optimizations can reduce the space to O(min(m, n)) by using only one row or column of the table at a time, the standard DP solution uses the full table.

## Java Solution
```java
/*
Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*'.

'.' Matches any single character.
'*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Example 1:

Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".
Example 2:

Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
Example 3:

Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more (*) of any character (.)".
Example 4:

Input: s = "aab", p = "c*a*b"
Output: true
Explanation: c can be repeated 0 times, a can be repeated 1 time. Therefore it matches "aab".
Example 5:

Input: s = "mississippi", p = "mis*is*p*."
Output: false


Constraints:

0 <= s.length() <= 20
0 <= p.length() <= 30
s contains only lowercase English letters.
p contains only lowercase English letters, '.' and '*'.

Difficulty: Hard
*/
class RegularExpressionMatching {
    public boolean isMatch(String s, String p) {
        int m = s.length();
        int n = p.length();

        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;

        for (int j = 1; j <= n; j++) {
            if (p.charAt(j - 1) == '*') {
                dp[0][j] = dp[0][j - 2];
            }
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (p.charAt(j - 1) == '.' || p.charAt(j - 1) == s.charAt(i - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (p.charAt(j - 1) == '*') {
                    dp[i][j] = dp[i][j - 2]; //Match zero occurrences
                    if (p.charAt(j - 2) == '.' || p.charAt(j - 2) == s.charAt(i - 1)) {
                        dp[i][j] = dp[i][j] | dp[i - 1][j]; //Match one or more occurrences
                    }
                }
            }
        }
        return dp[m][n];
    }
}
```