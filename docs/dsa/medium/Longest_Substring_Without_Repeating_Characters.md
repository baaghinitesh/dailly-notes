# Problem: Longest Substring Without Repeating Characters

## Summary of Approach

The "Longest Substring Without Repeating Characters" problem aims to find the length of the longest substring within a given string that contains no repeating characters.  A sliding window approach is efficient for solving this.  We use two pointers, `left` and `right`, representing the start and end of the sliding window.  A `set` (or dictionary/hashmap) is used to track the characters currently within the window.

The algorithm iterates, expanding the window to the right (`right++`) as long as the next character is not already in the set.  If a repeating character is encountered, the window is contracted from the left (`left++`) until the repeating character is removed from the window (removed from the set).  The length of the longest substring is tracked throughout the process.


## Time and Space Complexity
- Time: O(n) - The algorithm iterates through the string at most twice (once expanding the window, and potentially again contracting it).  The set lookup and insertion operations are O(1) on average.
- Space: O(min(m, n)) - The space used by the set is proportional to the number of unique characters in the substring, where 'n' is the length of the input string and 'm' is the size of the character set (e.g., 256 for ASCII). In the worst case (all characters unique), it's O(n), while in the best case (all characters the same), it's O(1).  The space used is bounded by the minimum of the input string length and the size of the character set.

## Java Solution
```java
//Longest Substring Without Repeating Characters
//Difficulty: Medium

class LongestSubstringWithoutRepeatingCharacters {
    public int lengthOfLongestSubstring(String s) {
        int n = s.length();
        int ans = 0;
        Map<Character, Integer> map = new HashMap<>();
        int j = 0;
        for (int i = 0; i < n; i++) {
            if (map.containsKey(s.charAt(i))) {
                j = Math.max(j, map.get(s.charAt(i)) + 1);
            }
            map.put(s.charAt(i), i);
            ans = Math.max(ans, i - j + 1);
        }
        return ans;
    }
}
```