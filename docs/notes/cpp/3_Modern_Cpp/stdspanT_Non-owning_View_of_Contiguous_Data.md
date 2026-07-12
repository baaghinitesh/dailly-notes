---
title: "std::span<T>: Non-owning View of Contiguous Data"
topic: "std::span<T>: Non-owning View of Contiguous Data"
section: "cpp"
tags: "cpp, std, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/cpp%20stdspan<T>%20Non-owning%20View%20of%20Contiguous%20Data%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![std::span](https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/C%2B%2B_Logo.svg/1024px-C%2B%2B_Logo.svg.png)

## Introduction
**std::span<T>** is a non-owning view of contiguous data, introduced in C++20. It provides a safe and efficient way to work with arrays, vectors, and other contiguous containers. This class template allows you to create a view of a contiguous sequence of objects, without taking ownership of the data. **std::span<T>** is a crucial component of modern C++ programming, and every engineer should understand its benefits and usage. In real-world scenarios, **std::span<T>** is used in various applications, such as data processing, image analysis, and scientific simulations, where efficient and safe data access is essential.

## Core Concepts
A **std::span<T>** object represents a non-owning view of a contiguous sequence of objects of type **T**. It consists of a pointer to the first element and a size, which represents the number of elements in the sequence. The key terminology associated with **std::span<T>** includes:
* **Contiguous data**: A sequence of objects stored in adjacent memory locations.
* **Non-owning view**: A view of the data that does not take ownership of the underlying memory.
* **Span**: A **std::span<T>** object that represents a view of a contiguous sequence of objects.

> **Note:** **std::span<T>** is a lightweight object, with a size similar to a pair of pointers, making it efficient for passing around views of data.

## How It Works Internally
**std::span<T>** works by storing a pointer to the first element of the contiguous sequence and a size, which represents the number of elements in the sequence. The internal mechanics of **std::span<T>** can be broken down into the following steps:
1. Construction: A **std::span<T>** object is constructed by providing a pointer to the first element and a size.
2. Access: The **std::span<T>** object provides access to the underlying data through its member functions, such as **data()** and **size()**.
3. Iteration: The **std::span<T>** object can be iterated over using its member functions, such as **begin()** and **end()**.

> **Warning:** When working with **std::span<T>**, it is essential to ensure that the underlying data remains valid for the lifetime of the span.

## Code Examples
### Example 1: Basic Usage
```cpp
#include <span>
#include <iostream>

int main() {
    int arr[] = {1, 2, 3, 4, 5};
    std::span<int> span(arr, 5);

    for (int i : span) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}
```
This example demonstrates the basic usage of **std::span<T>**, creating a span from an array and iterating over its elements.

### Example 2: Real-World Pattern
```cpp
#include <span>
#include <vector>
#include <iostream>

void processData(std::span<int> data) {
    for (int i : data) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    processData(vec);

    return 0;
}
```
This example demonstrates a real-world pattern, where a function takes a **std::span<T>** as an argument, allowing it to work with different types of contiguous data.

### Example 3: Advanced Usage
```cpp
#include <span>
#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::span<int> span(vec);

    std::sort(span.begin(), span.end());

    for (int i : span) {
        std::cout << i << " ";
    }
    std::cout << std::endl;

    return 0;
}
```
This example demonstrates advanced usage of **std::span<T>**, using it with the **std::sort** algorithm to sort the underlying data.

## Visual Diagram
```mermaid
flowchart TD
    A[Contiguous Data] -->| pointer | B["std::span<T>"]
    B -->| size | C["std::span<T>"]
    C -->| data() | D[Underlying Data]
    D -->| size() | E["std::span<T>"]
    E -->| begin() | F[Iterator]
    F -->| end() | G[Iterator]
    G -->| iteration | H["std::span<T>"]
    H -->| access | I[Underlying Data]
    I -->| modification | J["std::span<T>"]
    J -->| validation | K["std::span<T>"]
    K -->| error handling | L[Error]
```
This diagram illustrates the internal mechanics of **std::span<T>**, showing how it works with contiguous data, provides access to the underlying data, and handles iteration and modification.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| **std::span<T>** | O(1) | O(1) | Safe, efficient, and flexible | Limited to contiguous data | Data processing, image analysis, and scientific simulations |
| **std::vector** | O(1) | O(n) | Dynamic, resizeable, and owning | Heavyweight, slower than **std::span<T>** | General-purpose programming, where dynamic memory allocation is necessary |
| **std::array** | O(1) | O(n) | Fixed-size, owning, and efficient | Limited to fixed-size arrays | Embedded systems, real-time programming, and performance-critical code |
| **std::string** | O(1) | O(n) | Dynamic, resizeable, and owning | Heavyweight, slower than **std::span<T>**, and limited to character data | Text processing, parsing, and serialization |

> **Tip:** When working with contiguous data, **std::span<T>** is often the best choice due to its safety, efficiency, and flexibility.

## Real-world Use Cases
1. **Google's TensorFlow**: Uses **std::span<T>** to provide a safe and efficient way to work with tensors and arrays.
2. **Microsoft's DirectX**: Employs **std::span<T>** to handle contiguous data in graphics and game development.
3. **Intel's OpenVINO**: Utilizes **std::span<T>** to optimize data processing and inference in machine learning and computer vision applications.

## Common Pitfalls
1. **Invalidating the underlying data**: Failing to ensure that the underlying data remains valid for the lifetime of the span.
```cpp
int* arr = new int[5];
std::span<int> span(arr, 5);
delete[] arr; // Invalidates the underlying data
```
2. **Using **std::span<T>** with non-contiguous data**: Attempting to use **std::span<T>** with non-contiguous data, such as a linked list.
```cpp
std::list<int> list = {1, 2, 3, 4, 5};
std::span<int> span(list.begin(), list.size()); // Invalid usage
```
3. **Modifying the underlying data**: Modifying the underlying data while iterating over the span.
```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
std::span<int> span(vec);
for (int i : span) {
    vec.push_back(i); // Modifies the underlying data
}
```
4. **Ignoring the size**: Ignoring the size of the span and accessing out-of-bounds elements.
```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};
std::span<int> span(vec);
std::cout << span[10]; // Accesses out-of-bounds element
```

## Interview Tips
1. **What is **std::span<T>** and how does it work?**: A strong answer should explain the purpose of **std::span<T>**, its internal mechanics, and its benefits.
2. **How do you use **std::span<T>** with contiguous data?**: A weak answer might describe using **std::span<T>** with non-contiguous data, while a strong answer should demonstrate its usage with arrays, vectors, and other contiguous containers.
3. **What are the advantages and disadvantages of using **std::span<T>**?**: A strong answer should discuss the safety, efficiency, and flexibility of **std::span<T>**, as well as its limitations and potential pitfalls.

> **Interview:** When asked about **std::span<T>**, be prepared to explain its purpose, internal mechanics, and benefits, as well as demonstrate its usage with contiguous data and discuss its advantages and disadvantages.

## Key Takeaways
* **std::span<T>** is a non-owning view of contiguous data.
* **std::span<T>** provides a safe and efficient way to work with arrays, vectors, and other contiguous containers.
* **std::span<T>** has a size similar to a pair of pointers, making it lightweight and efficient.
* **std::span<T>** is limited to contiguous data and does not take ownership of the underlying memory.
* **std::span<T>** is a crucial component of modern C++ programming and is used in various applications, such as data processing, image analysis, and scientific simulations.
* **std::span<T>** has a time complexity of O(1) and a space complexity of O(1).
* **std::span<T>** is flexible and can be used with different types of contiguous data.
* **std::span<T>** requires careful handling to avoid invalidating the underlying data or accessing out-of-bounds elements.