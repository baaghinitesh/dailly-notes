---
title: "Calculate Compound Interest"
language: "c"
difficulty: "easy"
section: "dsa"
tags: "dsa, c, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/114/1200/630"
update_count: 0
---

# Calculate Compound Interest

## Problem Understanding
The problem asks to calculate the compound interest, which is the interest calculated on the initial principal, which also includes all of the accumulated interest from previous periods. The key constraints are that the principal, rate, time, and number of times interest is compounded per year must be non-negative. What makes this problem non-trivial is handling edge cases where the input values are invalid. The formula for compound interest is A = P(1 + r/n)^(nt), where A is the amount of money accumulated after n years, including interest, P is the principal amount (initial amount of money), r is the annual interest rate (in decimal), n is the number of times that interest is compounded per year, and t is the time the money is invested for in years.

## Approach
The algorithm strategy is to use the formula A = P(1 + r/n)^(nt) to calculate the compound interest. This approach works because it takes into account the principal, rate, time, and number of times interest is compounded per year. The mathematical reasoning behind this formula is that it calculates the interest for each period and adds it to the principal, which is then used to calculate the interest for the next period. The data structure used is a simple function that takes in the principal, rate, time, and n as parameters and returns the final amount. This approach handles the key constraints by checking for non-positive input values and returning an error message if any of the inputs are invalid.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(1)  | The time complexity is O(1) because the calculation of compound interest using the formula A = P(1 + r/n)^(nt) takes constant time, regardless of the input size. The pow function in C also takes constant time. |
| Space  | O(1)  | The space complexity is O(1) because the function only uses a constant amount of space to store the input parameters and the result. |

## Algorithm Walkthrough
```
Input: principal = 1000.0, rate = 0.05, time = 5.0, n = 1.0
Step 1: Check for edge cases: principal = 1000.0 (positive), rate = 0.05 (non-negative), time = 5.0 (non-negative), n = 1.0 (positive)
Step 2: Calculate compound interest using the formula A = P(1 + r/n)^(nt)
    amount = 1000.0 * pow((1 + 0.05/1.0), (1.0*5.0)) = 1000.0 * pow(1.05, 5.0) = 1000.0 * 1.2762815625 = 1276.28
Output: The final amount after 5.000000 years is: $1276.28
```
This example exercises the main logic path of the algorithm, which is to calculate the compound interest using the formula A = P(1 + r/n)^(nt).

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Check for edge cases}
    B -->|Yes| C["Print error message and return -1"]
    B -->|No| D["Calculate compound interest using the formula A = P("1 + r/n")^(nt)"]
    D --> E[Return the final amount]
    C --> F[End]
    E --> F
```
This flowchart shows the decision flow of the algorithm, which checks for edge cases and calculates the compound interest using the formula A = P(1 + r/n)^(nt).

## Key Insight
> **Tip:** The key insight to calculating compound interest is to use the formula A = P(1 + r/n)^(nt), which takes into account the principal, rate, time, and number of times interest is compounded per year.

## Edge Cases
- **Empty/null input**: If the input is empty or null, the function will not be able to calculate the compound interest and will return an error message.
- **Single element**: If the input is a single element, the function will still be able to calculate the compound interest using the formula A = P(1 + r/n)^(nt).
- **Negative rate**: If the rate is negative, the function will return an error message because a negative rate is not a valid input.

## Common Mistakes
- **Mistake 1**: Not checking for edge cases, such as non-positive input values, which can cause the function to return incorrect results.
- **Mistake 2**: Not using the correct formula for compound interest, which can also cause the function to return incorrect results.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → This is not applicable to this problem because the input is not a list of numbers that needs to be sorted.
- "Can you do it in O(1) space?" → Yes, the function already uses O(1) space because it only uses a constant amount of space to store the input parameters and the result.
- "What if there are duplicates?" → This is not applicable to this problem because the input is not a list of numbers that can have duplicates.

## C Solution

```c
// Problem: Calculate Compound Interest
// Language: C
// Difficulty: Easy
// Time Complexity: O(1) — constant time calculation
// Space Complexity: O(1) — constant space usage
// Approach: formula-based calculation — using the formula A = P(1 + r/n)^(nt)

#include <stdio.h>
#include <math.h>

/**
 * Calculate compound interest.
 *
 * @param principal initial amount of money
 * @param rate interest rate (in decimal form)
 * @param time time the money is invested for (in years)
 * @param n number of times interest is compounded per year
 * @return the final amount after compound interest
 */
double calculateCompoundInterest(double principal, double rate, double time, double n) {
    // Check for edge cases: non-positive principal, rate, time, or n
    if (principal <= 0) { // Edge case: non-positive principal
        printf("Error: Principal must be a positive number.\n");
        return -1;
    }
    if (rate < 0) { // Edge case: negative rate
        printf("Error: Rate must be a non-negative number.\n");
        return -1;
    }
    if (time < 0) { // Edge case: negative time
        printf("Error: Time must be a non-negative number.\n");
        return -1;
    }
    if (n <= 0) { // Edge case: non-positive n
        printf("Error: Number of times interest is compounded per year must be a positive number.\n");
        return -1;
    }

    // Calculate compound interest using the formula A = P(1 + r/n)^(nt)
    double amount = principal * pow((1 + rate/n), (n*time)); // calculate compound interest

    return amount;
}

int main() {
    double principal = 1000.0; // initial amount of money
    double rate = 0.05; // interest rate (5%)
    double time = 5.0; // time the money is invested for (5 years)
    double n = 1.0; // number of times interest is compounded per year

    double finalAmount = calculateCompoundInterest(principal, rate, time, n);
    if (finalAmount != -1) {
        printf("The final amount after %f years is: $%.2f\n", time, finalAmount); // print the final amount
    }

    return 0;
}
```
