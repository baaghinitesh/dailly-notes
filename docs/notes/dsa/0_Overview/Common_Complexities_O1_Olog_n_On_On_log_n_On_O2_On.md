---
title: "Common Complexities: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ), O(n!)"
topic: "Common Complexities: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ), O(n!)"
section: "dsa"
tags: "dsa, common-complexities, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/dsa%20Common%20Complexities%20O(1),%20O(log%20n),%20O(n),%20O(n%20log%20n),%20O(n²),%20O(2ⁿ),%20O(n!)%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![complexities](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Big_O_notation.svg/1200px-Big_O_notation.svg.png)

## Introduction
**Big O notation** is a fundamental concept in computer science that describes the complexity of an algorithm, which is the amount of time or space it requires as the size of the input increases. Understanding big O notation is crucial for any software developer, as it helps to predict the performance of an algorithm and make informed decisions about which algorithm to use in a particular situation. In this section, we will introduce the concept of big O notation and its importance in real-world applications.

> **Note:** Big O notation is not a measure of the actual time or space an algorithm takes, but rather a measure of how the time or space changes as the size of the input increases.

Big O notation is used to classify algorithms into different complexity classes, such as **O(1)**, **O(log n)**, **O(n)**, **O(n log n)**, **O(n²)**, **O(2ⁿ)**, and **O(n!)**. Each of these classes has its own characteristics and is suitable for different types of problems. For example, **O(1)** is suitable for problems that require constant time, while **O(n)** is suitable for problems that require linear time.

## Core Concepts
The core concept of big O notation is to describe the upper bound of an algorithm's complexity. It is usually expressed as a function of the size of the input, typically represented as 'n'. The most common complexity classes are:

* **O(1)** - constant time complexity
* **O(log n)** - logarithmic time complexity
* **O(n)** - linear time complexity
* **O(n log n)** - linearithmic time complexity
* **O(n²)** - quadratic time complexity
* **O(2ⁿ)** - exponential time complexity
* **O(n!)** - factorial time complexity

> **Warning:** Big O notation can be misleading if not used correctly. For example, an algorithm with a time complexity of **O(n)** may be slower than an algorithm with a time complexity of **O(n log n)** for small inputs.

## How It Works Internally
Big O notation works by analyzing the number of operations an algorithm performs as the size of the input increases. The number of operations is usually measured in terms of the number of basic operations, such as additions, multiplications, and comparisons.

For example, consider an algorithm that searches for an element in an array. The algorithm iterates through the array, comparing each element to the target element. The number of operations is proportional to the size of the array, so the time complexity is **O(n)**.

> **Tip:** To determine the time complexity of an algorithm, count the number of basic operations it performs and express it as a function of the size of the input.

## Code Examples
Here are three complete and runnable examples of algorithms with different time complexities:

### Example 1: O(1) - Constant Time Complexity
```python
def constant_time(n):
    return 5
```
This function returns a constant value, regardless of the input size. The time complexity is **O(1)**, because the number of operations does not change with the size of the input.

### Example 2: O(n) - Linear Time Complexity
```python
def linear_time(n):
    sum = 0
    for i in range(n):
        sum += i
    return sum
```
This function calculates the sum of the first 'n' integers. The time complexity is **O(n)**, because the number of operations is proportional to the size of the input.

### Example 3: O(n log n) - Linearithmic Time Complexity
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result.extend(left)
    result.extend(right)
    return result

arr = [5, 2, 8, 3, 1, 6, 4]
print(merge_sort(arr))
```
This function sorts an array using the merge sort algorithm. The time complexity is **O(n log n)**, because the algorithm divides the array in half at each step and merges the results.

## Visual Diagram
```mermaid
graph TD
    A[Input Size] --> B["O(1)"]
    A --> C["O(log n)"]
    A --> D["O(n)"]
    A --> E["O(n log n)"]
    A --> F["O(n²)"]
    A --> G["O(2ⁿ)"]
    A --> H["O("n!")"]
    B --> I[Constant Time]
    C --> J[Logarithmic Time]
    D --> K[Linear Time]
    E --> L[Linearithmic Time]
    F --> M[Quadratic Time]
    G --> N[Exponential Time]
    H --> O[Factorial Time]
```
This diagram illustrates the different complexity classes and their relationships to the input size.

> **Interview:** What is the time complexity of the merge sort algorithm? How does it compare to other sorting algorithms?

## Comparison
| Complexity | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| O(1) | constant | constant | fast, efficient | limited applicability | caching, lookup tables |
| O(log n) | logarithmic | logarithmic | fast, efficient | limited applicability | binary search, tree traversals |
| O(n) | linear | linear | simple, easy to implement | slow for large inputs | linear search, array operations |
| O(n log n) | linearithmic | linearithmic | fast, efficient | complex implementation | sorting, merging |
| O(n²) | quadratic | quadratic | simple, easy to implement | slow for large inputs | bubble sort, insertion sort |
| O(2ⁿ) | exponential | exponential | fast for small inputs | extremely slow for large inputs | recursive algorithms, dynamic programming |
| O(n!) | factorial | factorial | extremely slow | limited applicability | permutations, combinations |

## Real-world Use Cases
Here are three real-world examples of algorithms with different time complexities:

* **Google's PageRank algorithm** uses a **O(n)** time complexity to calculate the importance of web pages.
* **Amazon's recommendation engine** uses a **O(n log n)** time complexity to suggest products to customers.
* **Facebook's news feed algorithm** uses a **O(2ⁿ)** time complexity to determine the order of posts in a user's news feed.

## Common Pitfalls
Here are four common mistakes that engineers make when dealing with big O notation:

* **Incorrectly assuming that a faster algorithm is always better**. While a faster algorithm may be better for large inputs, it may be slower for small inputs due to overhead.
* **Not considering the space complexity of an algorithm**. An algorithm with a low time complexity may have a high space complexity, making it impractical for large inputs.
* **Not using big O notation correctly**. Big O notation is an upper bound, not an exact measure of an algorithm's complexity.
* **Not testing an algorithm thoroughly**. An algorithm may have a low time complexity, but still have bugs or performance issues if not tested thoroughly.

> **Warning:** Big O notation can be misleading if not used correctly. Always consider the space complexity and test an algorithm thoroughly before deploying it.

## Interview Tips
Here are three common interview questions related to big O notation:

* **What is the time complexity of the bubble sort algorithm?** A weak answer would be "it's slow", while a strong answer would be "it's **O(n²)**, making it impractical for large inputs".
* **How does the time complexity of the merge sort algorithm compare to the quicksort algorithm?** A weak answer would be "they're both fast", while a strong answer would be "merge sort has a time complexity of **O(n log n)**, while quicksort has an average time complexity of **O(n log n)**, but can be **O(n²)** in the worst case".
* **What is the space complexity of the recursive Fibonacci algorithm?** A weak answer would be "it's low", while a strong answer would be "it's **O(2ⁿ)**, making it impractical for large inputs due to stack overflow".

## Key Takeaways
Here are ten key takeaways about big O notation:

* **Big O notation is an upper bound**, not an exact measure of an algorithm's complexity.
* **Time complexity is not the only consideration**; space complexity is also important.
* **O(1)** is the best time complexity, but it's not always achievable.
* **O(log n)** is a good time complexity for search algorithms.
* **O(n)** is a good time complexity for linear search algorithms.
* **O(n log n)** is a good time complexity for sorting algorithms.
* **O(n²)** is a poor time complexity for large inputs.
* **O(2ⁿ)** is an extremely poor time complexity for large inputs.
* **O(n!)** is an extremely poor time complexity for large inputs.
* **Big O notation is essential for predicting the performance of an algorithm** and making informed decisions about which algorithm to use.