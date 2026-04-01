---
title: "Interface Default Methods"
topic: "Interface Default Methods"
section: "kotlin"
tags: "kotlin, interface-default-methods, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/kotlin%20Interface%20Default%20Methods%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![Interface Default Methods](https://kotlinlang.org/assets/images/fun.png)

## Introduction
**Interface default methods** are a feature in Kotlin that allows interfaces to have methods with default implementations. This means that when a class implements an interface, it does not need to provide an implementation for every method in the interface. Instead, it can use the default implementation provided by the interface. This feature is particularly useful when working with legacy code or when you want to add new functionality to an existing interface without breaking existing implementations.

In real-world scenarios, interface default methods are used extensively in frameworks and libraries, such as the **Java Standard Library** and **Kotlinx Coroutines**. For example, the `Iterable` interface in Kotlin has a default implementation for the `forEach` method, which allows you to iterate over a collection using a lambda expression.

> **Note:** Interface default methods are also known as **defender methods** or **virtual extension methods** in other programming languages.

## Core Concepts
To understand interface default methods, you need to grasp the following core concepts:

* **Interface**: A contract that specifies a set of methods that must be implemented by any class that implements it.
* **Default method**: A method in an interface that has a default implementation, which can be used by classes that implement the interface.
* **Implementation**: The code that provides the behavior for a method in an interface.

Mental models that can help you understand interface default methods include:

* Thinking of an interface as a contract that specifies a set of methods that must be implemented.
* Visualizing a default method as a "fallback" implementation that can be used by classes that implement the interface.

Key terminology includes:

* **Abstract method**: A method in an interface that does not have a default implementation and must be implemented by any class that implements the interface.
* **Concrete method**: A method in an interface that has a default implementation and can be used by classes that implement the interface.

## How It Works Internally
When a class implements an interface, the Kotlin compiler checks if the class provides an implementation for every method in the interface. If a method has a default implementation, the compiler will use that implementation if the class does not provide one.

Here's a step-by-step breakdown of how interface default methods work internally:

1. The Kotlin compiler checks if a class implements an interface.
2. If the class implements an interface, the compiler checks if the class provides an implementation for every method in the interface.
3. If a method has a default implementation, the compiler will use that implementation if the class does not provide one.
4. The compiler will generate bytecode that calls the default implementation if the class does not provide an implementation for a method.

> **Warning:** If a class implements multiple interfaces that have default implementations for the same method, the compiler will throw an error.

## Code Examples
### Example 1: Basic Interface Default Method
```kotlin
interface Printable {
    fun print() {
        println("Default print implementation")
    }
}

class Document : Printable()

fun main() {
    val document = Document()
    document.print() // prints "Default print implementation"
}
```
In this example, the `Printable` interface has a default implementation for the `print` method. The `Document` class implements the `Printable` interface but does not provide an implementation for the `print` method. Therefore, the default implementation is used.

### Example 2: Real-World Interface Default Method
```kotlin
interface Iterable<T> {
    fun iterator(): Iterator<T>
    fun forEach(action: (T) -> Unit) {
        val iterator = iterator()
        while (iterator.hasNext()) {
            action(iterator.next())
        }
    }
}

class List<T> : Iterable<T> {
    override fun iterator(): Iterator<T> {
        // implementation of iterator
    }
}

fun main() {
    val list = List<Int>()
    list.forEach { println(it) } // uses default implementation of forEach
}
```
In this example, the `Iterable` interface has a default implementation for the `forEach` method. The `List` class implements the `Iterable` interface and provides an implementation for the `iterator` method. The `forEach` method is used without providing an implementation, and the default implementation is used instead.

### Example 3: Advanced Interface Default Method
```kotlin
interface Logger {
    fun log(message: String) {
        println("Default log implementation: $message")
    }
    fun logError(message: String) {
        println("Default error log implementation: $message")
    }
}

class ConsoleLogger : Logger {
    override fun log(message: String) {
        println("Console log implementation: $message")
    }
}

fun main() {
    val logger = ConsoleLogger()
    logger.log("Hello, world!") // uses custom implementation of log
    logger.logError("Error occurred") // uses default implementation of logError
}
```
In this example, the `Logger` interface has default implementations for the `log` and `logError` methods. The `ConsoleLogger` class implements the `Logger` interface and provides a custom implementation for the `log` method. The `logError` method is used without providing an implementation, and the default implementation is used instead.

## Visual Diagram
```mermaid
flowchart TD
    A[Interface] -->|implements|> B[Class]
    B -->|uses|> C[Default Method]
    C -->|calls|> D[Default Implementation]
    D -->|returns|> E[Result]
    E -->|used by|> B
    B -->|provides|> F[Custom Implementation]
    F -->|overrides|> C
```
This diagram illustrates the relationship between an interface, a class, and a default method. The class implements the interface and uses the default method, which calls the default implementation and returns a result. The class can also provide a custom implementation that overrides the default method.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Interface Default Method | O(1) | O(1) | Provides a default implementation for methods, reduces code duplication | Can lead to multiple inheritance issues | Legacy code, frameworks, and libraries |
| Abstract Class | O(1) | O(1) | Provides a way to implement abstract methods, can be used as a base class | Can lead to tight coupling, less flexible than interfaces | Complex hierarchies, base classes |
| Trait | O(1) | O(1) | Provides a way to implement reusable code, can be used to compose classes | Can lead to multiple inheritance issues, less flexible than interfaces | Reusable code, composition |
| Mixin | O(1) | O(1) | Provides a way to implement reusable code, can be used to compose classes | Can lead to multiple inheritance issues, less flexible than interfaces | Reusable code, composition |

> **Tip:** When choosing an approach, consider the trade-offs between flexibility, reusability, and maintainability.

## Real-world Use Cases
1. **Java Standard Library**: The `Iterable` interface in Java has a default implementation for the `forEach` method, which allows you to iterate over a collection using a lambda expression.
2. **Kotlinx Coroutines**: The `CoroutineScope` interface in Kotlinx Coroutines has default implementations for the `launch` and `async` methods, which allow you to launch and await coroutines.
3. **Android Framework**: The `View` class in the Android framework has default implementations for the `onClickListener` and `onLongClickListener` methods, which allow you to handle click and long click events.

> **Interview:** Can you explain the difference between an interface and an abstract class? How would you choose between the two?

## Common Pitfalls
1. **Multiple Inheritance Issues**: When a class implements multiple interfaces that have default implementations for the same method, the compiler will throw an error.
```kotlin
interface Interface1 {
    fun method() {
        println("Interface1 implementation")
    }
}

interface Interface2 {
    fun method() {
        println("Interface2 implementation")
    }
}

class Class : Interface1, Interface2 {
    // compiler error: multiple inheritance issue
}
```
To fix this issue, you can provide a custom implementation for the method in the class.
```kotlin
class Class : Interface1, Interface2 {
    override fun method() {
        println("Custom implementation")
    }
}
```
2. **Tight Coupling**: When a class implements an interface and provides a custom implementation for every method, it can lead to tight coupling between the class and the interface.
```kotlin
interface Interface {
    fun method1()
    fun method2()
}

class Class : Interface {
    override fun method1() {
        // implementation
    }

    override fun method2() {
        // implementation
    }
}
```
To avoid this issue, you can use abstract classes or traits to provide a way to implement abstract methods.
3. **Less Flexible than Interfaces**: When a class implements an interface and provides a custom implementation for every method, it can make the class less flexible than if it had used an interface.
```kotlin
interface Interface {
    fun method1()
    fun method2()
}

class Class : Interface {
    override fun method1() {
        // implementation
    }

    override fun method2() {
        // implementation
    }
}
```
To avoid this issue, you can use interfaces to provide a way to define a contract without providing an implementation.
4. **Reusability Issues**: When a class implements an interface and provides a custom implementation for every method, it can make the class less reusable than if it had used an interface.
```kotlin
interface Interface {
    fun method1()
    fun method2()
}

class Class : Interface {
    override fun method1() {
        // implementation
    }

    override fun method2() {
        // implementation
    }
}
```
To avoid this issue, you can use interfaces to provide a way to define a contract without providing an implementation.

## Interview Tips
1. **What is the difference between an interface and an abstract class?**
	* Weak answer: "An interface is a contract, and an abstract class is a class that can't be instantiated."
	* Strong answer: "An interface is a contract that specifies a set of methods that must be implemented, while an abstract class is a class that provides a way to implement abstract methods and can be used as a base class. Interfaces are more flexible and reusable than abstract classes."
2. **How would you choose between an interface and an abstract class?**
	* Weak answer: "I would choose an interface if I need to define a contract, and an abstract class if I need to provide an implementation."
	* Strong answer: "I would choose an interface if I need to define a contract without providing an implementation, and an abstract class if I need to provide a way to implement abstract methods and can be used as a base class. I would consider the trade-offs between flexibility, reusability, and maintainability when making this choice."
3. **Can you explain the concept of interface default methods?**
	* Weak answer: "Interface default methods are methods that have a default implementation."
	* Strong answer: "Interface default methods are methods that have a default implementation provided by the interface, which can be used by classes that implement the interface. This feature allows for more flexibility and reusability in programming, and can be used to provide a way to implement methods that have a default behavior."

## Key Takeaways
* **Interface default methods** provide a way to define a contract with default implementations for methods.
* **Abstract classes** provide a way to implement abstract methods and can be used as a base class.
* **Traits** provide a way to implement reusable code and can be used to compose classes.
* **Mixins** provide a way to implement reusable code and can be used to compose classes.
* **Multiple inheritance issues** can occur when a class implements multiple interfaces that have default implementations for the same method.
* **Tight coupling** can occur when a class implements an interface and provides a custom implementation for every method.
* **Less flexibility than interfaces** can occur when a class implements an interface and provides a custom implementation for every method.
* **Reusability issues** can occur when a class implements an interface and provides a custom implementation for every method.
* The **trade-offs between flexibility, reusability, and maintainability** should be considered when choosing between an interface, an abstract class, a trait, or a mixin.
* **Interface default methods** can be used to provide a way to implement methods that have a default behavior.
* The **default implementation** of a method can be overridden by a class that implements the interface.
* **Custom implementations** can be provided by classes that implement an interface to override the default implementation of a method.