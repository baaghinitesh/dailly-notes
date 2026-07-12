---
title: "Find the Frequency of Each Element in Array"
language: "c"
difficulty: "easy"
section: "dsa"
tags: "dsa, c, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/591/1200/630"
update_count: 0
---

# Find the Frequency of Each Element in Array

## Problem Understanding
The problem asks to find the frequency of each element in a given array, which means counting the number of occurrences of each unique element. The key constraint is that the array can contain duplicate elements, and the problem requires an efficient solution to handle this. This problem is non-trivial because a naive approach, such as using nested loops to compare each element with others, would result in a time complexity of O(n^2), which is inefficient for large arrays. The problem becomes more challenging when considering the need to optimize the solution for better performance.

## Approach
The algorithm strategy for this problem involves two approaches: a brute force frequency counting method and an optimized sorting and counting method. The brute force approach uses nested loops to iterate through the array and count the occurrences of each element. The optimized approach sorts the array in ascending order and then counts the consecutive occurrences of each element. The mathematical/logical reasoning behind the optimized approach is that by sorting the array, we can easily identify the consecutive occurrences of each element and count them efficiently. The data structure used in both approaches is the array itself, and the choice of this data structure is due to the problem's requirement to operate on an array. The optimized approach handles the key constraint of duplicate elements by sorting the array and then counting the consecutive occurrences of each element.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n^2) / O(n log n) | The brute force approach has a time complexity of O(n^2) due to the nested loops, while the optimized approach has a time complexity of O(n log n) due to the sorting operation. |
| Space  | O(1) | Both approaches have a space complexity of O(1) because they only use a constant amount of extra space to store variables, excluding the output. |

## Algorithm Walkthrough
```
Input: array = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
Step 1: (Brute Force) Initialize count for first element (1)
Step 2: (Brute Force) Loop through array to count occurrences of 1: count = 1
Step 3: (Brute Force) Print frequency of 1: Frequency of 1: 1
Step 4: (Brute Force) Initialize count for second element (2)
Step 5: (Brute Force) Loop through array to count occurrences of 2: count = 2
Step 6: (Brute Force) Print frequency of 2: Frequency of 2: 2
...
Step 10: (Optimized) Sort the array in ascending order: [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
Step 11: (Optimized) Initialize count for first element (1): count = 1
Step 12: (Optimized) Loop through sorted array to count consecutive occurrences of each element
Step 13: (Optimized) Print frequency of each element: Frequency of 1: 1, Frequency of 2: 2, Frequency of 3: 3, Frequency of 4: 4
Output: Frequencies of each element in the array
```

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Empty Array?"}
    B -->|Yes| C[Print "Array is empty"]
    B -->|No| D[Loop through array]
    D --> E{"Brute Force / Optimized"}
    E -->|Brute Force| F[Loop through array to count occurrences]
    E -->|Optimized| G[Sort array]
    G --> H[Loop through sorted array to count consecutive occurrences]
    F --> I[Print frequency of each element]
    H --> I
```

## Key Insight
> **Tip:** The key insight to solving this problem efficiently is to sort the array first, which allows us to easily count the consecutive occurrences of each element, reducing the time complexity from O(n^2) to O(n log n).

## Edge Cases
- **Empty/null input**: If the input array is empty, the algorithm should print a message indicating that the array is empty and return without attempting to access the array.
- **Single element**: If the input array contains only one element, the algorithm should print the frequency of that element as 1.
- **Duplicate elements**: If the input array contains duplicate elements, the algorithm should correctly count the occurrences of each element, including the duplicates.

## Common Mistakes
- **Mistake 1**: Not handling the edge case of an empty input array, which can lead to a runtime error when attempting to access the array.
- **Mistake 2**: Not correctly counting the occurrences of each element, especially when there are duplicates, which can result in incorrect output.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The optimized approach would still work correctly, but the time complexity would be O(n) because the array is already sorted.
- "Can you do it in O(1) space?" → No, it is not possible to solve this problem in O(1) space because we need to store the frequencies of each element, which requires extra space.
- "What if there are duplicates?" → The optimized approach correctly handles duplicates by sorting the array and counting the consecutive occurrences of each element.

## C Solution

```c
// Problem: Find the Frequency of Each Element in Array
// Language: C
// Difficulty: Easy
// Time Complexity: O(n^2) — nested loop to compare each element with others
// Space Complexity: O(1) — no extra space used, excluding output
// Approach: Brute force frequency counting — iterate through array and count occurrences of each element

#include <stdio.h>

// Function to find frequency of each element in array
void findFrequencies(int array[], int size) {
    // Edge case: empty input → print message and return
    if (size == 0) {
        printf("Array is empty\n");
        return;
    }

    for (int i = 0; i < size; i++) {  // Loop through each element in array
        int count = 0;  // Initialize count for current element
        for (int j = 0; j < size; j++) {  // Loop through array to count occurrences
            if (array[i] == array[j]) {  // If current element matches, increment count
                count++;
            }
        }
        printf("Frequency of %d: %d\n", array[i], count);  // Print frequency of current element
    }
}

// Alternative optimized solution using sorting and counting
// Time Complexity: O(n log n) — sorting the array
// Space Complexity: O(1) — no extra space used, excluding output
// Approach: Sorting and counting — sort array and count consecutive occurrences of each element
void findFrequenciesOptimized(int array[], int size) {
    // Edge case: empty input → print message and return
    if (size == 0) {
        printf("Array is empty\n");
        return;
    }

    // Sort the array in ascending order
    for (int i = 0; i < size - 1; i++) {  // Loop through array
        for (int j = i + 1; j < size; j++) {  // Loop through remaining elements
            if (array[i] > array[j]) {  // If current element is greater than next, swap
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }

    int count = 1;  // Initialize count for first element
    for (int i = 1; i < size; i++) {  // Loop through sorted array
        if (array[i] == array[i - 1]) {  // If current element matches previous, increment count
            count++;
        } else {  // If current element is different from previous, print frequency and reset count
            printf("Frequency of %d: %d\n", array[i - 1], count);
            count = 1;
        }
    }
    printf("Frequency of %d: %d\n", array[size - 1], count);  // Print frequency of last element
}

int main() {
    int array[] = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4};
    int size = sizeof(array) / sizeof(array[0]);
    findFrequencies(array, size);
    findFrequenciesOptimized(array, size);
    return 0;
}
```
