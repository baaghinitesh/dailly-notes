---
title: "New Architecture: JSI, Fabric Renderer, TurboModules — No More Bridge"
topic: "New Architecture: JSI, Fabric Renderer, TurboModules — No More Bridge"
section: "react-native"
tags: "react-native, new-architecture, programming, notes, interview"
banner: "https://picsum.photos/seed/24/1200/630"
update_count: 0
---

![react-native](https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg)

## Introduction
React Native is a popular framework for building cross-platform mobile applications. However, its traditional architecture has been criticized for its limitations, particularly with regards to performance and complexity. To address these issues, Facebook has introduced a new architecture for React Native, which includes JSI, Fabric Renderer, and TurboModules. This new architecture aims to improve performance, simplify the codebase, and provide a more seamless user experience. In this article, we will delve into the details of this new architecture, exploring its core concepts, internal mechanics, and real-world applications.

## Core Concepts
The new React Native architecture is built around three main components: JSI (JavaScript Interface), Fabric Renderer, and TurboModules.
- **JSI (JavaScript Interface)**: JSI is a lightweight, low-overhead interface between JavaScript and native code. It allows for direct communication between the two, eliminating the need for a bridge.
- **Fabric Renderer**: Fabric Renderer is a new rendering engine that replaces the traditional React Native renderer. It provides a more efficient and flexible way of rendering components, allowing for better performance and customization.
- **TurboModules**: TurboModules are a new way of building and managing native modules in React Native. They provide a more streamlined and efficient way of interacting with native code, making it easier to build and maintain complex applications.

## How It Works Internally
The new architecture works as follows:
1. **JSI Initialization**: When the application starts, JSI is initialized, establishing a direct connection between JavaScript and native code.
2. **Fabric Renderer Initialization**: The Fabric Renderer is initialized, setting up the rendering engine and preparing it for use.
3. **TurboModules Registration**: TurboModules are registered, making them available for use in the application.
4. **Component Rendering**: When a component is rendered, the Fabric Renderer takes over, using JSI to communicate with native code and TurboModules to interact with native modules.
5. **Native Code Execution**: Native code is executed, using JSI to communicate with JavaScript and TurboModules to interact with the application.

> **Note:** The new architecture is designed to be more efficient and flexible than the traditional React Native architecture. By eliminating the bridge and introducing a more direct communication mechanism, it provides a better user experience and improves performance.

## Code Examples
### Example 1: Basic JSI Usage
```javascript
// Import the JSI module
import { JSI } from 'react-native';

// Create a new JSI instance
const jsi = new JSI();

// Use JSI to call a native function
jsi.callNative('myNativeFunction', 'Hello, World!');
```

### Example 2: Fabric Renderer Usage
```javascript
// Import the Fabric Renderer module
import { FabricRenderer } from 'react-native';

// Create a new Fabric Renderer instance
const renderer = new FabricRenderer();

// Use the Fabric Renderer to render a component
renderer.render(<MyComponent />);
```

### Example 3: TurboModules Usage
```javascript
// Import the TurboModules module
import { TurboModules } from 'react-native';

// Create a new TurboModules instance
const turboModules = new TurboModules();

// Register a new TurboModule
turboModules.register('myTurboModule', () => {
  // Implement the TurboModule logic here
});
```

## Visual Diagram
```mermaid
graph LR
    A[JSI Initialization] --> B[Fabric Renderer Initialization]
    B --> C[TurboModules Registration]
    C --> D[Component Rendering]
    D --> E[Native Code Execution]
    E --> F[JSI Communication]
    F --> G[TurboModules Interaction]
    G --> H[Application Logic]
    H --> I[User Interaction]
    I --> J[Component Updates]
    J --> K[Rendering Engine]
    K --> L[Native Code Updates]
    L --> M[JSI Updates]
    M --> N[Fabric Renderer Updates]
    N --> O[TurboModules Updates]
    O --> P[Application Updates]
```
The diagram illustrates the flow of the new architecture, from JSI initialization to TurboModules interaction.

> **Tip:** The new architecture is designed to be more modular and flexible than the traditional React Native architecture. By breaking down the components into smaller, more manageable pieces, it provides a better foundation for building complex applications.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Traditional React Native | O(n) | O(n) | Easy to use, well-documented | Performance issues, complex codebase | Simple applications |
| New React Native Architecture | O(log n) | O(log n) | Better performance, more flexible | Steeper learning curve, more complex | Complex applications |
| Flutter | O(n) | O(n) | Fast development, hot reload | Limited native integration, steep learning curve | Cross-platform applications |
| NativeScript | O(n) | O(n) | Native performance, easy to use | Limited platform support, complex codebase | Native applications |

## Real-world Use Cases
1. **Facebook**: Facebook uses the new React Native architecture to power its mobile applications, providing a seamless user experience and improved performance.
2. **Instagram**: Instagram uses the new React Native architecture to build its mobile applications, taking advantage of the improved performance and flexibility.
3. **Walmart**: Walmart uses the new React Native architecture to power its mobile applications, providing a better user experience and improving customer engagement.

> **Warning:** The new architecture is still evolving, and there may be compatibility issues with existing libraries and frameworks. Make sure to test thoroughly before deploying to production.

## Common Pitfalls
1. **Incorrect JSI Usage**: Using JSI incorrectly can lead to performance issues and crashes. Make sure to follow the documentation and examples carefully.
2. **Insufficient TurboModules Registration**: Failing to register TurboModules correctly can lead to errors and crashes. Make sure to register all required TurboModules.
3. **Inadequate Fabric Renderer Configuration**: Failing to configure the Fabric Renderer correctly can lead to performance issues and errors. Make sure to follow the documentation and examples carefully.
4. **Incompatible Library Versions**: Using incompatible library versions can lead to errors and crashes. Make sure to use the latest versions of all libraries and frameworks.

> **Interview:** When asked about the new React Native architecture, be sure to highlight its benefits, such as improved performance and flexibility. Also, be prepared to discuss potential pitfalls and how to avoid them.

## Interview Tips
1. **What is the new React Native architecture, and how does it improve performance?**: The new architecture uses JSI, Fabric Renderer, and TurboModules to provide a more direct and efficient communication mechanism between JavaScript and native code.
2. **How do you use JSI in a React Native application?**: JSI is used to call native functions and interact with native code. Make sure to follow the documentation and examples carefully.
3. **What are the benefits of using TurboModules in a React Native application?**: TurboModules provide a more streamlined and efficient way of interacting with native code, making it easier to build and maintain complex applications.

## Key Takeaways
* The new React Native architecture uses JSI, Fabric Renderer, and TurboModules to provide a more direct and efficient communication mechanism between JavaScript and native code.
* JSI is used to call native functions and interact with native code.
* TurboModules provide a more streamlined and efficient way of interacting with native code.
* The new architecture is designed to be more modular and flexible than the traditional React Native architecture.
* The new architecture provides better performance and a more seamless user experience.
* The new architecture is still evolving, and there may be compatibility issues with existing libraries and frameworks.
* Make sure to follow the documentation and examples carefully to avoid common pitfalls.
* Use the latest versions of all libraries and frameworks to ensure compatibility.
* Test thoroughly before deploying to production to ensure a smooth user experience.