---
title: "Base 7 Conversion Algorithm"
language: "cpp"
difficulty: "easy"
section: "dsa"
tags: "dsa, cpp, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/222/1200/630"
update_count: 0
---

# Base 7 Conversion Algorithm

## Problem Understanding
The problem asks for an algorithm to convert a given integer into its base 7 representation. The key constraint here is that the input number can be any integer, including negative numbers and zero. What makes this problem non-trivial is the need to handle the conversion process efficiently, considering the possibility of negative numbers and the requirement to represent the result in base 7. The naive approach might involve manually calculating the powers of 7 and trying to fit the number into these powers, but this would be cumbersome and inefficient.

## Approach
The algorithm strategy used here is a simple iterative conversion, where we iterate through each digit of the input number and convert it to its base 7 equivalent. This approach works because it leverages the properties of modular arithmetic and integer division to efficiently calculate the remainder of the number when divided by 7, which gives us the next digit in the base 7 representation. We use a string to store the result, which allows us to easily prepend the digits as we calculate them. The approach also handles the key constraint of negative numbers by first determining if the number is negative, making it positive for the conversion, and then prepending a negative sign to the result if necessary.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(log(n)) | The time complexity is O(log(n)) because we are essentially performing a constant amount of work for each digit in the input number. The number of digits in the input number is proportional to the logarithm of the number, hence the time complexity. |
| Space  | O(log(n)) | The space complexity is O(log(n)) because we are storing the result in a string, and the length of this string is proportional to the number of digits in the input number, which is O(log(n)). |

## Algorithm Walkthrough
```
Input: num = 100
Step 1: Check if num is 0, it's not, so we proceed.
Step 2: Determine if num is negative, it's not, so isNegative = false.
Step 3: Make num positive if necessary, num remains 100.
Step 4: Calculate remainder = num % 7 = 100 % 7 = 2.
Step 5: Prepend remainder to result, result = "2".
Step 6: Update num = num / 7 = 100 / 7 = 14.
Step 7: Repeat steps 4-6 until num > 0:
  - remainder = 14 % 7 = 0, result = "02".
  - num = 14 / 7 = 2.
  - remainder = 2 % 7 = 2, result = "202".
  - num = 2 / 7 = 0, so we exit the loop.
Step 8: Since isNegative = false, we don't prepend a negative sign to result.
Output: result = "202".
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Is num 0?"}
    B -->|Yes| C[Return "0"]
    B -->|No| D{"Is num negative?"}
    D -->|Yes| E["Make num positive and set isNegative = true"]
    D -->|No| E
    E --> F["Calculate remainder = num % 7"]
    F --> G[Prepend remainder to result]
    G --> H["Update num = num / 7"]
    H --> I{"Is num > 0?"}
    I -->|Yes| F
    I -->|No| J{"Was num originally negative?"}
    J -->|Yes| K["Prepend \"-\" to result"]
    J -->|No| K
    K --> L[Return result]
```

## Key Insight
> **Tip:** The key insight here is to use the properties of modular arithmetic to efficiently calculate the base 7 representation of a number by iteratively calculating the remainder when divided by 7.

## Edge Cases
- **Empty/null input**: This is not applicable in the context of this problem, as the input is an integer. However, if we consider an "empty" input as a 0, the algorithm correctly handles this by returning "0".
- **Single element**: If the input number is a single digit (i.e., between -7 and 7, inclusive), the algorithm still works correctly, as it will simply return the number as a string, prepending a negative sign if necessary.
- **Large input number**: The algorithm handles large input numbers efficiently because it uses integer division and modular arithmetic, which avoids the need for explicit power calculations or large intermediate results.

## Common Mistakes
- **Mistake 1**: Forgetting to handle the case where the input number is 0. To avoid this, we explicitly check for num == 0 at the beginning of the algorithm.
- **Mistake 2**: Not correctly handling negative numbers. To avoid this, we determine if the number is negative at the start and make it positive for the conversion, then prepend a negative sign to the result if necessary.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → This question is not applicable in the context of this problem, as the input is an integer, not a collection of numbers. However, the algorithm does not rely on the input being sorted, so it would work regardless.
- "Can you do it in O(1) space?" → No, it's not possible to achieve O(1) space complexity because we need to store the result, which can grow up to O(log(n)) in size.
- "What if there are duplicates?" → This question is not applicable in the context of this problem, as the input is an integer, not a collection of numbers. The algorithm does not consider duplicates because it operates on a single number.

## CPP Solution

```cpp
// Problem: Base 7 Conversion Algorithm
// Language: cpp
// Difficulty: Easy
// Time Complexity: O(log(n)) — number of digits in the input number
// Space Complexity: O(log(n)) — string to store the result
// Approach: Simple iterative conversion — iterate through each digit and convert to base 7

class Solution {
public:
    string convertToBase7(int num) {
        // Edge case: input number is 0
        if (num == 0) return "0";
        
        // Initialize an empty string to store the result
        string result = "";
        
        // Determine if the number is negative
        bool isNegative = num < 0;
        
        // Make the number positive for the conversion
        num = abs(num);
        
        // Iterate through each digit and convert to base 7
        while (num > 0) {
            // Calculate the remainder of the number when divided by 7
            int remainder = num % 7;
            
            // Prepend the remainder to the result string
            result = to_string(remainder) + result;
            
            // Update the number by performing integer division by 7
            num /= 7;
        }
        
        // If the original number was negative, prepend a negative sign to the result
        if (isNegative) {
            result = "-" + result;
        }
        
        return result;
    }
};
```
