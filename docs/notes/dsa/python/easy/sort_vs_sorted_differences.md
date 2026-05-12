---
title: "sort() vs sorted() differences"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/682/1200/630"
update_count: 0
---

# sort() vs sorted() differences

## Problem Understanding
The problem is asking to explain the differences between the `sort()` and `sorted()` functions in Python. The `sort()` method sorts the list in-place, meaning it modifies the original list, while the `sorted()` function returns a new sorted list and leaves the original list unchanged. This problem requires understanding the implications of these differences and how they affect the output. What makes this problem non-trivial is that it requires considering the trade-offs between memory usage and the need to preserve the original list.

## Approach
The algorithm strategy is to demonstrate the differences between `list.sort()` and `sorted()` by applying them to example lists. The intuition behind this approach is to show how each function affects the original list and the resulting sorted list. The `list.sort()` method is used to sort the list in-place, while the `sorted()` function is used to return a new sorted list. The `copy()` method is used to create a copy of the original list before sorting it in-place. This approach handles the key constraints by preserving the original list when using `sorted()` and modifying the original list when using `list.sort()`.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(n log n) | Both `sort()` and `sorted()` use the Timsort algorithm, which has a time complexity of O(n log n) in the worst case. |
| Space  | O(n) | The `sorted()` function returns a new sorted list, which requires additional space proportional to the size of the input list. On the other hand, `sort()` sorts the list in-place, requiring minimal additional space. |

## Algorithm Walkthrough
```
Input: unsorted_list = [5, 2, 9, 1, 7]
Step 1: Create a copy of the original list to preserve it: sorted_list_in_place = unsorted_list.copy()
Step 2: Sort the copied list in-place using list.sort(): sorted_list_in_place.sort()
Step 3: Use sorted() function to return a new sorted list: sorted_list_new = sorted(unsorted_list)
Output: 
Sorted list (in-place): [1, 2, 5, 7, 9]
Original list: [5, 2, 9, 1, 7]
Sorted list (new): [1, 2, 5, 7, 9]
```
This walkthrough demonstrates how `list.sort()` and `sorted()` affect the original list and the resulting sorted list.

## Visual Flow
```mermaid
flowchart TD
    A[Start] --> B{Choose sorting method}
    B -->|sort()| C["Sort in-place"]
    B -->|sorted()| D[Return new sorted list]
    C --> E[Modify original list]
    D --> F[Leave original list unchanged]
    E --> G[Print sorted list]
    F --> G
```
This flowchart shows the decision flow between using `list.sort()` and `sorted()`, and how each method affects the original list.

## Key Insight
> **Tip:** The key difference between `sort()` and `sorted()` is that `sort()` modifies the original list, while `sorted()` returns a new sorted list, preserving the original list.

## Edge Cases
- **Empty/null input**: Both `list.sort()` and `sorted()` handle empty lists correctly, returning an empty list or sorting the empty list in-place.
- **Single element**: Both `list.sort()` and `sorted()` handle single-element lists correctly, returning the same list.
- **List with duplicate elements**: Both `list.sort()` and `sorted()` handle lists with duplicate elements correctly, sorting the duplicates together.

## Common Mistakes
- **Mistake 1**: Assuming that `sort()` returns a new sorted list, instead of modifying the original list. → To avoid this, use `sorted()` to return a new sorted list.
- **Mistake 2**: Assuming that `sorted()` modifies the original list, instead of returning a new sorted list. → To avoid this, use `list.sort()` to sort the list in-place.

## Interview Follow-ups
> **Interview:** These are the exact follow-up questions interviewers ask:
- "What if the input is sorted?" → The time complexity of `sort()` and `sorted()` remains O(n log n) even if the input is sorted, because Timsort algorithm has a best-case time complexity of O(n).
- "Can you do it in O(1) space?" → No, `sorted()` requires O(n) space to return a new sorted list. However, `list.sort()` can sort the list in-place, using minimal additional space.
- "What if there are duplicates?" → Both `list.sort()` and `sorted()` handle lists with duplicate elements correctly, sorting the duplicates together.

## Python Solution

```python
# Problem: sort() vs sorted() differences
# Language: Python
# Difficulty: Easy
# Time Complexity: O(n log n) — both sort() and sorted() use Timsort algorithm
# Space Complexity: O(n) — sorted() returns a new sorted list, while sort() sorts in-place
# Approach: comparison of list.sort() and sorted() functions — demonstrating their differences

def sort_vs_sorted():
    # Test list
    unsorted_list = [5, 2, 9, 1, 7]

    # Using list.sort() method
    # This method sorts the list in-place, meaning it modifies the original list
    sorted_list_in_place = unsorted_list.copy()  # Create a copy to preserve the original list
    sorted_list_in_place.sort()  # Sort the list in-place
    print("Sorted list (in-place):", sorted_list_in_place)  # Output: [1, 2, 5, 7, 9]

    # Using sorted() function
    # This function returns a new sorted list and leaves the original list unchanged
    sorted_list_new = sorted(unsorted_list)  # Return a new sorted list
    print("Original list:", unsorted_list)  # Output: [5, 2, 9, 1, 7]
    print("Sorted list (new):", sorted_list_new)  # Output: [1, 2, 5, 7, 9]

    # Edge case: empty list
    empty_list = []
    print("Sorting empty list (in-place):")
    empty_list.sort()
    print("Sorted empty list (in-place):", empty_list)  # Output: []

    print("Sorting empty list (new):")
    sorted_empty_list = sorted(empty_list)
    print("Sorted empty list (new):", sorted_empty_list)  # Output: []

    # Edge case: list with duplicate elements
    list_with_duplicates = [5, 2, 9, 1, 7, 2, 5]
    print("Sorting list with duplicates (in-place):")
    list_with_duplicates.sort()
    print("Sorted list with duplicates (in-place):", list_with_duplicates)  # Output: [1, 2, 2, 5, 5, 7, 9]

    print("Sorting list with duplicates (new):")
    sorted_list_with_duplicates = sorted(list_with_duplicates)
    print("Sorted list with duplicates (new):", sorted_list_with_duplicates)  # Output: [1, 2, 2, 5, 5, 7, 9]

# Execute the function
sort_vs_sorted()
```
