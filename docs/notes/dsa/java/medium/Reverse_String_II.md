---
title: "Reverse String II"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/865/1200/630"
update_count: 0
---

# Reverse String II

## Problem Understanding
The problem is asking us to reverse every k-character substring within a given string, while keeping the overall order of the substrings intact. The key constraint here is that we need to reverse each substring of length k, but if the remaining characters are less than k, we should reverse them as well. What makes this problem non-trivial is that a naive approach of simply reversing the entire string or reversing each character individually would not work, as it would disrupt the order of the substrings.

## Approach
The algorithm strategy used here is to iterate through the string in steps of 2k, where k is the length of the substring to be reversed. For each step, we calculate the end index of the substring to be reversed, making sure it doesn't exceed the string length. We then use two pointers, one starting from the beginning of the substring and one from the end, to swap the characters and effectively reverse the substring. This approach works because it ensures that each substring of length k is reversed, while keeping the overall order of the substrings intact. The data structure used is a character array, which allows for efficient manipulation of the string.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm makes two passes through the string: one to convert the string to a character array and another to reverse the substrings. The reversal process involves swapping characters, which takes constant time. Since we're doing this for each character in the string, the overall time complexity is linear. |
| Space  | O(n)  | The algorithm uses a character array to store the characters of the string, which requires O(n) space. The space complexity is linear because we're storing each character in the array. |

## Algorithm Walkthrough
```
Input: s = "abcdefg", k = 2
Step 1: Convert the string to a character array: chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
Step 2: Calculate the end index for the first substring: end = min(0 + 2, 7) = 2
Step 3: Reverse the first substring: chars = ['b', 'a', 'c', 'd', 'e', 'f', 'g']
Step 4: Calculate the end index for the next substring: end = min(2 + 2, 7) = 4
Step 5: Reverse the next substring: chars = ['b', 'a', 'd', 'c', 'e', 'f', 'g']
Step 6: Calculate the end index for the next substring: end = min(4 + 2, 7) = 6
Step 7: Reverse the next substring: chars = ['b', 'a', 'd', 'c', 'f', 'e', 'g']
Output: "bacdfeg"
```
This walkthrough demonstrates the algorithm's step-by-step process for reversing the substrings.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Calculate end index}
    B -->|end = min("start + k, length")| C[Reverse substring]
    C --> D{"start + 2k < length"}
    D -->|Yes| E{Calculate next end index}
    E -->|end = min("start + 2k, length")| B
    D -->|No| F[Return result]
```
This flowchart illustrates the algorithm's decision flow and data transformation.

## Key Insight
> **Tip:** The key insight here is to recognize that we need to reverse each substring of length k, but also handle the case where the remaining characters are less than k.

## Edge Cases
- **Empty/null input**: If the input string is empty or null, the algorithm will return an empty string. This is because the algorithm checks for the length of the input string and handles it accordingly.
- **Single element**: If the input string has only one character, the algorithm will return the same string, as there's nothing to reverse.
- **k greater than string length**: If k is greater than the length of the string, the algorithm will simply reverse the entire string.

## Common Mistakes
- **Mistake 1**: Not handling the case where the remaining characters are less than k. To avoid this, we need to calculate the end index of the substring to be reversed and make sure it doesn't exceed the string length.
- **Mistake 2**: Not using a character array to store the characters of the string. This can lead to inefficient string manipulation and incorrect results.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still work correctly, as it only relies on the length of the substrings to be reversed, not on the order of the characters.
- "Can you do it in O(1) space?" → No, because we need to store the characters of the string in a character array, which requires O(n) space.
- "What if there are duplicates?" → The algorithm will still work correctly, as it only relies on the length of the substrings to be reversed, not on the uniqueness of the characters.

## Java Solution

```java
// Problem: Reverse String II
// Language: Java
// Difficulty: Medium
// Time Complexity: O(n) — two passes through the string
// Space Complexity: O(n) — StringBuilder stores the characters of the string
// Approach: StringBuilder substring reversal — reverse each substring of length k

public class Solution {
    public String reverseStr(String s, int k) {
        // Convert the string to a character array for easier manipulation
        char[] chars = s.toCharArray();
        
        // Loop through the string in steps of 2k
        for (int start = 0; start < s.length(); start += 2 * k) {
            // Calculate the end index, making sure it doesn't exceed the string length
            int end = Math.min(start + k, s.length());
            
            // Reverse the substring from start to end
            int left = start; // left pointer
            int right = end - 1; // right pointer
            while (left < right) {
                // Swap the characters at the left and right pointers
                char temp = chars[left];
                chars[left] = chars[right];
                chars[right] = temp;
                left++; // move the left pointer to the right
                right--; // move the right pointer to the left
            }
        }
        
        // Edge case: empty input → return empty string
        if (chars.length == 0) {
            return "";
        }
        
        // Convert the character array back to a string
        return new String(chars);
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.reverseStr("abcdefg", 2));  // "bacdfeg"
        System.out.println(solution.reverseStr("abcd", 2));  // "bacd"
    }
}
```
