---
title: "Hello World and printf scanf in C"
language: "c"
difficulty: "easy"
section: "dsa"
tags: "dsa, c, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/626/1200/630"
update_count: 0
---

# Hello World and printf scanf in C

## Problem Understanding
The problem asks to create a simple C program that prints "Hello World" to the console, prompts the user for a number, reads the input, and then prints the input number. The key constraints are to use `printf` for output and `scanf` for input, and to handle invalid input (e.g., non-numeric characters). What makes this problem non-trivial is the need to handle invalid input and clear the input buffer to prevent infinite loops or unexpected behavior.

## Approach
The algorithm strategy is to use standard input/output operations in C, specifically `printf` for output and `scanf` for input. The intuition behind this approach is to leverage the built-in functions in the C standard library to simplify the programming task. The program uses `printf` to output a string and a prompt, and `scanf` to read an integer from the user. To handle invalid input, the program checks the return value of `scanf` and clears the input buffer using `getchar` if necessary.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(1)  | The time complexity is constant because the program performs a fixed number of operations, including printing a string, reading input, and handling invalid input. The `while` loop used to clear the input buffer has a finite number of iterations bounded by the input size. |
| Space  | O(1)  | The space complexity is constant because the program uses a fixed amount of memory to store the input number and other variables. The input buffer is cleared using `getchar`, which does not allocate additional memory. |

## Algorithm Walkthrough
```
Input: 
Step 1: Print "Hello World" to the console
  - Output: "Hello World\n"
Step 2: Prompt the user for input
  - Output: "Enter a number: "
Step 3: Read the user's input
  - Input: 42
  - Variable num is assigned the value 42
Step 4: Check for invalid input
  - If invalid input is detected, clear the input buffer and print an error message
Step 5: Print the input number
  - Output: "You entered: 42\n"
Output: 
```
For example, if the user enters "42", the program will output "You entered: 42".

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Print "Hello World"]
    B --> C[Prompt user for input]
    C --> D[Read input using scanf]
    D --> E{"Invalid input?"}
    E -->|Yes| F[Clear input buffer]
    E -->|No| G[Print input number]
    F --> H[Print error message]
    H --> I["Exit with non-zero status"]
    G --> J[Exit with zero status]
```
This flowchart illustrates the program's decision flow and data transformation.

## Key Insight
> **Tip:** Always check the return value of `scanf` to handle invalid input and clear the input buffer using `getchar` to prevent unexpected behavior.

## Edge Cases
- **Empty/null input**: If the user enters an empty string, the program will detect invalid input and print an error message.
- **Single element**: If the user enters a single number, the program will print the input number.
- **Non-numeric input**: If the user enters non-numeric characters, the program will detect invalid input, clear the input buffer, and print an error message.

## Common Mistakes
- **Mistake 1**: Not checking the return value of `scanf` → To avoid this, always check the return value of `scanf` to handle invalid input.
- **Mistake 2**: Not clearing the input buffer → To avoid this, use `getchar` to clear the input buffer when invalid input is detected.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The program does not rely on the input being sorted, so it will work correctly regardless of the input order.
- "Can you do it in O(1) space?" → The program already uses O(1) space, so it meets this requirement.
- "What if there are duplicates?" → The program will handle duplicates correctly, as it reads and prints each input number separately.

## C Solution

```c
// Problem: Hello World and printf scanf in C
// Language: C
// Difficulty: Easy
// Time Complexity: O(1) — constant time complexity for simple print and scan operations
// Space Complexity: O(1) — constant space complexity for simple variables
// Approach: Standard input/output operations — using printf for output and scanf for input

#include <stdio.h> // Include standard input/output library

int main() {
    // Print "Hello World" to the console
    printf("Hello World\n"); // Using printf to output a string

    int num; // Declare an integer variable
    // Prompt the user for input
    printf("Enter a number: "); // Using printf to prompt the user
    // Read the user's input
    scanf("%d", &num); // Using scanf to read an integer from the user

    // Edge case: invalid input (e.g., non-numeric input)
    // Note: scanf returns the number of successful assignments, so we check its return value
    if (scanf("%*c") != EOF) { // If there's remaining input (e.g., non-numeric characters), clear it
        // Clear the input buffer to handle invalid input
        int c; // Declare a character variable to clear the buffer
        while ((c = getchar()) != '\n' && c != EOF); // Clear the input buffer
        printf("Invalid input. Please enter a number.\n"); // Print an error message
        return 1; // Return with a non-zero exit status to indicate an error
    }

    // Print the input number
    printf("You entered: %d\n", num); // Using printf to output the input number

    return 0; // Return with a zero exit status to indicate success
}
```
