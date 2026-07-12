---
title: "Selection Sort"
language: "java"
difficulty: "easy"
section: "dsa"
tags: "dsa, java, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/940/1200/630"
update_count: 0
---

# Selection Sort

## Problem Understanding
The problem asks to sort an array of integers in ascending order using the selection sort algorithm. The key constraint is that the algorithm should have a time complexity of O(n^2) and a space complexity of O(1), meaning it should use no additional data structures. What makes this problem non-trivial is that the naive approach of comparing and swapping elements in a nested loop structure can be inefficient, and the algorithm needs to be optimized to find the minimum element in the unsorted part of the array and put it at the beginning. The selection sort algorithm is suitable for small arrays or arrays with a limited number of unique elements.

## Approach
The algorithm strategy is to use an iterative selection and swapping approach, where the algorithm repeatedly finds the minimum element from the unsorted part of the array and puts it at the beginning. This approach works because it ensures that the smallest element is always at the beginning of the unsorted part of the array, and the algorithm can then move on to the next element. The algorithm uses a nested loop structure to compare and swap elements, and it uses a temporary variable to store the current element during the swapping process. The algorithm handles the key constraints by using no additional data structures and by optimizing the comparison and swapping process.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n^2) | The algorithm uses two nested loops to compare and swap elements, where n is the number of elements in the array. The outer loop runs n-1 times, and the inner loop runs n-i times, resulting in a total of n*(n-1)/2 comparisons. |
| Space  | O(1)  | The algorithm uses no additional data structures, only a temporary variable to store the current element during the swapping process. |

## Algorithm Walkthrough
```
Input: [64, 25, 12, 22, 11]
Step 1: i = 0, minIndex = 0, array = [64, 25, 12, 22, 11]
  - Compare 64 with 25, 12, 22, 11, and find the minimum element 11 at index 4
  - Swap 64 and 11, array = [11, 25, 12, 22, 64]
Step 2: i = 1, minIndex = 1, array = [11, 25, 12, 22, 64]
  - Compare 25 with 12, 22, 64, and find the minimum element 12 at index 2
  - Swap 25 and 12, array = [11, 12, 25, 22, 64]
Step 3: i = 2, minIndex = 2, array = [11, 12, 25, 22, 64]
  - Compare 25 with 22, 64, and find the minimum element 22 at index 3
  - Swap 25 and 22, array = [11, 12, 22, 25, 64]
Step 4: i = 3, minIndex = 3, array = [11, 12, 22, 25, 64]
  - Compare 25 with 64, and find the minimum element 25 at index 3
  - No swap needed, array = [11, 12, 22, 25, 64]
Output: [11, 12, 22, 25, 64]
```
## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{"Empty or null array?"}
    B -->|Yes| C["Print \"Array is empty.\" and return"]
    B -->|No| D[Initialize i to 0 and minIndex to i]
    D --> E{"Found minimum element?"}
    E -->|Yes| F[Swap elements at i and minIndex]
    E -->|No| G["Compare array[j"] with array[minIndex] and update minIndex]
    G --> H{"Reached end of array?"}
    H -->|Yes| I[Increment i and repeat from D]
    H -->|No| G
    I --> J{"Reached end of sorting?"}
    J -->|Yes| K[Print sorted array]
    J -->|No| I
```
## Key Insight
> **Tip:** The key insight to the selection sort algorithm is to repeatedly find the minimum element from the unsorted part of the array and put it at the beginning, ensuring that the smallest element is always at the beginning of the unsorted part of the array.

## Edge Cases
- **Empty or null array**: The algorithm will print "Array is empty." and return immediately.
- **Single element**: The algorithm will not perform any comparisons or swaps, and will simply return the original array.
- **Array with duplicate elements**: The algorithm will still work correctly, but it may perform unnecessary swaps if the duplicate elements are not in the correct order.

## Common Mistakes
- **Mistake 1: Not checking for empty or null array**: This can lead to a NullPointerException or incorrect results. To avoid this, always check for empty or null arrays at the beginning of the algorithm.
- **Mistake 2: Not updating the minIndex correctly**: This can lead to incorrect results or infinite loops. To avoid this, always update the minIndex correctly when a smaller element is found.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The algorithm will still have a time complexity of O(n^2), but it will perform fewer swaps.
- "Can you do it in O(1) space?" → The algorithm already uses O(1) space, so no changes are needed.
- "What if there are duplicates?" → The algorithm will still work correctly, but it may perform unnecessary swaps if the duplicate elements are not in the correct order.

## Java Solution

```java
// Problem: Selection Sort
// Language: Java
// Difficulty: Easy
// Time Complexity: O(n^2) — two nested loops to compare and swap elements
// Space Complexity: O(1) — no additional data structures used
// Approach: Iterative selection and swapping — repeatedly find the minimum element from unsorted part and put it at the beginning

public class SelectionSort {
    /**
     * Sorts an array of integers using the selection sort algorithm.
     * 
     * @param array the array to be sorted
     */
    public static void selectionSort(int[] array) {
        // Edge case: empty or null array → return immediately
        if (array == null || array.length == 0) {
            return;
        }

        // Iterate over the array from the first element to the second last element
        for (int i = 0; i < array.length - 1; i++) {
            // Initialize the minimum index to the current index
            int minIndex = i; // assuming the first element is the smallest

            // Find the minimum element in the unsorted part of the array
            for (int j = i + 1; j < array.length; j++) {
                // If a smaller element is found, update the minimum index
                if (array[j] < array[minIndex]) {
                    minIndex = j; // update the minimum index
                }
            }

            // If the minimum index is not the current index, swap the elements
            if (minIndex != i) {
                // Swap the elements at the current index and the minimum index
                int temp = array[i]; // store the current element in a temporary variable
                array[i] = array[minIndex]; // replace the current element with the minimum element
                array[minIndex] = temp; // replace the minimum element with the current element
            }
        }
    }

    /**
     * Prints the elements of an array.
     * 
     * @param array the array to be printed
     */
    public static void printArray(int[] array) {
        // Edge case: empty or null array → print a message
        if (array == null || array.length == 0) {
            System.out.println("Array is empty.");
            return;
        }

        // Print the elements of the array
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i] + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        // Test the selection sort algorithm
        int[] array = {64, 25, 12, 22, 11};
        System.out.println("Original array:");
        printArray(array);
        selectionSort(array);
        System.out.println("Sorted array:");
        printArray(array);
    }
}
```
