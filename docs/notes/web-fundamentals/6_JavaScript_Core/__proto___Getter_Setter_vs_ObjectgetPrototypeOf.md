---
title: "`__proto__` Getter/Setter vs `Object.getPrototypeOf()`"
topic: "`__proto__` Getter/Setter vs `Object.getPrototypeOf()`"
section: "web-fundamentals"
tags: "web-fundamentals, `__proto__`-getter-setter-vs-`object.getprototypeof()`, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/web-fundamentals%20`__proto__`%20GetterSetter%20vs%20`Object.getPrototypeOf()`%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![topic](https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/JavaScript_logo.svg/1200px-JavaScript_logo.svg.png)

## Introduction
The `__proto__` getter/setter and `Object.getPrototypeOf()` are two fundamental concepts in JavaScript that allow developers to access and manipulate the prototype chain of an object. The prototype chain is a crucial aspect of JavaScript's object-oriented programming model, as it enables inheritance and method overriding. In this section, we will delve into the world of `__proto__` and `Object.getPrototypeOf()`, exploring their differences, use cases, and best practices.

> **Note:** Understanding the `__proto__` getter/setter and `Object.getPrototypeOf()` is essential for any JavaScript developer, as it allows them to write more efficient, scalable, and maintainable code.

In real-world applications, the `__proto__` getter/setter and `Object.getPrototypeOf()` are used extensively in frameworks and libraries such as React, Angular, and Vue.js. For instance, React uses the `__proto__` getter to implement its virtual DOM, while Angular uses `Object.getPrototypeOf()` to create a prototype chain for its components.

## Core Concepts
Before diving into the implementation details, let's define some key terms:

* **Prototype chain**: A sequence of objects that are linked together through their `__proto__` properties.
* **`__proto__` getter/setter**: A property that allows developers to access and modify the prototype of an object.
* **`Object.getPrototypeOf()`**: A method that returns the prototype of an object.
* **Inheritance**: The process of creating a new object that inherits the properties and methods of an existing object.

> **Tip:** When working with the `__proto__` getter/setter and `Object.getPrototypeOf()`, it's essential to understand the concept of inheritance and how it affects the prototype chain.

## How It Works Internally
When an object is created in JavaScript, it is linked to its prototype through the `__proto__` property. The `__proto__` property is a reference to the prototype object, which contains the methods and properties that are inherited by the object.

Here's a step-by-step breakdown of how the `__proto__` getter/setter and `Object.getPrototypeOf()` work:

1. **Object creation**: An object is created using the `new` keyword or the `Object.create()` method.
2. **Prototype linking**: The object is linked to its prototype through the `__proto__` property.
3. **`__proto__` getter**: The `__proto__` getter returns the prototype object linked to the object.
4. **`__proto__` setter**: The `__proto__` setter modifies the prototype object linked to the object.
5. **`Object.getPrototypeOf()`**: The `Object.getPrototypeOf()` method returns the prototype object linked to the object.

> **Warning:** Modifying the `__proto__` property can have unintended consequences, such as breaking the prototype chain or causing performance issues.

## Code Examples
### Example 1: Basic usage of `__proto__` getter/setter
```javascript
// Create an object
const obj = {};

// Set the prototype of the object
obj.__proto__ = { foo: 'bar' };

// Get the prototype of the object
console.log(obj.__proto__); // Output: { foo: 'bar' }
```

### Example 2: Using `Object.getPrototypeOf()` to access the prototype chain
```javascript
// Create an object
const obj = {};

// Create a prototype object
const proto = { foo: 'bar' };

// Set the prototype of the object
obj.__proto__ = proto;

// Get the prototype of the object using Object.getPrototypeOf()
console.log(Object.getPrototypeOf(obj)); // Output: { foo: 'bar' }
```

### Example 3: Advanced usage of `__proto__` getter/setter and `Object.getPrototypeOf()` to implement inheritance
```javascript
// Create a parent object
const parent = {
  foo: 'bar',
  baz: function() {
    console.log('baz');
  }
};

// Create a child object
const child = {};

// Set the prototype of the child object to the parent object
child.__proto__ = parent;

// Get the prototype of the child object using Object.getPrototypeOf()
console.log(Object.getPrototypeOf(child)); // Output: { foo: 'bar', baz: [Function: baz] }

// Call the baz method on the child object
child.baz(); // Output: baz
```

## Visual Diagram
```mermaid
flowchart TD
    A[Object] -->|__proto__| B[Prototype]
    B -->|__proto__| C[Parent Prototype]
    C -->|__proto__| D[Grandparent Prototype]
    D -->|__proto__| E["Object.prototype"]
    E -->|__proto__| F[null]
    F -->|End of prototype chain|
```
The diagram illustrates the prototype chain of an object, showing how the `__proto__` property links each object to its prototype. The `Object.getPrototypeOf()` method can be used to traverse the prototype chain and access the prototype objects.

> **Note:** The prototype chain is a fundamental concept in JavaScript, and understanding how it works is essential for building efficient and scalable applications.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| `__proto__` getter/setter | O(1) | O(1) | Easy to use, fast access to prototype | Can break prototype chain, performance issues | Simple applications, prototyping |
| `Object.getPrototypeOf()` | O(1) | O(1) | Safe, efficient, and scalable | Slower than `__proto__` getter/setter | Large-scale applications, production code |
| Inheritance using constructors | O(n) | O(n) | Easy to implement, flexible | Can lead to tight coupling, performance issues | Small-scale applications, educational purposes |
| Inheritance using classes | O(n) | O(n) | Easy to implement, flexible | Can lead to tight coupling, performance issues | Small-scale applications, educational purposes |

> **Tip:** When choosing an approach, consider the trade-offs between time complexity, space complexity, and maintainability.

## Real-world Use Cases
1. **React**: React uses the `__proto__` getter to implement its virtual DOM, allowing for efficient rendering and updating of components.
2. **Angular**: Angular uses `Object.getPrototypeOf()` to create a prototype chain for its components, enabling inheritance and method overriding.
3. **Vue.js**: Vue.js uses a combination of `__proto__` getter/setter and `Object.getPrototypeOf()` to implement its reactivity system and component lifecycle.

## Common Pitfalls
1. **Modifying the `__proto__` property**: Modifying the `__proto__` property can break the prototype chain and cause performance issues.
```javascript
// Wrong way
const obj = {};
obj.__proto__ = null; // Breaks the prototype chain

// Right way
const obj = {};
Object.setPrototypeOf(obj, null); // Safely sets the prototype to null
```

2. **Using `__proto__` getter/setter in performance-critical code**: Using `__proto__` getter/setter in performance-critical code can lead to performance issues.
```javascript
// Wrong way
for (let i = 0; i < 100000; i++) {
  const obj = {};
  obj.__proto__ = { foo: 'bar' }; // Slow and inefficient
}

// Right way
const proto = { foo: 'bar' };
for (let i = 0; i < 100000; i++) {
  const obj = Object.create(proto); // Fast and efficient
}
```

3. **Not understanding the prototype chain**: Not understanding the prototype chain can lead to confusion and bugs.
```javascript
// Wrong way
const parent = { foo: 'bar' };
const child = {};
child.__proto__ = parent;
console.log(child.foo); // Output: 'bar' (but why?)

// Right way
const parent = { foo: 'bar' };
const child = Object.create(parent);
console.log(child.foo); // Output: 'bar' (because of the prototype chain)
```

4. **Using `Object.getPrototypeOf()` in a loop**: Using `Object.getPrototypeOf()` in a loop can lead to performance issues.
```javascript
// Wrong way
for (let i = 0; i < 100000; i++) {
  const obj = {};
  Object.getPrototypeOf(obj); // Slow and inefficient
}

// Right way
const obj = {};
const proto = Object.getPrototypeOf(obj); // Fast and efficient
for (let i = 0; i < 100000; i++) {
  // Use the cached proto reference
}
```

## Interview Tips
1. **What is the difference between `__proto__` getter/setter and `Object.getPrototypeOf()`?**
	* Weak answer: "They are the same thing."
	* Strong answer: "The `__proto__` getter/setter is a property that allows developers to access and modify the prototype of an object, while `Object.getPrototypeOf()` is a method that returns the prototype of an object. The `__proto__` getter/setter is faster but can break the prototype chain, while `Object.getPrototypeOf()` is safer but slower."
2. **How do you implement inheritance in JavaScript?**
	* Weak answer: "I use the `__proto__` getter/setter to set the prototype of an object."
	* Strong answer: "I use a combination of `Object.create()` and `Object.getPrototypeOf()` to implement inheritance. I create a new object with a prototype that is linked to the parent object, and then use `Object.getPrototypeOf()` to access the prototype chain."
3. **What is the prototype chain, and how does it work?**
	* Weak answer: "The prototype chain is a sequence of objects that are linked together."
	* Strong answer: "The prototype chain is a sequence of objects that are linked together through their `__proto__` properties. Each object in the chain has a reference to its prototype, which allows for method overriding and inheritance. The prototype chain is a fundamental concept in JavaScript, and understanding how it works is essential for building efficient and scalable applications."

## Key Takeaways
* The `__proto__` getter/setter and `Object.getPrototypeOf()` are two fundamental concepts in JavaScript that allow developers to access and manipulate the prototype chain of an object.
* The `__proto__` getter/setter is faster but can break the prototype chain, while `Object.getPrototypeOf()` is safer but slower.
* Inheritance is a crucial concept in JavaScript, and understanding how to implement it using `Object.create()` and `Object.getPrototypeOf()` is essential.
* The prototype chain is a sequence of objects that are linked together through their `__proto__` properties, allowing for method overriding and inheritance.
* Modifying the `__proto__` property can have unintended consequences, such as breaking the prototype chain or causing performance issues.
* Using `__proto__` getter/setter in performance-critical code can lead to performance issues.
* Not understanding the prototype chain can lead to confusion and bugs.
* Using `Object.getPrototypeOf()` in a loop can lead to performance issues.
* Implementing inheritance using constructors or classes can lead to tight coupling and performance issues.