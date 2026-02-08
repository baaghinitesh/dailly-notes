/*
Given a string word, return true if word is a valid abbreviation of a non-empty string.
Example 1:
Input: word = "leetcode"
Output: false
Explanation:
"leetcode" is not a valid abbreviation of any string.
Example 2:
Input: word = "lEetCodE"
Output: true
Explanation:
"lEetCodE" is a valid abbreviation of "leetCode".
Difficulty: Medium
*/
class DetectCapital {
    public boolean detectCapitalUse(String word) {
        int n = word.length();
        if (n == 0) return false;
        boolean allCaps = true;
        boolean allLower = true;
        boolean firstCapRestLower = true;

        for (int i = 0; i < n; i++) {
            char c = word.charAt(i);
            if (Character.isLowerCase(c)) allCaps = false;
            if (Character.isUpperCase(c)) allLower = false;
            if (i > 0 && Character.isUpperCase(c)) firstCapRestLower = false;
        }

        if (allCaps || allLower || (Character.isUpperCase(word.charAt(0)) && firstCapRestLower) ) return true;

        return false;
    }
}