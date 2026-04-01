---
title: "Concepts (C++20): requires Clause, Named Concepts"
topic: "Concepts (C++20): requires Clause, Named Concepts"
section: "cpp"
tags: "cpp, concepts-(c++20), programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/cpp%20Concepts%20(C++20)%20requires%20Clause,%20Named%20Concepts%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![Concepts (C++20)](https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/ISO_C%2B%2B_Logo.svg/2000px-ISO_C%2B%2B_Logo.svg.png)

## Introduction
The **requires clause** and **named concepts** are two fundamental features introduced in C++20, which aim to simplify and improve the usage of templates in C++. These features enable developers to define and constrain templates using a more expressive and flexible syntax. In this section, we will delve into the world of C++20 concepts, exploring their purpose, real-world relevance, and importance for every engineer.

C++ templates have been a powerful tool for generic programming since their introduction in C++98. However, their usage has been limited by the lack of a standardized way to constrain and define template parameters. The **requires clause** and **named concepts** address this issue by providing a declarative syntax for specifying template constraints, making it easier to write and maintain generic code.

> **Note:** The **requires clause** and **named concepts** are part of the C++20 standard, and their adoption is expected to significantly improve the way developers write and use templates in C++.

## Core Concepts
To understand the **requires clause** and **named concepts**, it is essential to grasp the following core concepts:

* **Concepts**: A concept is a set of constraints that a type must satisfy to be used as a template parameter. Concepts can be defined using the `concept` keyword and can include various constraints, such as type requirements, function requirements, and variable requirements.
* **Requires clause**: The **requires clause** is a syntax element that allows developers to specify constraints on template parameters. It consists of the `requires` keyword followed by a sequence of constraints, which can include type requirements, function requirements, and variable requirements.
* **Named concepts**: A named concept is a concept that has been given a name, allowing it to be reused throughout the code. Named concepts can be defined using the `concept` keyword and can be used to constrain template parameters.

> **Tip:** Named concepts can be used to simplify the definition of complex constraints and to improve code readability.

## How It Works Internally
The **requires clause** and **named concepts** work internally by allowing the compiler to check the constraints on template parameters at compile-time. When a template is instantiated, the compiler checks the constraints specified in the **requires clause** and ensures that the template parameters satisfy the constraints.

Here is a step-by-step breakdown of how it works:

1. The compiler parses the template definition and identifies the **requires clause**.
2. The compiler checks the constraints specified in the **requires clause** and ensures that the template parameters satisfy the constraints.
3. If the constraints are satisfied, the compiler instantiates the template.
4. If the constraints are not satisfied, the compiler reports an error.

> **Warning:** The **requires clause** and **named concepts** are not a runtime mechanism; they are a compile-time feature. Therefore, any errors related to constraint satisfaction will be reported at compile-time.

## Code Examples
Here are three complete and runnable code examples that demonstrate the usage of the **requires clause** and **named concepts**:

### Example 1: Basic usage of the **requires clause**
```cpp
template<typename T>
requires requires(T a) { { a + a } -> std::same_as<T>; }
T add(T a, T b) {
    return a + b;
}

int main() {
    int a = 5;
    int b = 10;
    int result = add(a, b);
    return 0;
}
```
This example demonstrates the basic usage of the **requires clause** to constrain a template parameter.

### Example 2: Defining a named concept
```cpp
template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};

template<Addable T>
T add(T a, T b) {
    return a + b;
}

int main() {
    int a = 5;
    int b = 10;
    int result = add(a, b);
    return 0;
}
```
This example demonstrates the definition of a named concept `Addable` and its usage to constrain a template parameter.

### Example 3: Advanced usage of the **requires clause** and named concepts
```cpp
template<typename T>
concept Container = requires(T a) {
    { a.begin() } -> std::input_iterator;
    { a.end() } -> std::input_iterator;
};

template<Container T>
void printContainer(T container) {
    for (auto it = container.begin(); it != container.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> vec = {1, 2, 3, 4, 5};
    printContainer(vec);
    return 0;
}
```
This example demonstrates the advanced usage of the **requires clause** and named concepts to constrain a template parameter and define a generic function.

## Visual Diagram
```mermaid
flowchart TD
    A[Template Definition] -->|requires clause|> B[Constraint Checking]
    B -->|satisfied|> C[Template Instantiation]
    B -->|not satisfied|> D[Error Reporting]
    C -->|instantiated|> E[Code Generation]
    E -->|generated|> F[Binary Code]
    F -->|executed|> G[Program Execution]
    D -->|reported|> H[Error Handling]
```
This diagram illustrates the internal workflow of the **requires clause** and **named concepts**, from template definition to code generation and execution.

## Comparison
The following table compares the **requires clause** and **named concepts** with other C++ features:

| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
|----------|----------------|-----------------|------|------|----------|
| **requires clause** | O(1) | O(1) | Simplifies template constraints, improves code readability | Limited to compile-time checking | Generic programming, metaprogramming |
| **named concepts** | O(1) | O(1) | Reusable, improves code readability | Limited to compile-time checking | Generic programming, metaprogramming |
| SFINAE | O(n) | O(n) | Flexible, allows for runtime checking | Complex, error-prone | Generic programming, metaprogramming |
| Tag dispatching | O(n) | O(n) | Flexible, allows for runtime checking | Complex, error-prone | Generic programming, metaprogramming |

> **Interview:** What is the main difference between the **requires clause** and SFINAE? Answer: The **requires clause** is a declarative syntax for specifying template constraints, while SFINAE is a imperative approach that relies on function overload resolution.

## Real-world Use Cases
The **requires clause** and **named concepts** have numerous real-world applications, including:

* **Google's Abseil library**: Abseil is a C++ library developed by Google that provides a set of reusable, generic components for building C++ applications. Abseil heavily relies on the **requires clause** and **named concepts** to define and constrain its generic components.
* **Microsoft's STL**: The Microsoft implementation of the C++ Standard Template Library (STL) uses the **requires clause** and **named concepts** to define and constrain its generic components.
* **LLVM**: The LLVM compiler infrastructure uses the **requires clause** and **named concepts** to define and constrain its generic components, such as the `std::vector` class.

## Common Pitfalls
Here are some common pitfalls to avoid when using the **requires clause** and **named concepts**:

* **Incorrect constraint ordering**: Incorrect ordering of constraints can lead to unexpected behavior or errors. For example, the following code will not compile:
```cpp
template<typename T>
requires requires(T a) { { a + a } -> std::same_as<T>; } && requires(T b) { { b + b } -> std::same_as<T>; }
T add(T a, T b) {
    return a + b;
}
```
The correct ordering is:
```cpp
template<typename T>
requires requires(T a, T b) { { a + b } -> std::same_as<T>; }
T add(T a, T b) {
    return a + b;
}
```
* **Missing constraints**: Failing to specify necessary constraints can lead to unexpected behavior or errors. For example, the following code will not compile:
```cpp
template<typename T>
T add(T a, T b) {
    return a + b;
}
```
The correct code is:
```cpp
template<typename T>
requires requires(T a, T b) { { a + b } -> std::same_as<T>; }
T add(T a, T b) {
    return a + b;
}
```
* **Incorrect concept definition**: Incorrectly defining a concept can lead to unexpected behavior or errors. For example, the following code will not compile:
```cpp
template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};

template<Addable T>
T add(T a, T b) {
    return a + b;
}
```
The correct definition is:
```cpp
template<typename T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
    { b + a } -> std::same_as<T>;
};

template<Addable T>
T add(T a, T b) {
    return a + b;
}
```
> **Tip:** Always carefully review and test your code to ensure that the **requires clause** and **named concepts** are used correctly.

## Interview Tips
Here are some common interview questions related to the **requires clause** and **named concepts**, along with sample answers:

* **What is the main difference between the **requires clause** and SFINAE?**
Answer: The **requires clause** is a declarative syntax for specifying template constraints, while SFINAE is an imperative approach that relies on function overload resolution.
* **How do you define a named concept in C++20?**
Answer: A named concept is defined using the `concept` keyword, followed by the concept name and a sequence of constraints.
* **What is the purpose of the **requires clause** in C++20?**
Answer: The **requires clause** is used to specify constraints on template parameters, allowing for more expressive and flexible generic programming.

> **Warning:** Be prepared to answer questions about the **requires clause** and **named concepts** in the context of C++20 and generic programming.

## Key Takeaways
Here are the key takeaways from this section:

* The **requires clause** and **named concepts** are fundamental features in C++20 for simplifying and improving the usage of templates.
* The **requires clause** is a declarative syntax for specifying template constraints.
* Named concepts are reusable, named sets of constraints that can be used to constrain template parameters.
* The **requires clause** and **named concepts** work internally by allowing the compiler to check constraints at compile-time.
* The **requires clause** and **named concepts** have numerous real-world applications, including Google's Abseil library, Microsoft's STL, and LLVM.
* Common pitfalls to avoid include incorrect constraint ordering, missing constraints, and incorrect concept definition.
* The **requires clause** and **named concepts** are essential topics in C++20 and generic programming, and developers should be prepared to answer questions about them in interviews.