---
title: "Basic Class Creation (__init__)"
language: "python"
difficulty: "easy"
section: "dsa"
tags: "dsa, python, easy, leetcode, algorithms, coding-interview"
banner: "https://picsum.photos/seed/388/1200/630"
update_count: 0
---

# Basic Class Creation (__init__)

## Problem Understanding
The problem is asking to create a basic class in Python that represents a person with attributes like name and age. The key constraint is to initialize these attributes using the `__init__` method, which is a special method that gets called when an object is created from the class. What makes this problem non-trivial is handling edge cases such as empty or invalid input for name and age, requiring a thoughtful approach to attribute initialization and validation. The problem also requires a method to print the person's details, adding an extra layer of complexity.

## Approach
The algorithm strategy is to define a class with an `__init__` method that initializes the name and age attributes. The intuition behind this approach is to encapsulate the data and behavior of a person into a single unit, making it easy to create and manage person objects. This approach works because the `__init__` method is automatically called when an object is created, allowing for seamless initialization of attributes. The `print_details` method is used to display the person's information, handling edge cases where the name or age might be invalid. The data structure used is a simple class with attributes, chosen for its simplicity and ease of use.

## Complexity Analysis
| Metric | Value | Detailed Reason |
|--------|-------|----------------|
| Time   | O(1)  | The time complexity is constant because the `__init__` method and `print_details` method perform a fixed number of operations, regardless of the input size. The creation of a new object and initialization of its attributes take constant time. |
| Space  | O(1)  | The space complexity is constant because the class creates a fixed amount of space to store the object's attributes (name and age), regardless of the input size. The space used does not grow with the size of the input. |

## Algorithm Walkthrough
```
Input: name = "John Doe", age = 30
Step 1: Create a new Person object with the given name and age
    - self.name = "John Doe"
    - self.age = 30
Step 2: Call the print_details method to display the person's information
    - Check if self.name is empty: False
    - Print "Name: John Doe"
    - Check if self.age is not a positive integer: False
    - Print "Age: 30"
Output: 
Name: John Doe
Age: 30
```

## Visual Flow
```mermaid
flowchart TD
    A[Create Person Object] --> B{Initialize Attributes}
    B -->|name and age provided| C["Set self.name and self.age"]
    B -->|empty or invalid input| D[Handle Edge Cases]
    C --> E[Call print_details Method]
    D --> E
    E --> F{Print Name}
    F -->|name not empty| G["Print \"Name: self.name\""]
    F -->|name empty| H[Print "Default Name"]
    E --> I{Print Age}
    I -->|age valid| J["Print \"Age: self.age\""]
    I -->|age not valid| K[Print "Default Age"]
```

## Key Insight
> **Tip:** The key to solving this problem is understanding how to use the `__init__` method to initialize object attributes and handle edge cases where the input might be invalid, making the code robust and reliable.

## Edge Cases
- **Empty/null input**: If the input for name or age is empty or null, the code handles this by printing default values, ensuring that the program does not crash and provides a meaningful output instead.
- **Single element**: This problem does not involve collections or lists, so the concept of a single element does not directly apply. However, if considering the person object as a single entity, the code handles its creation and manipulation correctly.
- **Invalid age**: If the age provided is not a positive integer, the code prints a default age, handling this edge case by ensuring that the output remains consistent and user-friendly.

## Common Mistakes
- **Mistake 1**: Forgetting to handle edge cases for invalid or missing input, leading to potential errors or crashes.
- **Mistake 2**: Not using the `__init__` method correctly, resulting in attributes not being initialized properly.

## Interview Follow-ups
> **Interview:** 
- "What if the input is sorted?" → This question does not directly apply to the problem of creating a person class, as sorting is not a relevant operation in this context.
- "Can you do it in O(1) space?" → The current solution already achieves O(1) space complexity, as it only uses a constant amount of space to store the object's attributes.
- "What if there are duplicates?" → This question is not directly relevant to the problem, as the creation of a person object does not inherently involve the concept of duplicates. However, if considering a collection of person objects, handling duplicates would depend on the specific requirements of the application.

## Python Solution

```python
# Problem: Basic Class Creation (__init__)
# Language: python
# Difficulty: Easy
# Time Complexity: O(1) — constant time for initialization
# Space Complexity: O(1) — constant space for object creation
# Approach: Class definition with __init__ method — initializes object attributes

class Person:
    def __init__(self, name: str, age: int) -> None:
        # Initialize name attribute
        self.name = name  # Store the provided name
        # Initialize age attribute
        self.age = age  # Store the provided age

    # Method to print person details
    def print_details(self) -> None:
        # Edge case: name is empty → print default name
        if not self.name:
            print("Default Name")
        else:
            print(f"Name: {self.name}")  # Print the person's name
        # Edge case: age is not a positive integer → print default age
        if self.age <= 0:
            print("Default Age")
        else:
            print(f"Age: {self.age}")  # Print the person's age

# Example usage
person = Person("John Doe", 30)  # Create a new Person object
person.print_details()  # Print the person's details

# Edge case: empty input → handle missing name and age
person_empty = Person("", -1)  # Create a new Person object with empty input
person_empty.print_details()  # Print the person's details with default values
```
