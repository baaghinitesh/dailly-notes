## Summary of Approach

The problem "Detect Capital" asks to determine if a given string has all capital letters, all lowercase letters, or only the first letter is capitalized.  The solution iterates through the string.  It first checks if the first character is uppercase.  Then, it checks the rest of the string:

* **If the first character is uppercase:** It checks if the remaining characters are all lowercase. If not, it checks if the remaining characters are all uppercase.
* **If the first character is lowercase:** It checks if the remaining characters are all lowercase.


If any of these conditions (all uppercase, all lowercase, first uppercase rest lowercase) are true, the function returns `true`; otherwise, it returns `false`.


## Time and Space Complexity
- Time: O(n), where n is the length of the input string. The algorithm iterates through the string once.
- Space: O(1). The algorithm uses a constant amount of extra space regardless of the input string size.