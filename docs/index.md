---
hide:
  - navigation
  - toc
---

# Daily Notes

A self-updating knowledge base for software engineers — covering DSA, React, React Native, Java, and more.

Content is generated and updated automatically via GitHub Actions using Groq's Llama-3 70B model.

---

## Topics

<div class="grid cards" markdown>

-   :material-code-braces: **React**

    ---

    Fundamentals, hooks, advanced patterns, performance, and ecosystem.

    [:octicons-arrow-right-24: Browse React notes](notes/react/index.md)

-   :material-cellphone: **React Native**

    ---

    Mobile development, navigation, device APIs, and deployment.

    [:octicons-arrow-right-24: Browse React Native notes](notes/react-native/index.md)

-   :material-coffee: **Java**

    ---

    Core Java, collections, concurrency, Spring Boot, and JVM internals.

    [:octicons-arrow-right-24: Browse Java notes](notes/java/index.md)

-   :material-database: **DSA**

    ---

    LeetCode solutions (Easy / Medium / Hard) with Java implementations and complexity analysis.

    [:octicons-arrow-right-24: Browse DSA problems](dsa/index.md)

</div>

---

## How it works

1. GitHub Actions runs twice daily (3am and 3pm UTC)
2. Picks a random topic from `topics.json`
3. Generates rich Markdown content using Groq's Llama-3 70B model
4. Commits the new article and deploys to GitHub Pages automatically
5. Existing articles get updated up to 5 times with new sections and examples
