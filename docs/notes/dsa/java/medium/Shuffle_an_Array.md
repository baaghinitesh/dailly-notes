---
title: "Shuffle an Array"
language: "java"
difficulty: "medium"
section: "dsa"
tags: "dsa, java, medium, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/255/1200/630"
update_count: 0
---

# Shuffle an Array

## Problem Understanding
The problem requires implementing a class that can shuffle an array and reset it to its original state. The key constraint is that the shuffle operation should return a random permutation of the array, and the reset operation should return the original array. This problem is non-trivial because a naive approach might not guarantee a truly random shuffle, and simply using a random number generator to swap elements could lead to biased results. The Fisher-Yates shuffle algorithm is a suitable solution, as it ensures that all permutations are equally likely.

## Approach
The approach used here is the Fisher-Yates shuffle algorithm, which is an unbiased shuffling algorithm. The algorithm works by iterating over the array from the last element to the first and swapping each element with a random element from the unshuffled part of the array. This approach ensures that all permutations are equally likely, making it suitable for generating random shuffles. The algorithm uses a copy of the original array to perform the shuffle, leaving the original array intact for the reset operation. The `Random` class is used to generate random indices for swapping.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n)  | The shuffle operation iterates over the array once, performing a constant amount of work for each element. The reset operation simply returns the original array, which is a constant time operation. |
| Space  | O(n)  | A copy of the original array is created for the shuffle operation, which requires linear space. The original array is stored for the reset operation, which also requires linear space. |

## Algorithm Walkthrough
```
Input: [1, 2, 3]
Step 1: Create a copy of the original array: [1, 2, 3]
Step 2: Iterate over the array from the last element to the first:
  - i = 2, j = random.nextInt(3) = 1, swap array[2] and array[1]: [1, 3, 2]
  - i = 1, j = random.nextInt(2) = 0, swap array[1] and array[0]: [3, 1, 2]
Step 3: Return the shuffled array: [3, 1, 2]
```
The `reset` operation simply returns the original array: [1, 2, 3]

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B[Create copy of original array]
    B --> C[Iterate over array from last to first]
    C --> D{Generate random index j}
    D -->|j = random.nextInt("i + 1")| E["Swap array[i"] and array[j]]
    E --> F{"Is i > 0?"}
    F -->|Yes| C
    F -->|No| G[Return shuffled array]
    G --> H[End]
```

## Key Insight
> **Tip:** The Fisher-Yates shuffle algorithm ensures that all permutations are equally likely by swapping each element with a random element from the unshuffled part of the array.

## Edge Cases
- **Empty/null input**: If the input array is empty or null, the shuffle operation will throw an exception when trying to access the array elements. The reset operation will return null or an empty array.
- **Single element**: If the input array has only one element, the shuffle operation will return the same array, as there is only one possible permutation.
- **Duplicate elements**: If the input array contains duplicate elements, the shuffle operation will still return a random permutation of the array, but the duplicates will be treated as identical elements.

## Common Mistakes
- **Mistake 1**: Not using a truly random number generator, which can lead to biased results. → Use a high-quality random number generator, such as the `Random` class in Java.
- **Mistake 2**: Not creating a copy of the original array for the shuffle operation, which can modify the original array. → Create a copy of the original array before performing the shuffle operation.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The Fisher-Yates shuffle algorithm will still return a random permutation of the array, regardless of the input being sorted.
- "Can you do it in O(1) space?" → No, the Fisher-Yates shuffle algorithm requires O(n) space to create a copy of the original array.
- "What if there are duplicates?" → The shuffle operation will treat duplicates as identical elements and return a random permutation of the array.

## Java Solution

```java
// Problem: Shuffle an Array
// Language: Java
// Difficulty: Medium
// Time Complexity: O(n) — single pass through array using Fisher-Yates shuffle
// Space Complexity: O(n) — creating a copy of the original array
// Approach: Fisher-Yates shuffle algorithm — for each element, swap it with a random element from the unshuffled part of the array

import java.util.Random;

public class Solution {
    private int[] original;
    private Random random;

    public Solution(int[] nums) {
        // Store the original array for later use
        original = nums;
        // Initialize the random number generator
        random = new Random();
    }

    /**
     * Resets the array to its original configuration and return it.
     */
    public int[] reset() {
        // Edge case: return the original array
        return original;
    }

    /**
     * Returns a random shuffling of the array.
     */
    public int[] shuffle() {
        // Create a copy of the original array
        int[] array = original.clone();
        // Iterate over the array from the last element to the first
        for (int i = array.length - 1; i > 0; i--) {
            // Generate a random index from 0 to i (inclusive)
            int j = random.nextInt(i + 1); // +1 to include i in the range
            // Swap the current element with the element at the random index
            int temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
        // Return the shuffled array
        return array;
    }

    public static void main(String[] args) {
        int[] nums = {1, 2, 3};
        Solution solution = new Solution(nums);
        int[] shuffled = solution.shuffle();
        for (int num : shuffled) {
            System.out.print(num + " ");
        }
        System.out.println();
        int[] reset = solution.reset();
        for (int num : reset) {
            System.out.print(num + " ");
        }
    }
}
```
