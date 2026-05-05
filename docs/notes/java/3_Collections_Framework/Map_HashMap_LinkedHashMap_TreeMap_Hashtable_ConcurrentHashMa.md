---
title: "Map: HashMap, LinkedHashMap, TreeMap, Hashtable, ConcurrentHashMap"
topic: "Map: HashMap, LinkedHashMap, TreeMap, Hashtable, ConcurrentHashMap"
section: "java"
tags: "java, map, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/java%20Map%20HashMap,%20LinkedHashMap,%20TreeMap,%20Hashtable,%20ConcurrentHashMap%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![Map](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Java_collections_framework.svg/1200px-Java_collections_framework.svg.png)

## Introduction
The **Map** interface in Java is a fundamental data structure that stores key-value pairs, allowing for efficient lookup, insertion, and deletion of elements. It is a crucial component of the Java Collections Framework and is widely used in various applications, including web development, data processing, and caching. In this study note, we will delve into the world of Maps, exploring their core concepts, internal workings, and practical applications.

> **Note:** The Map interface is not to be confused with the **List** interface, which stores a collection of elements without keys.

## Core Concepts
A **Map** is a data structure that associates each key with a value, allowing for fast retrieval of values by their corresponding keys. The key concepts in a Map are:

* **Key**: a unique identifier for a value
* **Value**: the data associated with a key
* **Entry**: a key-value pair
* **Map**: the collection of key-value pairs

The most common implementations of the Map interface in Java are:

* **HashMap**: a hash-based implementation that provides fast lookup, insertion, and deletion operations
* **LinkedHashMap**: a hash-based implementation that preserves the order of insertion
* **TreeMap**: a tree-based implementation that provides sorted keys
* **Hashtable**: a legacy hash-based implementation that is synchronized
* **ConcurrentHashMap**: a thread-safe hash-based implementation

## How It Works Internally
The internal workings of a Map depend on its implementation. Here is a step-by-step breakdown of how a **HashMap** works:

1. **Hashing**: when a key is inserted, its hash code is calculated using the `hashCode()` method
2. **Indexing**: the hash code is used to determine the index of the key in the underlying array
3. **Collision resolution**: if two keys have the same hash code, a collision occurs, and the Map uses a technique such as chaining or open addressing to resolve the collision
4. **Entry creation**: a new entry is created with the key and value, and it is added to the Map

The time complexity of **HashMap** operations is:

* **get**: O(1) on average, O(n) in the worst case
* **put**: O(1) on average, O(n) in the worst case
* **remove**: O(1) on average, O(n) in the worst case

> **Warning:** The **HashMap** implementation is not thread-safe, and concurrent modifications can lead to unpredictable behavior.

## Code Examples
### Example 1: Basic Usage
```java
import java.util.HashMap;
import java.util.Map;

public class HashMapExample {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        map.put("John", 25);
        map.put("Jane", 30);
        System.out.println(map.get("John")); // prints 25
        System.out.println(map.containsKey("Jane")); // prints true
    }
}
```

### Example 2: Real-world Pattern
```java
import java.util.HashMap;
import java.util.Map;

public class CacheExample {
    private Map<String, String> cache = new HashMap<>();

    public String get(String key) {
        return cache.get(key);
    }

    public void put(String key, String value) {
        cache.put(key, value);
    }

    public static void main(String[] args) {
        CacheExample cache = new CacheExample();
        cache.put("user", "John");
        System.out.println(cache.get("user")); // prints John
    }
}
```

### Example 3: Advanced Usage
```java
import java.util.HashMap;
import java.util.Map;

public class AdvancedHashMapExample {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        map.put("John", 25);
        map.put("Jane", 30);
        map.computeIfAbsent("Bob", k -> 35);
        System.out.println(map.get("Bob")); // prints 35
        map.computeIfPresent("John", (k, v) -> v + 5);
        System.out.println(map.get("John")); // prints 30
    }
}
```

## Visual Diagram
```mermaid
flowchart TD
    A[Key] -->|hashCode()| B[Hash Code]
    B -->|Indexing| C[Index]
    C -->|Collision Resolution| D[Entry]
    D -->|Add to Map| E[Map]
    E -->|get()| F[Value]
    F -->|put()| E
    E -->|remove()| G[Map]
    G -->|isEmpty()| H[Boolean]
    H -->|containsKey()| I[Boolean]
    I -->|containsValue()| J[Boolean]
    J -->|size()| K[Integer]
    K -->|clear()| L[Map]
    L -->|entrySet()| M[Set]
    M -->|keySet()| N[Set]
    N -->|values()| O[Collection]
```
The diagram illustrates the internal workings of a **HashMap**, including hashing, indexing, collision resolution, and entry creation.

## Comparison
| Implementation | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| **HashMap** | O(1) average, O(n) worst case | O(n) | Fast lookup, insertion, and deletion | Not thread-safe, collision resolution | General-purpose caching, data storage |
| **LinkedHashMap** | O(1) average, O(n) worst case | O(n) | Preserves order of insertion | Slower than **HashMap** | Ordered caching, data storage |
| **TreeMap** | O(log n) | O(n) | Sorted keys, fast range queries | Slower than **HashMap** | Sorted data storage, range queries |
| **Hashtable** | O(1) average, O(n) worst case | O(n) | Synchronized, thread-safe | Legacy implementation, slower than **HashMap** | Legacy code, thread-safe caching |
| **ConcurrentHashMap** | O(1) average, O(n) worst case | O(n) | Thread-safe, fast lookup, insertion, and deletion | More complex than **HashMap** | High-performance, thread-safe caching |

## Real-world Use Cases
1. **Google's Cache**: Google uses a **ConcurrentHashMap**-based cache to store frequently accessed data, reducing the load on their database and improving page load times.
2. **Amazon's Dynamo**: Amazon's Dynamo database uses a **HashMap**-based caching layer to improve performance and reduce latency.
3. **Facebook's Memcached**: Facebook uses a **HashMap**-based caching layer, Memcached, to store frequently accessed data and reduce the load on their database.

> **Tip:** Use a **ConcurrentHashMap** when you need a thread-safe cache, and use a **HashMap** when you need a fast, non-thread-safe cache.

## Common Pitfalls
1. **Not synchronizing access**: failing to synchronize access to a **HashMap** can lead to unpredictable behavior and data corruption.
2. **Using a **Hashtable****: using a **Hashtable** can lead to slower performance and legacy code maintenance issues.
3. **Not handling collisions**: failing to handle collisions can lead to data loss and performance issues.
4. **Not using **computeIfAbsent****: failing to use **computeIfAbsent** can lead to unnecessary computations and performance issues.

## Interview Tips
1. **What is the difference between a **HashMap** and a **ConcurrentHashMap****?**: a **ConcurrentHashMap** is thread-safe, while a **HashMap** is not.
2. **How do you handle collisions in a **HashMap****?**: use a technique such as chaining or open addressing to resolve collisions.
3. **What is the time complexity of **get** and **put** operations in a **HashMap****?**: O(1) average, O(n) worst case.

> **Interview:** Be prepared to explain the internal workings of a **HashMap**, including hashing, indexing, and collision resolution.

## Key Takeaways
* **HashMap** is a fast, non-thread-safe cache implementation.
* **ConcurrentHashMap** is a thread-safe cache implementation.
* **LinkedHashMap** preserves the order of insertion.
* **TreeMap** provides sorted keys and fast range queries.
* **Hashtable** is a legacy implementation that is synchronized but slower than **HashMap**.
* Use **computeIfAbsent** to avoid unnecessary computations.
* Handle collisions using techniques such as chaining or open addressing.
* Use a **ConcurrentHashMap** when you need a thread-safe cache, and use a **HashMap** when you need a fast, non-thread-safe cache.