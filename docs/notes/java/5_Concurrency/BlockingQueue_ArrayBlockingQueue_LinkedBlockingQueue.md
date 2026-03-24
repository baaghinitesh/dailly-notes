---
title: "BlockingQueue: ArrayBlockingQueue, LinkedBlockingQueue"
topic: "BlockingQueue: ArrayBlockingQueue, LinkedBlockingQueue"
section: "java"
tags: "java, blockingqueue, programming, notes, interview"
banner: "https://picsum.photos/seed/676/1200/630"
update_count: 0
---

![BlockingQueue](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Java_Concurrency_Utilities.svg/1024px-Java_Concurrency_Utilities.svg.png)

## Introduction
A **BlockingQueue** is a type of queue in Java that follows the **FIFO (First-In-First-Out)** principle, meaning that the first element that is added to the queue will be the first one to be removed. It is a thread-safe implementation of a queue, which means it can be safely accessed and modified by multiple threads concurrently. The **BlockingQueue** interface is part of the Java Concurrency Utilities and provides a way to handle producer-consumer problems in a multithreaded environment. In real-world scenarios, **BlockingQueue** is used in job scheduling, message passing, and data processing systems.

> **Note:** The **BlockingQueue** interface is a part of the Java Collections Framework and provides a way to handle producer-consumer problems in a multithreaded environment.

## Core Concepts
The **BlockingQueue** interface provides several key methods for adding, removing, and inspecting elements, including **add**, **offer**, **put**, **take**, **poll**, and **peek**. The **BlockingQueue** interface also provides several implementations, including **ArrayBlockingQueue** and **LinkedBlockingQueue**.

*   **ArrayBlockingQueue**: A bounded blocking queue backed by an array. This queue orders elements in a FIFO manner.
*   **LinkedBlockingQueue**: An optionally bounded blocking queue backed by linked nodes. This queue orders elements in a FIFO manner.

> **Tip:** When choosing between **ArrayBlockingQueue** and **LinkedBlockingQueue**, consider the performance and memory requirements of your application. **ArrayBlockingQueue** is more memory-efficient, but **LinkedBlockingQueue** provides better performance for large queues.

## How It Works Internally
The **BlockingQueue** interface provides a way to handle producer-consumer problems in a multithreaded environment. When a producer thread adds an element to the queue, it will block until the queue is not full. Similarly, when a consumer thread removes an element from the queue, it will block until the queue is not empty.

Here is a step-by-step breakdown of how **BlockingQueue** works internally:

1.  The producer thread adds an element to the queue using the **put** method.
2.  If the queue is full, the producer thread will block until an element is removed from the queue.
3.  The consumer thread removes an element from the queue using the **take** method.
4.  If the queue is empty, the consumer thread will block until an element is added to the queue.

## Code Examples
Here are three complete and runnable examples of using **BlockingQueue**:

### Example 1: Basic Usage
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class BasicBlockingQueueExample {
    public static void main(String[] args) throws InterruptedException {
        // Create a linked blocking queue
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();

        // Add elements to the queue
        queue.put("Element 1");
        queue.put("Element 2");
        queue.put("Element 3");

        // Remove elements from the queue
        System.out.println(queue.take());
        System.out.println(queue.take());
        System.out.println(queue.take());
    }
}
```

### Example 2: Producer-Consumer Pattern
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ProducerConsumerExample {
    public static void main(String[] args) {
        // Create a linked blocking queue
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();

        // Create a producer thread
        Thread producerThread = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    queue.put("Element " + i);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // Create a consumer thread
        Thread consumerThread = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    System.out.println(queue.take());
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        // Start the producer and consumer threads
        producerThread.start();
        consumerThread.start();
    }
}
```

### Example 3: Using ArrayBlockingQueue
```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class ArrayBlockingQueueExample {
    public static void main(String[] args) {
        // Create an array blocking queue with a capacity of 5
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);

        // Add elements to the queue
        try {
            queue.put("Element 1");
            queue.put("Element 2");
            queue.put("Element 3");
            queue.put("Element 4");
            queue.put("Element 5");

            // Attempt to add an element to a full queue
            try {
                queue.put("Element 6");
            } catch (InterruptedException e) {
                System.out.println("Queue is full");
            }

            // Remove elements from the queue
            System.out.println(queue.take());
            System.out.println(queue.take());
            System.out.println(queue.take());
            System.out.println(queue.take());
            System.out.println(queue.take());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## Visual Diagram
```mermaid
sequenceDiagram
    participant Producer as "Producer Thread"
    participant Queue as "BlockingQueue"
    participant Consumer as "Consumer Thread"

    Note over Producer,Queue,Consumer: Producer adds an element to the queue
    Producer->>Queue: put(element)
    Note over Producer,Queue,Consumer: Queue is not full, so the producer continues
    Note over Producer,Queue,Consumer: Consumer removes an element from the queue
    Consumer->>Queue: take()
    Note over Producer,Queue,Consumer: Queue is not empty, so the consumer continues
    Note over Producer,Queue,Consumer: Producer attempts to add an element to a full queue
    Producer->>Queue: put(element)
    Note over Producer,Queue,Consumer: Producer blocks until the queue is not full
    Note over Producer,Queue,Consumer: Consumer removes an element from the queue
    Consumer->>Queue: take()
    Note over Producer,Queue,Consumer: Producer unblocks and adds the element to the queue
    Producer->>Queue: put(element)
```
The diagram illustrates the producer-consumer pattern using a **BlockingQueue**. The producer thread adds elements to the queue, and the consumer thread removes elements from the queue. If the queue is full, the producer thread will block until an element is removed from the queue. Similarly, if the queue is empty, the consumer thread will block until an element is added to the queue.

## Comparison
The following table compares the different implementations of **BlockingQueue**:

| Implementation | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| **ArrayBlockingQueue** | O(1) for add, remove, and peek operations | O(n) for n elements | Memory-efficient, bounded queue | Fixed capacity, slower than **LinkedBlockingQueue** for large queues | Small to medium-sized queues, memory-constrained environments |
| **LinkedBlockingQueue** | O(1) for add, remove, and peek operations | O(n) for n elements | Optionally bounded, better performance for large queues | Slower than **ArrayBlockingQueue** for small queues, more memory-intensive | Large queues, high-performance applications |
| **PriorityBlockingQueue** | O(log n) for add and remove operations, O(1) for peek operation | O(n) for n elements | Priority-based ordering, optionally bounded | Slower than **ArrayBlockingQueue** and **LinkedBlockingQueue**, more memory-intensive | Priority-based queues, job scheduling |

> **Warning:** When choosing a **BlockingQueue** implementation, consider the performance and memory requirements of your application. **ArrayBlockingQueue** is more memory-efficient, but **LinkedBlockingQueue** provides better performance for large queues.

## Real-world Use Cases
Here are three real-world use cases for **BlockingQueue**:

*   **Job Scheduling:** A job scheduling system can use a **BlockingQueue** to manage jobs. The producer thread can add jobs to the queue, and the consumer thread can remove jobs from the queue and execute them.
*   **Message Passing:** A message passing system can use a **BlockingQueue** to manage messages. The producer thread can add messages to the queue, and the consumer thread can remove messages from the queue and process them.
*   **Data Processing:** A data processing system can use a **BlockingQueue** to manage data. The producer thread can add data to the queue, and the consumer thread can remove data from the queue and process it.

> **Interview:** When asked about **BlockingQueue** in an interview, be prepared to explain the different implementations, their pros and cons, and how to use them in real-world scenarios.

## Common Pitfalls
Here are four common pitfalls to watch out for when using **BlockingQueue**:

*   **Not Handling InterruptedException:** When using **BlockingQueue**, it is essential to handle **InterruptedException** properly. If an **InterruptedException** is not handled, the thread may be interrupted, and the queue may be left in an inconsistent state.
*   **Not Checking for Queue Fullness:** When adding elements to a **BlockingQueue**, it is essential to check for queue fullness. If the queue is full, the producer thread will block until an element is removed from the queue.
*   **Not Using a Fair Lock:** When using **BlockingQueue**, it is essential to use a fair lock to ensure that threads are treated fairly. If a fair lock is not used, threads may be starved, and the queue may be left in an inconsistent state.
*   **Not Using a Bounded Queue:** When using **BlockingQueue**, it is essential to use a bounded queue to prevent the queue from growing indefinitely. If the queue is not bounded, it may consume all available memory, and the system may crash.

> **Tip:** When using **BlockingQueue**, always handle **InterruptedException** properly, check for queue fullness, use a fair lock, and use a bounded queue to prevent common pitfalls.

## Interview Tips
Here are three common interview questions related to **BlockingQueue**:

*   **What is the difference between ArrayBlockingQueue and LinkedBlockingQueue?**
    *   Weak answer: **ArrayBlockingQueue** is faster than **LinkedBlockingQueue**.
    *   Strong answer: **ArrayBlockingQueue** is more memory-efficient than **LinkedBlockingQueue**, but **LinkedBlockingQueue** provides better performance for large queues.
*   **How do you handle InterruptedException when using BlockingQueue?**
    *   Weak answer: You can ignore **InterruptedException**.
    *   Strong answer: You should handle **InterruptedException** properly by checking the interrupted flag and taking appropriate action.
*   **What is the purpose of using a fair lock with BlockingQueue?**
    *   Weak answer: A fair lock is not necessary with **BlockingQueue**.
    *   Strong answer: A fair lock ensures that threads are treated fairly and prevents thread starvation.

> **Warning:** When answering interview questions related to **BlockingQueue**, be prepared to explain the different implementations, their pros and cons, and how to use them in real-world scenarios.

## Key Takeaways
Here are ten key takeaways to remember when using **BlockingQueue**:

*   **BlockingQueue** is a thread-safe implementation of a queue that follows the FIFO principle.
*   **ArrayBlockingQueue** is more memory-efficient than **LinkedBlockingQueue**, but **LinkedBlockingQueue** provides better performance for large queues.
*   **BlockingQueue** can be used to manage jobs, messages, and data in a multithreaded environment.
*   **BlockingQueue** provides several methods for adding, removing, and inspecting elements, including **add**, **offer**, **put**, **take**, **poll**, and **peek**.
*   **BlockingQueue** can be bounded or unbounded, depending on the implementation.
*   **BlockingQueue** can be used with a fair lock to ensure that threads are treated fairly.
*   **InterruptedException** should be handled properly when using **BlockingQueue**.
*   **BlockingQueue** can be used to prevent thread starvation and ensure that threads are treated fairly.
*   **BlockingQueue** provides a way to handle producer-consumer problems in a multithreaded environment.
*   **BlockingQueue** is an essential component of the Java Concurrency Utilities and is widely used in real-world applications.

> **Note:** When using **BlockingQueue**, always remember to handle **InterruptedException** properly, check for queue fullness, use a fair lock, and use a bounded queue to prevent common pitfalls.