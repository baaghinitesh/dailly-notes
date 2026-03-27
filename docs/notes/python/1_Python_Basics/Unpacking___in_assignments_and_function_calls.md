---
title: "Unpacking: *, ** in assignments and function calls"
topic: "Unpacking: *, ** in assignments and function calls"
section: "python"
tags: "python, unpacking, programming, notes, interview"
banner: "https://picsum.photos/seed/206/1200/630"
update_count: 0
---

![topic](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python.svg/2000px-Python.svg.png)

## Introduction
**Unpacking** in Python is a powerful feature that allows you to assign values from iterables (such as lists, tuples, or dictionaries) to multiple variables. It is a fundamental concept in Python programming and is used extensively in various scenarios, including function calls, assignments, and data manipulation. In this section, we will delve into the world of unpacking, exploring its syntax, benefits, and real-world applications.

Unpacking is particularly useful when working with functions that return multiple values or when dealing with data structures that contain multiple elements. It simplifies the process of assigning values to variables, making the code more readable and efficient. For instance, consider a function that returns a tuple containing a user's name, age, and location. Without unpacking, you would need to access each element of the tuple using indexing, which can be cumbersome and prone to errors. With unpacking, you can assign the values to separate variables in a single line of code.

> **Note:** Unpacking is a key feature in Python that sets it apart from other programming languages. It is an essential tool for any Python developer, and mastering it can significantly improve your coding skills and productivity.

## Core Concepts
At its core, unpacking involves using the `*` and `**` operators to assign values from iterables to variables. The `*` operator is used to unpack lists and tuples, while the `**` operator is used to unpack dictionaries.

*   **Unpacking lists and tuples:** When using the `*` operator, Python assigns the values from the list or tuple to the variables on the left side of the assignment. If the number of variables is less than the number of elements in the list or tuple, Python will raise a `ValueError`. However, if the number of variables is more than the number of elements, Python will assign `None` to the remaining variables.
*   **Unpacking dictionaries:** When using the `**` operator, Python assigns the key-value pairs from the dictionary to the variables on the left side of the assignment. The keys are used as variable names, and the values are assigned to those variables.

> **Tip:** When working with unpacking, it's essential to ensure that the number of variables matches the number of elements in the iterable. This can help prevent errors and make the code more reliable.

## How It Works Internally
When you use the `*` or `**` operator in an assignment, Python performs the following steps:

1.  **Evaluation:** Python evaluates the expression on the right side of the assignment, which can be a list, tuple, dictionary, or any other iterable.
2.  **Unpacking:** Python unpacks the values from the iterable and assigns them to the variables on the left side of the assignment.
3.  **Assignment:** Python performs the assignment, binding the values to the variables.

The time complexity of unpacking is O(n), where n is the number of elements in the iterable. The space complexity is also O(n), as Python needs to create new variables to store the unpacked values.

> **Warning:** Unpacking can raise a `ValueError` if the number of variables does not match the number of elements in the iterable. It's essential to handle this error properly to prevent crashes and ensure reliable code execution.

## Code Examples
### Example 1: Basic Unpacking
```python
# Define a tuple containing three values
user_info = ("John", 30, "New York")

# Unpack the values into separate variables
name, age, location = user_info

# Print the values
print("Name:", name)
print("Age:", age)
print("Location:", location)
```

### Example 2: Unpacking with the `*` Operator
```python
# Define a list containing five values
numbers = [1, 2, 3, 4, 5]

# Unpack the values into separate variables using the `*` operator
first, *middle, last = numbers

# Print the values
print("First:", first)
print("Middle:", middle)
print("Last:", last)
```

### Example 3: Unpacking Dictionaries with the `**` Operator
```python
# Define a dictionary containing three key-value pairs
user_data = {"name": "Jane", "age": 25, "location": "London"}

# Define a function that takes three arguments
def print_user_info(name, age, location):
    print("Name:", name)
    print("Age:", age)
    print("Location:", location)

# Unpack the dictionary into keyword arguments using the `**` operator
print_user_info(**user_data)
```

## Visual Diagram
```mermaid
graph LR
    A[Iterable] -->|Evaluation|> B[Unpacking]
    B -->|Assignment|> C[Variables]
    C -->|Binding|> D[Values]
    D -->|Error Handling|> E[Error]
    E -->|Exception|> F[Crash]
    F -->|Reliable Code|> G[Execution]
    G -->|Output|> H[Result]
    H -->|Success|> I[Done]
    I -->|Repeat|> A
```

The diagram illustrates the process of unpacking in Python, from evaluation to assignment and error handling. It highlights the importance of proper error handling to prevent crashes and ensure reliable code execution.

> **Interview:** Can you explain the difference between the `*` and `**` operators in Python? How do they relate to unpacking?

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Unpacking with `*` | O(n) | O(n) | Simplifies assignments, improves readability | Raises `ValueError` if lengths mismatch | Assigning values from lists or tuples to variables |
| Unpacking with `**` | O(n) | O(n) | Simplifies assignments, improves readability | Raises `ValueError` if keys mismatch | Assigning values from dictionaries to variables |
| Indexing | O(1) | O(1) | Fast and efficient | Cumbersome and prone to errors | Accessing specific elements in lists or tuples |
| Dictionary Access | O(1) | O(1) | Fast and efficient | Cumbersome and prone to errors | Accessing specific key-value pairs in dictionaries |

## Real-world Use Cases
1.  **Data Analysis:** Unpacking is essential in data analysis, where you often need to assign values from datasets to variables for further processing. For instance, the popular `pandas` library uses unpacking to assign values from DataFrames to variables.
2.  **Web Development:** In web development, unpacking is used to assign values from request objects to variables. For example, the `Flask` framework uses unpacking to assign values from request forms to variables.
3.  **Scientific Computing:** Unpacking is used in scientific computing to assign values from numerical computations to variables. For instance, the `NumPy` library uses unpacking to assign values from arrays to variables.

> **Tip:** Unpacking can simplify your code and improve readability. However, it's essential to use it judiciously and handle errors properly to prevent crashes and ensure reliable code execution.

## Common Pitfalls
1.  **Length Mismatch:** Unpacking can raise a `ValueError` if the number of variables does not match the number of elements in the iterable.
2.  **Key Mismatch:** Unpacking dictionaries can raise a `ValueError` if the keys in the dictionary do not match the variable names.
3.  **Error Handling:** Failing to handle errors properly can lead to crashes and unreliable code execution.
4.  **Performance:** Unpacking can have a performance overhead due to the creation of new variables and the assignment of values.

> **Warning:** Unpacking can be a powerful tool, but it requires careful handling to avoid errors and ensure reliable code execution.

## Interview Tips
1.  **Explain Unpacking:** Be prepared to explain the concept of unpacking, including the `*` and `**` operators, and how they relate to assignments and function calls.
2.  **Provide Examples:** Provide examples of using unpacking in different scenarios, such as assigning values from lists or dictionaries to variables.
3.  **Discuss Error Handling:** Discuss the importance of error handling when using unpacking, including how to handle `ValueError` exceptions and prevent crashes.

> **Interview:** Can you write a function that takes a list of numbers as input and returns the sum of the numbers using unpacking?

## Key Takeaways
*   Unpacking is a powerful feature in Python that simplifies assignments and improves readability.
*   The `*` operator is used to unpack lists and tuples, while the `**` operator is used to unpack dictionaries.
*   Unpacking can raise a `ValueError` if the number of variables does not match the number of elements in the iterable.
*   Error handling is essential when using unpacking to prevent crashes and ensure reliable code execution.
*   Unpacking has a time complexity of O(n) and a space complexity of O(n), where n is the number of elements in the iterable.
*   Unpacking is widely used in data analysis, web development, and scientific computing.
*   Mastering unpacking can significantly improve your coding skills and productivity.
*   Always use unpacking judiciously and handle errors properly to ensure reliable code execution.