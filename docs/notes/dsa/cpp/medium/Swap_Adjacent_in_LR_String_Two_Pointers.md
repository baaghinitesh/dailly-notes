---
title: "Swap Adjacent in LR String Two Pointers"
language: "cpp"
difficulty: "medium"
section: "dsa"
tags: "dsa, cpp, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/978/1200/630"
update_count: 0
---

# Swap Adjacent in LR String Two Pointers

## Problem Understanding
The problem asks to determine if it is possible to transform a given string `start` into another string `end` by swapping adjacent characters 'L' and 'R' in `start`. The key constraint is that the strings have the same length, and the transformation should only involve swapping adjacent characters. What makes this problem non-trivial is that the naive approach of trying all possible swaps would result in exponential time complexity, making it inefficient for large strings.

## Approach
The algorithm strategy is to use two pointers, `i` and `j`, to track the current position in the `start` and `end` strings, respectively. The intuition behind this approach is to compare the characters at the current positions in both strings and decide whether to move the pointers forward or swap the adjacent characters in `start`. This approach works because it ensures that the transformation is done in a way that minimizes the number of swaps, and the use of two pointers allows for an efficient comparison of the characters in both strings. The algorithm uses a simple conditional statement to handle the key constraints and decide the next step.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm makes a single pass through the string, where n is the length of the string. The while loop iterates over each character in the string, and the conditional statements inside the loop take constant time. |
| Space  | O(1)  | The algorithm uses a constant amount of space to store the pointers and the strings, regardless of the input size. The input strings are not modified, and no additional data structures are used. |

## Algorithm Walkthrough
```
Input: start = "RXXLRXRXL", end = "XRLXXRRLX"
Step 1: i = 0, j = 0, start[i] = 'R', end[j] = 'X'
Step 2: i = 0, j = 0, start[i] = 'R', end[j] = 'X', start[i + 1] = 'X', end[j + 1] = 'R'
Step 3: i = 2, j = 2, start[i] = 'X', end[j] = 'L'
Step 4: i = 2, j = 2, start[i] = 'X', end[j] = 'L', start[i + 1] = 'L', end[j + 1] = 'R'
Step 5: i = 4, j = 4, start[i] = 'R', end[j] = 'R'
...
Output: "YES"
```
This example demonstrates how the algorithm compares the characters in the `start` and `end` strings and decides whether to move the pointers forward or swap the adjacent characters in `start`.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Compare start[i] and end[j]"}
    B -->|start[i] == end[j]| C[Move pointers forward]
    B -->|start[i] == 'L' and end["j + 1"] == 'R'| D{Check if swap is possible}
    D -->|Swap is possible| E[Swap adjacent characters]
    D -->|Swap is not possible| F[Return ""]
    B -->|start[i] == 'R' and end["j + 1"] == 'L'| D
    C --> A
    E --> A
    F -->|End|
```
This flowchart illustrates the decision-making process of the algorithm, showing how it compares the characters in the `start` and `end` strings and decides whether to move the pointers forward or swap the adjacent characters in `start`.

## Key Insight
> **Tip:** The key insight is to use two pointers to track the current position in the `start` and `end` strings, allowing for an efficient comparison of the characters and decision-making process.

## Edge Cases
- **Empty/null input**: If either `start` or `end` is empty, the algorithm returns an empty string.
- **Single element**: If both `start` and `end` have a single element, the algorithm returns "YES" if the elements are the same, and an empty string otherwise.
- **Start and end strings have different lengths**: The algorithm returns an empty string if the lengths of `start` and `end` are different.

## Common Mistakes
- **Mistake 1**: Not checking if the lengths of `start` and `end` are the same before proceeding with the algorithm.
- **Mistake 2**: Not handling the case where the swap is not possible, resulting in an incorrect output.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm would still work correctly, but the number of swaps required would be minimized.
- "Can you do it in O(1) space?" → The algorithm already uses O(1) space, as it only uses a constant amount of space to store the pointers and the strings.
- "What if there are duplicates?" → The algorithm would still work correctly, as it compares the characters in the `start` and `end` strings and decides whether to move the pointers forward or swap the adjacent characters in `start` based on the comparison.

## CPP Solution

```cpp
// Problem: Swap Adjacent in LR String Two Pointers
// Language: cpp
// Difficulty: Medium
// Time Complexity: O(n) — single pass through the string
// Space Complexity: O(n) — string manipulation
// Approach: Two pointers — use two pointers to track 'L' and 'R' and swap them if they are adjacent

class Solution {
public:
    string swapAdjacentInLRString(string start, string end) {
        // Check if the strings have the same length
        if (start.length() != end.length()) {
            return "";
        }

        int n = start.length();
        int i = 0; // Pointer for the start string
        int j = 0; // Pointer for the end string

        while (i < n) {
            // If the current characters are the same, move both pointers forward
            if (start[i] == end[j]) {
                i++;
                j++;
            } 
            // If the current character in start is 'L' and the next character in end is 'R', 
            // then we need to swap the adjacent characters in start
            else if (start[i] == 'L' && j + 1 < n && end[j + 1] == 'R') {
                // Check if we can swap the adjacent characters in start
                if (i + 1 < n && start[i + 1] == 'R' && end[j] == 'L') {
                    i += 2; // Move the pointer two steps forward
                    j += 2;
                } 
                // If we cannot swap the adjacent characters in start, return ""
                else {
                    return "";
                }
            } 
            // If the current character in start is 'R' and the next character in end is 'L', 
            // then we need to swap the adjacent characters in start
            else if (start[i] == 'R' && j + 1 < n && end[j + 1] == 'L') {
                // Check if we can swap the adjacent characters in start
                if (i + 1 < n && start[i + 1] == 'L' && end[j] == 'R') {
                    i += 2; // Move the pointer two steps forward
                    j += 2;
                } 
                // If we cannot swap the adjacent characters in start, return ""
                else {
                    return "";
                }
            } 
            // If none of the above conditions are met, return ""
            else {
                return "";
            }
        }

        // If we have processed all characters in start and end, return "YES"
        return "YES";
    }
};
```
