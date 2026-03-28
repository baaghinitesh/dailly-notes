---
title: "Transpilation: TypeScript → JavaScript, Kotlin → JavaScript"
topic: "Transpilation: TypeScript → JavaScript, Kotlin → JavaScript"
section: "languages-overview"
tags: "languages-overview, transpilation, programming, notes, interview"
banner: "https://picsum.photos/seed/256/1200/630"
update_count: 0
---

![Transpilation](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Typescript_logo_2020.svg/1024px-Typescript_logo_2020.svg.png)

## Introduction
Transpilation is the process of converting source code from one programming language to another. In the context of **Polyglot Programming**, transpilation is crucial for leveraging the strengths of multiple languages in a single project. For instance, **TypeScript** can be transpiled to **JavaScript**, allowing developers to write type-safe code that can run in any JavaScript environment. Similarly, **Kotlin** can be transpiled to **JavaScript**, enabling the use of Kotlin's concise and safe syntax for web development. In this article, we will delve into the world of transpilation, exploring its core concepts, internal mechanics, and real-world applications.

## Core Concepts
To understand transpilation, it's essential to grasp the following key concepts:
* **Source language**: The original language in which the code is written (e.g., TypeScript or Kotlin).
* **Target language**: The language to which the code is being transpiled (e.g., JavaScript).
* **Transpiler**: The tool responsible for performing the transpilation process (e.g., `tsc` for TypeScript or `kotlinc` for Kotlin).
* **Compilation**: The process of translating source code into machine code or an intermediate representation.

> **Note:** Transpilation is often confused with compilation, but they serve different purposes. Compilation typically involves translating source code into machine code, whereas transpilation involves translating source code from one language to another.

## How It Works Internally
The transpilation process involves several steps:
1. **Lexical analysis**: The source code is broken down into a sequence of tokens, such as keywords, identifiers, and symbols.
2. **Syntax analysis**: The tokens are parsed into an abstract syntax tree (AST), representing the source code's syntactic structure.
3. **Semantic analysis**: The AST is analyzed to ensure that the code is semantically correct, including type checking and scoping.
4. **Transformation**: The AST is transformed into an intermediate representation (IR) that can be used to generate the target language code.
5. **Code generation**: The IR is used to generate the target language code, which can be executed directly or further compiled.

> **Warning:** Transpilation can sometimes introduce performance overhead or compatibility issues if not done correctly. It's essential to choose the right transpiler and configure it properly to minimize these risks.

## Code Examples
Here are three examples of transpilation, ranging from basic to advanced:

### Example 1: Basic TypeScript → JavaScript Transpilation
```typescript
// source.ts
function add(a: number, b: number): number {
  return a + b;
}

console.log(add(2, 3));
```
```javascript
// compiled.js
function add(a, b) {
  return a + b;
}

console.log(add(2, 3));
```
This example demonstrates a simple transpilation of a TypeScript function to JavaScript.

### Example 2: Real-world Kotlin → JavaScript Transpilation
```kotlin
// source.kt
fun greet(name: String) {
  println("Hello, $name!")
}

greet("John")
```
```javascript
// compiled.js
function greet(name) {
  console.log("Hello, " + name + "!");
}

greet("John");
```
This example shows how Kotlin code can be transpiled to JavaScript, allowing for the use of Kotlin's concise syntax in web development.

### Example 3: Advanced TypeScript → JavaScript Transpilation with Decorators
```typescript
// source.ts
function logger(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  const originalMethod = descriptor.value;
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with arguments: ${args.join(", ")}`);
    return originalMethod.apply(this, args);
  };
  return descriptor;
}

class Calculator {
  @logger
  add(a: number, b: number): number {
    return a + b;
  }
}

const calculator = new Calculator();
console.log(calculator.add(2, 3));
```
```javascript
// compiled.js
function logger(target, propertyKey, descriptor) {
  const originalMethod = descriptor.value;
  descriptor.value = function (...args) {
    console.log(`Calling ${propertyKey} with arguments: ${args.join(", ")}`);
    return originalMethod.apply(this, args);
  };
  return descriptor;
}

class Calculator {
  constructor() {}
  add(a, b) {
    return a + b;
  }
}

Object.defineProperty(Calculator.prototype, "add", logger(Calculator.prototype, "add", Object.getOwnPropertyDescriptor(Calculator.prototype, "add")));

const calculator = new Calculator();
console.log(calculator.add(2, 3));
```
This example demonstrates the transpilation of a TypeScript class with a decorator, which is transformed into a JavaScript class with the equivalent functionality.

## Visual Diagram
```mermaid
graph LR
    A[Source Code] -->|Lexical Analysis|> B[Tokens]
    B -->|Syntax Analysis|> C[Abstract Syntax Tree (AST)]
    C -->|Semantic Analysis|> D[Analyzed AST]
    D -->|Transformation|> E[Intermediate Representation (IR)]
    E -->|Code Generation|> F[Target Language Code]
    F -->|Execution|> G[Result]
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#f9f,stroke:#333,stroke-width:4px
    style C fill:#f9f,stroke:#333,stroke-width:4px
    style D fill:#f9f,stroke:#333,stroke-width:4px
    style E fill:#f9f,stroke:#333,stroke-width:4px
    style F fill:#f9f,stroke:#333,stroke-width:4px
    style G fill:#f9f,stroke:#333,stroke-width:4px
```
This diagram illustrates the transpilation process, from source code to target language code execution.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| TypeScript → JavaScript | O(n) | O(n) | Type safety, compatibility with existing JavaScript code | Performance overhead, compatibility issues | Web development, enterprise applications |
| Kotlin → JavaScript | O(n) | O(n) | Concise syntax, null safety, interoperability with JavaScript | Steeper learning curve, performance overhead | Android app development, web development |
| CoffeeScript → JavaScript | O(n) | O(n) | Simplified syntax, improved readability | Performance overhead, compatibility issues | Web development, rapid prototyping |
| Dart → JavaScript | O(n) | O(n) | Strongly typed, compiled language | Performance overhead, compatibility issues | Web development, mobile app development |

> **Tip:** When choosing a transpilation approach, consider the trade-offs between performance, compatibility, and development ease. TypeScript and Kotlin are popular choices for their balance of type safety and compatibility.

## Real-world Use Cases
1. **Google**: Uses TypeScript for many of its web applications, including Google Maps and Google Drive.
2. **Microsoft**: Employs TypeScript for its Azure cloud platform and Visual Studio Code editor.
3. **Airbnb**: Utilizes Kotlin for its Android app development, taking advantage of its concise syntax and null safety features.

## Common Pitfalls
1. **Incompatible syntax**: Using language-specific features that are not supported in the target language.
2. **Type mismatches**: Failing to account for type differences between the source and target languages.
3. **Performance issues**: Introducing performance overhead due to unnecessary transpilation steps or inefficient code generation.
4. **Debugging challenges**: Difficulty in debugging transpiled code due to the lack of direct mapping between source and target code.

> **Interview:** Can you explain the differences between transpilation and compilation? How would you approach debugging a transpilation issue?

## Interview Tips
1. **Understand the transpilation process**: Be able to explain the steps involved in transpilation, from lexical analysis to code generation.
2. **Familiarize yourself with popular transpilers**: Know the strengths and weaknesses of popular transpilers, such as TypeScript and Kotlin.
3. **Practice debugging transpiled code**: Develop skills in debugging transpiled code, including identifying type mismatches and performance issues.

## Key Takeaways
* Transpilation is the process of converting source code from one language to another.
* TypeScript and Kotlin are popular languages for transpilation due to their type safety and compatibility features.
* The transpilation process involves lexical analysis, syntax analysis, semantic analysis, transformation, and code generation.
* Performance overhead and compatibility issues are common pitfalls in transpilation.
* Debugging transpiled code can be challenging due to the lack of direct mapping between source and target code.
* Popular transpilers include `tsc` for TypeScript and `kotlinc` for Kotlin.
* Time complexity and space complexity are important considerations in transpilation, with most approaches having a time complexity of O(n) and space complexity of O(n).