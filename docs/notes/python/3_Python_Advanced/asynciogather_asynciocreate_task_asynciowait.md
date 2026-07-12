---
title: "asyncio.gather(), asyncio.create_task(), asyncio.wait()"
topic: "asyncio.gather(), asyncio.create_task(), asyncio.wait()"
section: "python"
tags: "python, asyncio.gather(),-asyncio.create_task(),-asyncio.wait(), programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/python%20asyncio.gather(),%20asyncio.create_task(),%20asyncio.wait()%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![asyncio](https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Asyncio_logo.svg/1024px-Asyncio_logo.svg.png)

## Introduction
**Asyncio** is a library in Python that allows for asynchronous programming, which enables writing single-threaded code that can handle multiple tasks concurrently. This is particularly useful for I/O-bound tasks, such as network requests or database queries, where the majority of the time is spent waiting for the operation to complete. **asyncio.gather()**, **asyncio.create_task()**, and **asyncio.wait()** are three essential functions in asyncio that help manage and coordinate these tasks.

In real-world scenarios, asyncio is used in production systems to handle a large number of concurrent connections, such as in web servers, chat applications, or data processing pipelines. For example, companies like Instagram and Pinterest use asyncio to handle their high-traffic APIs.

> **Note:** Asyncio is not a replacement for multiprocessing or multithreading, but rather a tool to write efficient single-threaded code that can handle multiple tasks concurrently.

## Core Concepts
- **Coroutines:** A coroutine is a function that can suspend and resume its execution at specific points, allowing other coroutines to run in the meantime. In asyncio, coroutines are defined using the `async def` syntax.
- **Event Loop:** The event loop is the core of asyncio, responsible for scheduling and running coroutines. It manages the execution of tasks and handles I/O operations.
- **Tasks:** A task is a coroutine that is scheduled to run in the event loop. Tasks can be created using **asyncio.create_task()** or **asyncio.gather()**.
- **Futures:** A future is an object that represents the result of a task. It can be used to wait for the completion of a task and retrieve its result.

## How It Works Internally
When a coroutine is defined using `async def`, it is not executed immediately. Instead, it is scheduled to run in the event loop using **asyncio.create_task()** or **asyncio.gather()**. The event loop is responsible for running the coroutine and handling any I/O operations.

Here's a step-by-step breakdown of how **asyncio.gather()**, **asyncio.create_task()**, and **asyncio.wait()** work internally:

1. **asyncio.create_task()**: When a coroutine is passed to **asyncio.create_task()**, it is scheduled to run in the event loop. The event loop will execute the coroutine and manage any I/O operations.
2. **asyncio.gather()**: When multiple coroutines are passed to **asyncio.gather()**, they are scheduled to run in the event loop concurrently. The event loop will execute each coroutine and manage any I/O operations.
3. **asyncio.wait()**: When a list of futures is passed to **asyncio.wait()**, it will wait for the completion of all the tasks represented by the futures. The event loop will continue to run and manage any I/O operations while waiting for the tasks to complete.

> **Warning:** If a task is not awaited, it will not be executed. This can lead to unexpected behavior or errors.

## Code Examples
### Example 1: Basic Usage of **asyncio.create_task()**
```python
import asyncio

async def my_coroutine():
    await asyncio.sleep(1)
    print("Coroutine completed")

async def main():
    task = asyncio.create_task(my_coroutine())
    await task

asyncio.run(main())
```
### Example 2: Using **asyncio.gather()** to Run Multiple Coroutines
```python
import asyncio

async def my_coroutine1():
    await asyncio.sleep(1)
    print("Coroutine 1 completed")
    return 1

async def my_coroutine2():
    await asyncio.sleep(2)
    print("Coroutine 2 completed")
    return 2

async def main():
    results = await asyncio.gather(my_coroutine1(), my_coroutine2())
    print(results)

asyncio.run(main())
```
### Example 3: Using **asyncio.wait()** to Wait for Multiple Tasks
```python
import asyncio

async def my_coroutine1():
    await asyncio.sleep(1)
    print("Coroutine 1 completed")
    return 1

async def my_coroutine2():
    await asyncio.sleep(2)
    print("Coroutine 2 completed")
    return 2

async def main():
    task1 = asyncio.create_task(my_coroutine1())
    task2 = asyncio.create_task(my_coroutine2())
    done, pending = await asyncio.wait({task1, task2})
    print([task.result() for task in done])

asyncio.run(main())
```
> **Tip:** Use **asyncio.gather()** to run multiple coroutines concurrently and wait for all of them to complete.

## Visual Diagram
```mermaid
flowchart TD
    A[Event Loop] -->|create_task()| B[Task 1]
    A -->|create_task()| C[Task 2]
    B -->|await| D[Future 1]
    C -->|await| E[Future 2]
    A -->|wait()| F[Wait for Tasks]
    F -->|done| G[Done Tasks]
    F -->|pending| H[Pending Tasks]
    G -->|result()| I[Task Results]
    H -->|await| J[Wait for Pending Tasks]
    J -->|done| G
```
The diagram shows the event loop creating tasks using **asyncio.create_task()** and waiting for their completion using **asyncio.wait()**. The tasks are represented by futures, which can be awaited to retrieve their results.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
|----------|----------------|-----------------|------|------|----------|
| **asyncio.create_task()** | O(1) | O(1) | Easy to use, flexible | Limited control over task execution | Simple, concurrent tasks |
| **asyncio.gather()** | O(n) | O(n) | Easy to use, concurrent execution | Limited control over task execution | Multiple, concurrent tasks |
| **asyncio.wait()** | O(n) | O(n) | Flexible, allows waiting for tasks | More complex to use | Waiting for multiple tasks |

> **Interview:** When would you use **asyncio.create_task()** versus **asyncio.gather()**?

## Real-world Use Cases
1. **Instagram:** Instagram uses asyncio to handle their high-traffic APIs, which require concurrent execution of multiple tasks.
2. **Pinterest:** Pinterest uses asyncio to handle their data processing pipeline, which involves concurrent execution of multiple tasks.
3. **Redis:** Redis uses asyncio to handle their high-performance, concurrent database queries.

## Common Pitfalls
1. **Not awaiting tasks:** If a task is not awaited, it will not be executed. This can lead to unexpected behavior or errors.
```python
# Wrong
async def my_coroutine():
    await asyncio.sleep(1)
    print("Coroutine completed")

async def main():
    asyncio.create_task(my_coroutine())

# Right
async def main():
    task = asyncio.create_task(my_coroutine())
    await task
```
2. **Not handling exceptions:** If an exception occurs in a task, it will not be propagated to the caller. This can lead to unexpected behavior or errors.
```python
# Wrong
async def my_coroutine():
    await asyncio.sleep(1)
    raise Exception("Error")

async def main():
    task = asyncio.create_task(my_coroutine())

# Right
async def main():
    task = asyncio.create_task(my_coroutine())
    try:
        await task
    except Exception as e:
        print(f"Error: {e}")
```
> **Warning:** Always await tasks and handle exceptions to ensure proper execution and error handling.

## Interview Tips
1. **What is the difference between **asyncio.create_task()** and **asyncio.gather()****?**
	* Weak answer: "They are both used to create tasks."
	* Strong answer: "**asyncio.create_task()** creates a single task, while **asyncio.gather()** creates multiple tasks and waits for their completion."
2. **How do you handle exceptions in asyncio tasks?**
	* Weak answer: "You can't handle exceptions in asyncio tasks."
	* Strong answer: "You can handle exceptions in asyncio tasks by using try-except blocks and awaiting the tasks."
3. **What is the purpose of the event loop in asyncio?**
	* Weak answer: "The event loop is used to create tasks."
	* Strong answer: "The event loop is the core of asyncio, responsible for scheduling and running tasks, as well as handling I/O operations."

## Key Takeaways
* **asyncio.create_task()** creates a single task, while **asyncio.gather()** creates multiple tasks and waits for their completion.
* **asyncio.wait()** allows waiting for multiple tasks and returns the results.
* Always await tasks and handle exceptions to ensure proper execution and error handling.
* The event loop is the core of asyncio, responsible for scheduling and running tasks, as well as handling I/O operations.
* Use **asyncio.gather()** to run multiple coroutines concurrently and wait for all of them to complete.
* Use **asyncio.wait()** to wait for multiple tasks and retrieve their results.
* The time complexity of **asyncio.create_task()** is O(1), while the time complexity of **asyncio.gather()** and **asyncio.wait()** is O(n).
* The space complexity of **asyncio.create_task()** is O(1), while the space complexity of **asyncio.gather()** and **asyncio.wait()** is O(n).