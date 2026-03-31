---
title: "Recursive Types"
topic: "Recursive Types"
section: "typescript"
tags: "typescript, recursive-types, programming, notes, interview"
banner: "https://picsum.photos/seed/312/1200/630"
update_count: 0
---

![Recursive Types](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Recursion_diagram.jpg/1024px-Recursion_diagram.jpg)

## Introduction
Recursive types are a fundamental concept in type theory, allowing for the definition of complex data structures in a self-referential manner. In other words, a recursive type is a type that refers to itself, either directly or indirectly, in its own definition. This concept is crucial in programming languages, as it enables the creation of data structures such as trees, graphs, and lists. Recursive types are particularly important in functional programming languages, where they are used to define recursive functions and data structures.

> **Note:** Recursive types are not unique to functional programming languages and can be found in object-oriented programming languages as well. However, their usage and implementation may vary.

In real-world applications, recursive types are used to model complex data structures, such as file systems, social networks, and organizational hierarchies. For example, a file system can be represented as a tree, where each node represents a directory or file, and the edges represent the relationships between them. Recursive types provide a powerful tool for defining and manipulating such data structures.

## Core Concepts
To understand recursive types, it's essential to grasp the following key concepts:

* **Self-reference**: A type that refers to itself in its own definition.
* **Inductive definition**: A definition that is based on a set of base cases and a recursive rule.
* **Recursive function**: A function that calls itself in its own definition.
* **Type constructor**: A function that takes a type as an argument and returns a new type.

> **Tip:** When working with recursive types, it's crucial to ensure that the recursive definition is well-founded, meaning that it has a clear base case and a recursive rule that eventually terminates.

## How It Works Internally
When a recursive type is defined, the type checker must ensure that the definition is valid and consistent. Here's a step-by-step breakdown of how recursive types work internally:

1. **Type definition**: The recursive type is defined using a type constructor, which takes a type as an argument and returns a new type.
2. **Type checking**: The type checker verifies that the recursive definition is well-founded and that the type constructor is applied correctly.
3. **Type unfolding**: The type checker unfolds the recursive definition, replacing each recursive reference with the corresponding type constructor application.
4. **Type normalization**: The type checker normalizes the unfolded type, ensuring that it is in a canonical form.

## Code Examples
Here are three complete and runnable examples of recursive types in TypeScript:

### Example 1: Basic Recursive Type
```typescript
type RecursiveType = {
  value: string;
  next: RecursiveType | null;
};

const example: RecursiveType = {
  value: 'hello',
  next: {
    value: 'world',
    next: null,
  },
};
```
This example defines a simple recursive type `RecursiveType`, which has a `value` property and a `next` property that refers to another `RecursiveType` or `null`.

### Example 2: Recursive Tree
```typescript
type TreeNode = {
  value: number;
  children: TreeNode[] | null;
};

const tree: TreeNode = {
  value: 1,
  children: [
    {
      value: 2,
      children: [
        {
          value: 3,
          children: null,
        },
      ],
    },
    {
      value: 4,
      children: null,
    },
  ],
};
```
This example defines a recursive type `TreeNode`, which has a `value` property and a `children` property that refers to an array of `TreeNode` or `null`.

### Example 3: Advanced Recursive Type
```typescript
type RecursiveList<T> = {
  head: T;
  tail: RecursiveList<T> | null;
};

const exampleList: RecursiveList<number> = {
  head: 1,
  tail: {
    head: 2,
    tail: {
      head: 3,
      tail: null,
    },
  },
};
```
This example defines a recursive type `RecursiveList`, which has a `head` property and a `tail` property that refers to another `RecursiveList` or `null`.

## Visual Diagram
```mermaid
graph TD
  A[RecursiveType] --> B[Value: string]
  A --> C[Next: RecursiveType | null]
  C --> D[RecursiveType]
  C --> E[null]
  D --> F[Value: string]
  D --> G[Next: RecursiveType | null]
  G --> H[RecursiveType]
  G --> I[null]
```
This diagram illustrates the recursive structure of the `RecursiveType` type, showing how each `RecursiveType` node refers to another `RecursiveType` or `null`.

## Comparison
Here's a comparison table of different approaches to defining recursive types:

| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Recursive Type | O(n) | O(n) | Easy to define, flexible | Can lead to stack overflows | Small to medium-sized data structures |
| Inductive Type | O(n) | O(n) | More efficient, less prone to stack overflows | More complex to define | Large data structures |
| Co-recursive Type | O(n) | O(n) | Can handle mutual recursion | More complex to define | Complex data structures with mutual recursion |

## Real-world Use Cases
Here are three production examples of recursive types in real-world systems:

1. **File Systems**: The file system in an operating system can be represented as a recursive tree, where each node represents a directory or file, and the edges represent the relationships between them.
2. **Social Networks**: A social network can be represented as a recursive graph, where each node represents a user, and the edges represent the relationships between users.
3. **Database Query Optimization**: A database query optimizer can use recursive types to represent the query plan, where each node represents a query operator, and the edges represent the dependencies between operators.

## Common Pitfalls
Here are four specific mistakes to watch out for when working with recursive types:

1. **Infinite Recursion**: Failing to ensure that the recursive definition is well-founded can lead to infinite recursion, causing a stack overflow.
```typescript
// WRONG
type InfiniteType = {
  value: string;
  next: InfiniteType;
};

// RIGHT
type WellFoundedType = {
  value: string;
  next: WellFoundedType | null;
};
```
2. **Type Inconsistency**: Failing to ensure that the recursive definition is consistent can lead to type errors.
```typescript
// WRONG
type InconsistentType = {
  value: string;
  next: number;
};

// RIGHT
type ConsistentType = {
  value: string;
  next: ConsistentType | null;
};
```
3. **Loss of Type Information**: Failing to preserve type information when using recursive types can lead to type errors.
```typescript
// WRONG
type LostType = {
  value: any;
  next: LostType | null;
};

// RIGHT
type PreservedType = {
  value: string;
  next: PreservedType | null;
};
```
4. **Performance Issues**: Failing to optimize recursive types can lead to performance issues.
```typescript
// WRONG
type UnoptimizedType = {
  value: string;
  next: UnoptimizedType;
};

// RIGHT
type OptimizedType = {
  value: string;
  next: OptimizedType | null;
};
```
## Interview Tips
Here are three common interview questions on recursive types, along with weak and strong answers:

1. **What is a recursive type?**
	* Weak answer: "A recursive type is a type that refers to itself."
	* Strong answer: "A recursive type is a type that refers to itself in its own definition, allowing for the definition of complex data structures in a self-referential manner."
2. **How do you ensure that a recursive type is well-founded?**
	* Weak answer: "I just make sure that the recursive definition is consistent."
	* Strong answer: "I ensure that the recursive definition has a clear base case and a recursive rule that eventually terminates, and I use techniques such as induction to prove that the definition is well-founded."
3. **What are some common pitfalls when working with recursive types?**
	* Weak answer: "I'm not sure, but I try to avoid them."
	* Strong answer: "Some common pitfalls when working with recursive types include infinite recursion, type inconsistency, loss of type information, and performance issues, and I take steps to avoid them by ensuring that my recursive definitions are well-founded, consistent, and optimized."

## Key Takeaways
Here are six key takeaways to remember when working with recursive types:

* **Recursive types are self-referential**: A recursive type refers to itself in its own definition.
* **Well-founded definitions are crucial**: A recursive definition must have a clear base case and a recursive rule that eventually terminates.
* **Type consistency is essential**: A recursive definition must be consistent to avoid type errors.
* **Type information must be preserved**: Recursive types must preserve type information to avoid type errors.
* **Optimization is important**: Recursive types must be optimized to avoid performance issues.
* **Infinite recursion is a common pitfall**: Failing to ensure that a recursive definition is well-founded can lead to infinite recursion, causing a stack overflow.