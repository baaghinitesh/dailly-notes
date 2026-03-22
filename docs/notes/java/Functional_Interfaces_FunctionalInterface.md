---
title: "Functional Interfaces: @FunctionalInterface"
topic: "Functional Interfaces: @FunctionalInterface"
section: "java"
tags: "java, functional-interfaces, programming, notes"
banner: "https://image.pollinations.ai/prompt/Functional%20Interfaces%20@FunctionalInterface%20java%20programming?width=800&height=400&nologo=true"
update_count: 0
---

![Functional Interfaces](https://image.pollinations.ai/prompt/Functional%20Interfaces%20@FunctionalInterface%20java%20programming?width=800&height=400&nologo=true)

## Introduction
Functional interfaces are a crucial concept in Java, particularly with the introduction of lambda expressions and method references in Java 8. A functional interface is an interface that has a single abstract method (SAM). The `@FunctionalInterface` annotation is used to indicate that an interface is intended to be a functional interface. In this section, we will explore the importance of functional interfaces and the role of the `@FunctionalInterface` annotation.

## Core Concepts
A functional interface is an interface that has only one abstract method. This allows it to be used as a target for lambda expressions or method references. The `@FunctionalInterface` annotation is optional but provides several benefits, including:
- Compiler checks: The compiler checks that the interface has only one abstract method.
- Documentation: The annotation clearly indicates that the interface is intended to be used as a functional interface.
- IDE support: Many IDEs provide additional support for functional interfaces annotated with `@FunctionalInterface`, such as code completion and inspections.

Here is an example of a simple functional interface:
```java
@FunctionalInterface
interface MathOperation {
    int operation(int a, int b);
}
```
In this example, the `MathOperation` interface has a single abstract method `operation`, making it a functional interface.

## Code Examples
Here are a few examples of using functional interfaces:
```java
// Example 1: Using a lambda expression to implement a functional interface
MathOperation addition = (a, b) -> a + b;
System.out.println(addition.operation(5, 3)); // Output: 8

// Example 2: Using a method reference to implement a functional interface
MathOperation subtraction = (a, b) -> a - b;
System.out.println(subtraction.operation(10, 4)); // Output: 6

// Example 3: Using a functional interface as a higher-order function
interface Calculator {
    int calculate(int a, int b, MathOperation operation);
}

Calculator calculator = (a, b, operation) -> operation.operation(a, b);
System.out.println(calculator.calculate(7, 2, (x, y) -> x * y)); // Output: 14
```
In these examples, we demonstrate how to use lambda expressions and method references to implement functional interfaces.

## Real-world Use Cases
Functional interfaces are used extensively in Java 8's Stream API, where they are used to represent operations such as mapping, filtering, and reducing. They are also used in the `java.util.function` package, which provides a set of predefined functional interfaces for common operations such as `Predicate`, `Consumer`, and `Supplier`.

Here is an example of using the `Predicate` functional interface:
```java
import java.util.function.Predicate;

// Example: Using a predicate to filter a list
List<String> names = Arrays.asList("John", "Jane", "Bob");
Predicate<String> startsWithJ = name -> name.startsWith("J");
names.stream()
     .filter(startsWithJ)
     .forEach(System.out::println);
// Output:
// John
// Jane
```
In this example, we use the `Predicate` functional interface to represent a condition that is used to filter a list of names.

## Common Pitfalls & How to Avoid Them
One common pitfall when working with functional interfaces is to accidentally add multiple abstract methods to an interface. This can lead to compiler errors and confusing code. To avoid this, use the `@FunctionalInterface` annotation and ensure that the interface has only one abstract method.

> **Note:** If you are using an IDE, it will often provide warnings or errors when you try to add multiple abstract methods to a functional interface.

Another common pitfall is to use functional interfaces as a replacement for abstract classes or regular classes. While functional interfaces can be used to represent simple operations, they are not suitable for complex logic or stateful objects.

> **Warning:** Avoid using functional interfaces as a replacement for abstract classes or regular classes. Instead, use them to represent simple operations or conditions.

## Summary / Key Takeaways
In summary, functional interfaces are a powerful tool in Java that allow you to represent simple operations or conditions using lambda expressions or method references. The `@FunctionalInterface` annotation provides compiler checks, documentation, and IDE support for functional interfaces. When working with functional interfaces, ensure that the interface has only one abstract method and use them to represent simple operations or conditions. Avoid using functional interfaces as a replacement for abstract classes or regular classes.

Key takeaways:
* A functional interface is an interface with a single abstract method (SAM).
* The `@FunctionalInterface` annotation is optional but provides compiler checks, documentation, and IDE support.
* Functional interfaces can be used to represent simple operations or conditions using lambda expressions or method references.
* Use functional interfaces to represent simple operations or conditions, but avoid using them as a replacement for abstract classes or regular classes.