---
title: "Defanging an IP Address"
language: "java"
difficulty: "easy"
section: "dsa"
tags: "dsa, java, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/167/1200/630"
update_count: 0
---

# Defanging an IP Address

## Problem Understanding
The problem is asking to defang an IP address, which means replacing every dot (`.`) in the IP address with its defanged version, i.e., `[.]`. The key constraint is to achieve this in a single pass through the string, implying an efficient time complexity. What makes this problem non-trivial is the need to handle edge cases such as null or empty input strings and to ensure the solution works for all possible valid IP addresses. The naive approach of manually iterating through the string and appending characters to a new string could work but might be less efficient or more prone to errors compared to using built-in string replacement methods.

## Approach
The algorithm strategy used here is string replacement, where each dot in the IP address is replaced with its defanged version, `[.]`. This approach works because the `replaceAll()` method in Java returns a copy of the string where all occurrences of a substring are replaced with another substring. The intuition behind this is to leverage Java's built-in string manipulation capabilities to efficiently achieve the desired outcome. A `String` object is used to store the input and the result, chosen for its ability to handle string operations such as replacement. This approach handles key constraints by first checking for null or empty input strings and then applying the replacement rule to all dots in the address.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The time complexity is linear because the `replaceAll()` method iterates through the string once, where n is the length of the input string. Each character is examined once to determine if it matches the pattern to be replaced. |
| Space  | O(n)  | The space complexity is also linear because a new string is created that is at least as large as the original string, plus additional characters for each replacement made. In the worst case, this could be nearly double the size of the original string if every character were replaced. |

## Algorithm Walkthrough
```
Input: "1.1.1.1"
Step 1: Check if input is null → not null, proceed
Step 2: Check if input is empty → not empty, proceed
Step 3: Use replaceAll() to replace all dots with "[.]" 
    - Original string: "1.1.1.1"
    - Replacement pattern: "\\."
    - Replacement string: "[.]"
    - Result: "1[.]1[.]1[.]1"
Output: "1[.]1[.]1[.]1"
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Input null?"}
    B -->|Yes| C[Throw NullPointerException]
    B -->|No| D{"Input empty?"}
    D -->|Yes| E[Return empty string]
    D -->|No| F["ReplaceAll dots with \"[."]"]
    F --> G[Return defanged IP address]
```

## Key Insight
> **Tip:** The most efficient way to defang an IP address in Java is to use the `replaceAll()` method, which replaces all occurrences of a pattern in a string with a replacement string, making it a one-liner solution for this problem.

## Edge Cases
- **Empty/null input**: If the input is null, the program throws a `NullPointerException`. If the input is an empty string, the program returns an empty string, as there are no dots to replace.
- **Single element**: If the input is a single element (e.g., "1"), the program returns the input as is, since there are no dots to replace.
- **IP address with leading or trailing dots**: The `replaceAll()` method will correctly replace dots regardless of their position in the string, including leading or trailing dots.

## Common Mistakes
- **Mistake 1**: Not checking for null input → can be avoided by adding a null check at the beginning of the method.
- **Mistake 2**: Using a loop to manually replace dots → can be avoided by using the `replaceAll()` method, which is more efficient and less prone to errors.

## Interview Follow-ups
> **Interview:** 
- "What if the input is sorted?" → This question does not apply to this problem since the input is an IP address, not a list of numbers or strings that can be sorted.
- "Can you do it in O(1) space?" → No, because we need to create a new string to store the result, which requires additional space proportional to the size of the input.
- "What if there are duplicates?" → The presence of duplicate IP addresses or parts thereof does not affect the solution, as the `replaceAll()` method treats each dot individually.

## Java Solution

```java
// Problem: Defanging an IP Address
// Language: Java
// Difficulty: Easy
// Time Complexity: O(n) — single pass through the string
// Space Complexity: O(n) — new string with added characters
// Approach: String replacement — replace each dot with its defanged version

public class Solution {
    public String defangIPaddr(String address) {
        // Edge case: null input → throw NullPointerException
        if (address == null) {
            throw new NullPointerException("Input address cannot be null");
        }
        
        // Edge case: empty input → return empty string
        if (address.isEmpty()) {
            return "";
        }
        
        // Use replaceAll() method to replace all dots with "[.]" 
        // This method returns a copy of the string where all occurrences of a substring are replaced with another substring
        String defangedAddress = address.replaceAll("\\.", "[.]"); 
        return defangedAddress;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.defangIPaddr("1.1.1.1"));  // Output: "1[.]1[.]1[.]1"
        System.out.println(solution.defangIPaddr("255.100.50.0"));  // Output: "255[.]100[.]50[.]0"
    }
}
```
