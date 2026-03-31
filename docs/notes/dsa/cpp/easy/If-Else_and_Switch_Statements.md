---
title: "If-Else and Switch Statements"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://image.pollinations.ai/prompt/dsa%20If-Else%20and%20Switch%20Statements%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

# If-Else and Switch Statements

## Problem Understanding
The problem is asking to demonstrate the use of if-else and switch statements in C++ to evaluate expressions. The key constraints are that the code must use if-else statements to compare an integer value and switch statements to evaluate a character. The problem is non-trivial because it requires understanding of conditional statements and their applications, as well as handling edge cases where the input values do not match the expected conditions. A naive approach might not consider these edge cases, leading to incorrect results.

## Approach
The algorithm strategy is to use if-else statements to compare an integer value and switch statements to evaluate a character. The intuition behind this approach is to provide a clear and concise way to evaluate expressions based on specific conditions. The code uses if-else statements to check if an integer is greater than 5, and switch statements to evaluate a character and print a corresponding message. The approach handles key constraints by using conditional statements to evaluate the input values and print the expected results. The code uses no additional data structures, making it efficient in terms of space complexity.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(1)  | The code performs a constant number of operations, regardless of the input size. The if-else and switch statements evaluate the input values in constant time. |
| Space  | O(1)  | The code uses no additional space that scales with the input size. The variables used to store the input values and the output messages are fixed in size. |

## Algorithm Walkthrough
```
Input: x = 10, c = 'a'
Step 1: Evaluate if-else statement for x = 10
  - x is greater than 5, so print "x is greater than 5"
Step 2: Evaluate switch statement for c = 'a'
  - c is 'a', so print "Character is 'a'"
Step 3: Evaluate if-else statement for x = 3
  - x is less than or equal to 5, so print "x is less than or equal to 5"
Step 4: Evaluate switch statement for c = 'c'
  - c is not 'a' or 'b', so print "Character is neither 'a' nor 'b'"
Output: 
  x is greater than 5
  Character is 'a'
  x is less than or equal to 5
  Character is neither 'a' nor 'b'
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is x greater than 5?"}
    B -->|Yes| C[Print "x is greater than 5"]
    B -->|No| D[Print "x is less than or equal to 5"]
    A --> E{"Is c 'a' or 'b'?"}
    E -->|'a'| F[Print "Character is 'a'"]
    E -->|'b'| G[Print "Character is 'b'"]
    E -->|Neither| H[Print "Character is neither 'a' nor 'b'"]
```

## Key Insight
> **Tip:** The key to using if-else and switch statements effectively is to clearly define the conditions and handle edge cases where the input values do not match the expected conditions.

## Edge Cases
- **Empty/null input**: If the input is empty or null, the code will not compile or will throw an error, because the input values are expected to be integers or characters.
- **Single element**: If the input is a single element, the code will evaluate the if-else and switch statements accordingly, and print the expected results.
- **Invalid character**: If the input character is not 'a' or 'b', the code will print "Character is neither 'a' nor 'b'", handling the edge case where the input character is not one of the expected values.

## Common Mistakes
- **Mistake 1**: Not handling edge cases where the input values do not match the expected conditions, leading to incorrect results or errors.
- **Mistake 2**: Using if-else statements instead of switch statements for evaluating characters, leading to less efficient and less readable code.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The code does not assume any specific order of the input values, so it will still work correctly even if the input is sorted.
- "Can you do it in O(1) space?" → The code already uses O(1) space, because it does not use any additional data structures that scale with the input size.
- "What if there are duplicates?" → The code does not assume any specific uniqueness of the input values, so it will still work correctly even if there are duplicates.

## CPP Solution

```cpp
// Problem: If-Else and Switch Statements
// Language: C++
// Difficulty: Easy
// Time Complexity: O(1) — constant time operations
// Space Complexity: O(1) — no additional space used
// Approach: Conditional statement evaluation — using if-else and switch statements to evaluate expressions

#include <iostream>

class IfElseSwitch {
public:
    void ifElseExample(int x) {
        // Check if x is greater than 5
        if (x > 5) {
            std::cout << "x is greater than 5" << std::endl;
        } else {
            // Edge case: x is less than or equal to 5
            std::cout << "x is less than or equal to 5" << std::endl;
        }
    }

    void switchExample(char c) {
        // Use switch statement to evaluate c
        switch (c) {
            case 'a':
                std::cout << "Character is 'a'" << std::endl;
                break;
            case 'b':
                std::cout << "Character is 'b'" << std::endl;
                break;
            default:
                // Edge case: c is not 'a' or 'b'
                std::cout << "Character is neither 'a' nor 'b'" << std::endl;
                break;
        }
    }
};

int main() {
    IfElseSwitch example;
    example.ifElseExample(10);  // x is greater than 5
    example.ifElseExample(3);    // x is less than or equal to 5
    example.switchExample('a');  // Character is 'a'
    example.switchExample('c');  // Character is neither 'a' nor 'b'
    return 0;
}
```
