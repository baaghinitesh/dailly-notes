import java.util.*;

/*
Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid word in wordDict.
Return all such possible sentences.
Note that the same word in the dictionary may be reused multiple times in the segmentation.

Example 1:
Input: s = "catsanddog", wordDict = ["cat","cats","sand","and","dog"]
Output: ["cats and dog","cat sand dog"]

Example 2:
Input: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
Explanation: Note that you are allowed to reuse a dictionary word.

Example 3:
Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: []

Constraints:
1 <= s.length() <= 20
1 <= wordDict.length <= 1000
1 <= wordDict[i].length() <= 10
s and wordDict[i] consist of lowercase English letters.
All the strings of wordDict are unique.
*/
//Medium

class WordBreakII {
    public List<String> wordBreak(String s, List<String> wordDict) {
        return wordBreakHelper(s, wordDict, 0);
    }

    private List<String> wordBreakHelper(String s, List<String> wordDict, int start) {
        List<String> result = new ArrayList<>();
        if (start == s.length()) {
            result.add("");
            return result;
        }

        for (int end = start + 1; end <= s.length(); end++) {
            String word = s.substring(start, end);
            if (wordDict.contains(word)) {
                List<String> subResult = wordBreakHelper(s, wordDict, end);
                for (String sub : subResult) {
                    String sentence = word + (sub.isEmpty() ? "" : " " + sub);
                    result.add(sentence);
                }
            }
        }
        return result;
    }
}