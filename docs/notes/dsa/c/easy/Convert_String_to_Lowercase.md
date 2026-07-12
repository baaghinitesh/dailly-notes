---
title: "Convert String to Lowercase"
language: "c"
difficulty: "easy"
section: "dsa"
tags: "dsa, c, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/235/1200/630"
update_count: 0
---

# Convert String to Lowercase

## Problem Understanding
The problem requires converting a given string to lowercase, meaning all uppercase characters in the string should be converted to their corresponding lowercase characters. The key constraint is that the conversion should be done in-place, meaning no extra space should be used other than the input string itself. This problem is non-trivial because a naive approach might involve creating a new string and copying the converted characters into it, which would use extra space. However, the requirement to modify the input string in-place makes the problem slightly more challenging.

## Approach
The algorithm strategy is to iterate through each character in the input string and check if it's an uppercase character. If it is, the character is converted to lowercase using the `tolower` function from the `ctype.h` library. This approach works because the `isupper` function can accurately identify uppercase characters, and `tolower` can convert them to lowercase. The `strlen` function is used to determine the length of the input string, allowing the algorithm to iterate through all characters. The input string is modified in-place, satisfying the space complexity constraint.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The algorithm iterates through each character in the string once, where n is the length of the string. The operations within the loop (checks and conversions) take constant time. |
| Space  | O(1)  | The algorithm modifies the input string in-place and does not use any data structures that scale with the input size, thus using constant space. |

## Algorithm Walkthrough
```
Input: "Hello"
Step 1: i = 0, str[i] = 'H' (isupper('H') == 1), convert 'H' to 'h'
Step 2: i = 1, str[i] = 'e' (isupper('e') == 0), no conversion needed
Step 3: i = 2, str[i] = 'l' (isupper('l') == 0), no conversion needed
Step 4: i = 3, str[i] = 'l' (isupper('l') == 0), no conversion needed
Step 5: i = 4, str[i] = 'o' (isupper('o') == 0), no conversion needed
Output: "hello"
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is input string NULL?"}
    B -->|Yes| C[Return NULL]
    B -->|No| D["Initialize i = 0"]
    D --> E{"Is i < strlen(str)?"}
    E -->|Yes| F["Check if str[i"] is uppercase]
    F -->|Yes| G["Convert str[i"] to lowercase]
    F -->|No| H[No conversion needed]
    G --> I[Increment i]
    H --> I
    I --> E
    E -->|No| J[Return modified string]
```

## Key Insight
> **Tip:** The key to solving this problem efficiently is recognizing that the `isupper` and `tolower` functions can be used to check and convert characters in a single pass through the string, allowing for in-place modification.

## Edge Cases
- **Empty string**: If the input string is empty, `strlen` returns 0, and the loop does not execute. The function returns the original empty string, which is the expected behavior.
- **Single character**: If the input string consists of a single character, the loop executes once. If the character is uppercase, it is converted to lowercase; otherwise, it remains unchanged.
- **NULL input**: If the input string is NULL, the function immediately returns NULL, avoiding potential segmentation faults or other errors.

## Common Mistakes
- **Mistake 1**: Not checking if the input string is NULL before attempting to access its contents. → This can be avoided by adding a simple NULL check at the beginning of the function.
- **Mistake 2**: Using an incorrect loop condition or not incrementing the loop counter correctly. → This can be avoided by carefully crafting the loop condition and ensuring the counter is updated correctly within the loop.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The sorting of the input does not affect the algorithm since it iterates through each character individually, regardless of the string's sorted status.
- "Can you do it in O(1) space?" → The algorithm already achieves O(1) space complexity by modifying the input string in-place.
- "What if there are duplicates?" → The presence of duplicate characters (either uppercase or lowercase) does not impact the algorithm's correctness or efficiency, as each character is processed individually.

## C Solution

```c
// Problem: Convert String to Lowercase
// Language: C
// Difficulty: Easy
// Time Complexity: O(n) — single pass through string
// Space Complexity: O(1) — no extra space used, modifying input in-place
// Approach: character-wise case conversion — for each character, check if it's uppercase and convert if necessary

#include <ctype.h>
#include <string.h>

char* toLowerCase(char *str) {
    // Check if input string is NULL: return NULL
    if (str == NULL) return NULL;
    
    // Iterate through each character in the string
    for (int i = 0; i < strlen(str); i++) {
        // Check if the character is uppercase: convert to lowercase if so
        if (isupper(str[i])) {
            // Convert to lowercase using the tolower function
            str[i] = tolower(str[i]);
        }
        // No need to explicitly handle non-uppercase characters
    }
    
    // Return the modified string
    return str;
}
```
