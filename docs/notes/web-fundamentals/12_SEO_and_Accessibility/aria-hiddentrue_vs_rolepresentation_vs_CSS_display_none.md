---
title: "aria-hidden="true" vs role="presentation" vs CSS display: none"
topic: "aria-hidden="true" vs role="presentation" vs CSS display: none"
section: "web-fundamentals"
tags: "web-fundamentals, aria-hidden="true"-vs-role="presentation"-vs-css-display, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/web-fundamentals%20aria-hidden="true"%20vs%20role="presentation"%20vs%20CSS%20display%20none%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![aria-hidden](https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/W3C_ARIA_Logo.svg/1200px-W3C_ARIA_Logo.svg.png)

## Introduction
**Accessibility** is a crucial aspect of web development, ensuring that websites and applications are usable by everyone, including people with disabilities. One important concept in accessibility is **hiding content** from screen readers and other assistive technologies while still allowing it to be visible to sighted users. In this section, we will explore three different methods for hiding content: `aria-hidden="true"`, `role="presentation"`, and `CSS display: none`. We will delve into the differences between these methods, their use cases, and best practices for implementation. > **Note:** Understanding the nuances of these methods is essential for creating accessible and usable web applications.

## Core Concepts
- **ARIA (Accessible Rich Internet Applications)**: a set of attributes that define ways to make dynamic web content and interactive elements more accessible to people with disabilities.
- **`aria-hidden="true"`**: an ARIA attribute that indicates an element is not visible or is not interactive, but still present in the DOM.
- **`role="presentation"`**: an ARIA attribute that indicates an element has no semantic meaning and should be ignored by screen readers.
- **`CSS display: none`**: a CSS property that hides an element from both screen readers and sighted users.
> **Tip:** When deciding which method to use, consider the purpose of the content and whether it needs to be accessible to screen readers.

## How It Works Internally
When an element is marked with `aria-hidden="true"`, screen readers will skip over it, but it will still be present in the DOM and visible to sighted users. On the other hand, `role="presentation"` removes the semantic meaning of an element, making it equivalent to a `div` or `span` element. `CSS display: none` completely removes an element from the rendering tree, making it invisible to both screen readers and sighted users. > **Warning:** Using `CSS display: none` can have unintended consequences, such as breaking layout or causing accessibility issues.

## Code Examples
### Example 1: Basic `aria-hidden="true"` usage
```html
<!-- Hide a paragraph from screen readers, but keep it visible to sighted users -->
<p aria-hidden="true">This paragraph is hidden from screen readers.</p>
```
### Example 2: Using `role="presentation"` for a table
```html
<!-- Remove semantic meaning from a table, making it equivalent to a div -->
<table role="presentation">
  <tr>
    <td>Cell 1</td>
    <td>Cell 2</td>
  </tr>
</table>
```
### Example 3: Advanced usage with `CSS display: none` and JavaScript
```javascript
// Hide an element using CSS display: none, and then show it when a button is clicked
const button = document.getElementById('button');
const element = document.getElementById('element');

button.addEventListener('click', () => {
  element.style.display = 'block';
});

// Initial state: hide the element
element.style.display = 'none';
```
> **Interview:** A common interview question is to ask how you would hide content from screen readers while still keeping it visible to sighted users. A strong answer would include a discussion of `aria-hidden="true"` and `role="presentation"`.

## Visual Diagram
```mermaid
graph TD
    A[Element] -->|aria-hidden="true"| B["Screen Reader: Skip"]
    A -->|role="presentation"| C["Screen Reader: Ignore"]
    A -->|CSS display: none| D["Rendering Tree: Remove"]
    B --> E[Element remains in DOM]
    C --> F[Element has no semantic meaning]
    D --> G[Element is invisible to all]
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#f9f,stroke:#333,stroke-width:4px
    style C fill:#f9f,stroke:#333,stroke-width:4px
    style D fill:#f9f,stroke:#333,stroke-width:4px
```
The diagram illustrates the different methods for hiding content and their effects on screen readers and the rendering tree. > **Note:** The `aria-hidden="true"` and `role="presentation"` methods have different use cases and should be used accordingly.

## Comparison
| Method | Effect on Screen Readers | Effect on Sighted Users | Use Case |
| --- | --- | --- | --- |
| `aria-hidden="true"` | Skip over element | Element remains visible | Hide decorative elements or dynamic content |
| `role="presentation"` | Ignore element | Element remains visible | Remove semantic meaning from elements |
| `CSS display: none` | Element is invisible | Element is invisible | Completely hide an element from all users |
| `visibility: hidden` | Element is invisible | Element takes up space | Hide an element while preserving its layout |
| `opacity: 0` | Element is invisible | Element takes up space | Hide an element while preserving its layout and interactions |

## Real-world Use Cases
- **Google**: uses `aria-hidden="true"` to hide decorative elements in their search results page.
- **Facebook**: uses `role="presentation"` to remove semantic meaning from certain elements in their news feed.
- **Amazon**: uses `CSS display: none` to hide elements that are not relevant to the current user's interaction.

## Common Pitfalls
- **Using `CSS display: none` unnecessarily**: can break layout or cause accessibility issues.
- **Forgetting to add `aria-hidden="true"`**: can cause screen readers to read unnecessary content.
- **Misusing `role="presentation"`**: can remove important semantic meaning from elements.
- **Not testing for accessibility**: can lead to unnoticed accessibility issues.

## Interview Tips
- **What is the difference between `aria-hidden="true"` and `role="presentation"`?**: A strong answer would include a discussion of the different use cases and effects on screen readers.
- **How would you hide an element from screen readers while still keeping it visible to sighted users?**: A strong answer would include a discussion of `aria-hidden="true"` and `role="presentation"`.
- **What are some common pitfalls when using accessibility attributes?**: A strong answer would include a discussion of the importance of testing for accessibility and avoiding unnecessary use of `CSS display: none`.

## Key Takeaways
* `aria-hidden="true"` hides an element from screen readers, but keeps it visible to sighted users.
* `role="presentation"` removes semantic meaning from an element, making it equivalent to a `div` or `span` element.
* `CSS display: none` completely removes an element from the rendering tree, making it invisible to both screen readers and sighted users.
* Use `aria-hidden="true"` for decorative elements or dynamic content.
* Use `role="presentation"` to remove semantic meaning from elements.
* Use `CSS display: none` to completely hide an element from all users.
* Always test for accessibility and avoid unnecessary use of `CSS display: none`.
* Use `visibility: hidden` or `opacity: 0` to hide an element while preserving its layout and interactions.