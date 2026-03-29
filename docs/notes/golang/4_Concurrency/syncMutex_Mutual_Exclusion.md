---
title: "sync.Mutex: Mutual Exclusion"
topic: "sync.Mutex: Mutual Exclusion"
section: "golang"
tags: "golang, sync.mutex, programming, notes, interview"
banner: "https://picsum.photos/seed/40/1200/630"
update_count: 0
---

![sync.Mutex](https://golang.org/doc/gopher/frontpage.png)

## Introduction
The `sync.Mutex` is a fundamental data structure in Go that provides mutual exclusion, allowing only one goroutine to access a shared resource at a time. This is crucial in concurrent programming, where multiple goroutines may try to access the same resource simultaneously, leading to data corruption or other unexpected behavior. In this section, we will explore what `sync.Mutex` is, why it matters, and its real-world relevance.

In Go, `sync.Mutex` is part of the `sync` package, which provides basic synchronization primitives. The `Mutex` type is a mutual exclusion lock that can be used to protect shared resources from concurrent access. It provides two main methods: `Lock()` and `Unlock()`, which are used to acquire and release the lock, respectively.

> **Note:** The `sync.Mutex` type is not reentrant, meaning that a goroutine cannot acquire the same lock multiple times. If a goroutine tries to acquire a lock that it already holds, the program will deadlock.

## Core Concepts
In this section, we will cover the core concepts related to `sync.Mutex`, including its definition, mental models, and key terminology.

* **Mutual Exclusion**: Mutual exclusion is a concept in concurrent programming that ensures only one goroutine can access a shared resource at a time. This is achieved using locks, which prevent other goroutines from accessing the resource while it is being used by another goroutine.
* **Lock**: A lock is a synchronization primitive that allows only one goroutine to access a shared resource at a time. In Go, the `sync.Mutex` type provides a lock that can be used to protect shared resources.
* **Critical Section**: A critical section is a block of code that accesses shared resources and requires mutual exclusion to ensure data integrity.

> **Tip:** When using `sync.Mutex`, it is essential to ensure that the lock is always released after acquiring it, even in the presence of errors. This can be achieved using a `defer` statement to release the lock.

## How It Works Internally
In this section, we will explore the internal mechanics of `sync.Mutex` and how it works under the hood.

The `sync.Mutex` type uses a combination of atomic operations and a wait queue to implement mutual exclusion. When a goroutine calls `Lock()`, it checks if the lock is available. If it is, the goroutine acquires the lock and continues execution. If the lock is not available, the goroutine is added to a wait queue and suspended until the lock is released.

When a goroutine calls `Unlock()`, it releases the lock and notifies the next goroutine in the wait queue to acquire the lock.

> **Warning:** If a goroutine panics while holding a lock, the lock will not be released, leading to a deadlock. It is essential to ensure that locks are always released, even in the presence of errors.

## Code Examples
In this section, we will explore three complete and runnable examples of using `sync.Mutex` in Go.

### Example 1: Basic Usage
```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	var mu sync.Mutex
	var count int

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			mu.Lock()
			count++
			mu.Unlock()
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println(count)
}
```
This example demonstrates the basic usage of `sync.Mutex` to protect a shared resource from concurrent access.

### Example 2: Real-World Pattern
```go
package main

import (
	"fmt"
	"sync"
)

type BankAccount struct {
	balance float64
	mu      sync.Mutex
}

func (a *BankAccount) Deposit(amount float64) {
	a.mu.Lock()
	a.balance += amount
	a.mu.Unlock()
}

func (a *BankAccount) Withdraw(amount float64) {
	a.mu.Lock()
	if a.balance >= amount {
		a.balance -= amount
	}
	a.mu.Unlock()
}

func main() {
	account := &BankAccount{}
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			account.Deposit(100)
			account.Withdraw(50)
			wg.Done()
		}()
	}
	wg.Wait()
	fmt.Println(account.balance)
}
```
This example demonstrates a real-world pattern of using `sync.Mutex` to protect a shared resource, in this case, a bank account.

### Example 3: Advanced Usage
```go
package main

import (
	"fmt"
	"sync"
	"time"
)

type Cache struct {
	data map[string]string
	mu   sync.Mutex
}

func (c *Cache) Get(key string) string {
	c.mu.Lock()
	value := c.data[key]
	c.mu.Unlock()
	return value
}

func (c *Cache) Set(key string, value string) {
	c.mu.Lock()
	c.data[key] = value
	c.mu.Unlock()
}

func main() {
	cache := &Cache{data: make(map[string]string)}
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(key string, value string) {
			cache.Set(key, value)
			time.Sleep(100 * time.Millisecond)
			fmt.Println(cache.Get(key))
			wg.Done()
		}(fmt.Sprintf("key-%d", i), fmt.Sprintf("value-%d", i))
	}
	wg.Wait()
}
```
This example demonstrates an advanced usage of `sync.Mutex` to protect a shared cache from concurrent access.

## Visual Diagram
```mermaid
graph LR
    A[Goroutine 1] -->|Lock()|> B[Mutex]
    B -->|Acquire Lock|> C[Goroutine 1 Executes]
    C -->|Unlock()|> D[Mutex]
    D -->|Release Lock|> E[Goroutine 2]
    E -->|Lock()|> B
    B -->|Acquire Lock|> F[Goroutine 2 Executes]
    F -->|Unlock()|> D
    style B fill:#f9f,stroke:#333,stroke-width:4px
```
This diagram illustrates the basic flow of acquiring and releasing a lock using `sync.Mutex`.

> **Interview:** Can you explain the difference between `sync.Mutex` and `sync.RWMutex`?

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| `sync.Mutex` | O(1) | O(1) | Simple to use, efficient | Not reentrant | Protecting shared resources from concurrent access |
| `sync.RWMutex` | O(1) | O(1) | Allows multiple readers, efficient | More complex to use | Protecting shared resources that require multiple readers |
| `sync.WaitGroup` | O(1) | O(1) | Simple to use, efficient | Not suitable for protecting shared resources | Waiting for multiple goroutines to complete |
| `sync.Cond` | O(1) | O(1) | Allows waiting for a condition | More complex to use | Waiting for a specific condition to occur |

## Real-world Use Cases
1. **Google's Go Runtime**: The Go runtime uses `sync.Mutex` to protect shared resources from concurrent access.
2. **Docker**: Docker uses `sync.Mutex` to protect shared resources, such as containers and images, from concurrent access.
3. **Kubernetes**: Kubernetes uses `sync.Mutex` to protect shared resources, such as pods and services, from concurrent access.

## Common Pitfalls
1. **Deadlock**: A deadlock occurs when two or more goroutines are blocked, waiting for each other to release a lock.
2. **Livelock**: A livelock occurs when two or more goroutines are constantly trying to acquire a lock, but are unable to do so.
3. **Starvation**: Starvation occurs when a goroutine is unable to acquire a lock, even though it is available.
4. **Priority Inversion**: Priority inversion occurs when a higher-priority goroutine is blocked, waiting for a lower-priority goroutine to release a lock.

> **Warning:** When using `sync.Mutex`, it is essential to ensure that locks are always released, even in the presence of errors.

## Interview Tips
1. **What is the difference between `sync.Mutex` and `sync.RWMutex`?**: `sync.Mutex` is a basic mutex that allows only one goroutine to access a shared resource, while `sync.RWMutex` allows multiple readers to access a shared resource.
2. **How do you avoid deadlocks when using `sync.Mutex`?**: To avoid deadlocks, ensure that locks are always released, even in the presence of errors, and avoid acquiring multiple locks in a specific order.
3. **What is the purpose of `sync.WaitGroup`?**: `sync.WaitGroup` is used to wait for multiple goroutines to complete.

## Key Takeaways
* `sync.Mutex` is a basic mutex that allows only one goroutine to access a shared resource.
* `sync.Mutex` is not reentrant, meaning that a goroutine cannot acquire the same lock multiple times.
* `sync.Mutex` is efficient, with a time complexity of O(1) and a space complexity of O(1).
* `sync.Mutex` is suitable for protecting shared resources from concurrent access.
* `sync.Mutex` can be used to avoid deadlocks, livelocks, starvation, and priority inversion.
* `sync.Mutex` is widely used in real-world applications, including Google's Go Runtime, Docker, and Kubernetes.
* `sync.Mutex` has a number of common pitfalls, including deadlocks, livelocks, starvation, and priority inversion.
* `sync.Mutex` is an essential data structure in concurrent programming, and every engineer should know how to use it effectively.