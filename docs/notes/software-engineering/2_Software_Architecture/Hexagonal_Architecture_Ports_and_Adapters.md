---
title: "Hexagonal Architecture (Ports and Adapters)"
topic: "Hexagonal Architecture (Ports and Adapters)"
section: "software-engineering"
tags: "software-engineering, hexagonal-architecture-(ports-and-adapters), programming, notes, interview"
banner: "https://picsum.photos/seed/704/1200/630"
update_count: 0
---

![Hexagonal Architecture](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Hexagonal_Architecture_%28Ports_and_Adapters%29.svg/1280px-Hexagonal_Architecture_%28Ports_and_Adapters%29.svg.png)

## Introduction
Hexagonal Architecture, also known as Ports and Adapters Architecture, is a software architecture pattern that aims to separate the application's business logic from its infrastructure and presentation layers. This pattern was first introduced by Alistair Cockburn in 2005. The main goal of Hexagonal Architecture is to make the application more maintainable, testable, and flexible by decoupling the core business logic from the external world. In this architecture, the application is surrounded by ports, which define how the application interacts with the outside world, and adapters, which implement these ports to interact with specific infrastructure or presentation layers.

> **Note:** The Hexagonal Architecture pattern is also known as the "Clean Architecture" pattern, although this term is sometimes used to describe a broader set of principles.

Real-world relevance of Hexagonal Architecture can be seen in many modern web applications, where the business logic needs to be separated from the presentation layer and the infrastructure layer. For example, an e-commerce website's business logic should be independent of the database used to store the data and the web framework used to handle the requests.

## Core Concepts
The core concepts of Hexagonal Architecture are:

* **Ports**: A port is an interface that defines how the application interacts with the outside world. Ports are the entry and exit points of the application.
* **Adapters**: An adapter is an implementation of a port that interacts with a specific infrastructure or presentation layer.
* **Application Core**: The application core is the business logic of the application, which is decoupled from the infrastructure and presentation layers.
* **Infrastructure**: The infrastructure layer includes databases, file systems, networks, and other external systems that the application interacts with.
* **Presentation**: The presentation layer includes web frameworks, desktop applications, and mobile applications that interact with the application core.

> **Warning:** One common mistake is to confuse the ports with the adapters. Ports are the interfaces that define how the application interacts with the outside world, while adapters are the implementations of these ports.

## How It Works Internally
Here is a step-by-step breakdown of how Hexagonal Architecture works internally:

1. The application core receives a request from the outside world through a port.
2. The application core processes the request and sends a response back to the port.
3. The port is implemented by an adapter, which interacts with the specific infrastructure or presentation layer.
4. The adapter receives the response from the port and sends it to the outside world.

For example, in a web application, the application core receives a request from the web framework through a port. The application core processes the request and sends a response back to the port. The port is implemented by a web adapter, which interacts with the web framework and sends the response back to the client.

## Code Examples
### Example 1: Basic Usage
```java
// Port interface
public interface UserRepository {
    User getUser(int id);
}

// Adapter implementation
public class MySQLUserRepository implements UserRepository {
    @Override
    public User getUser(int id) {
        // MySQL database interaction
        return new User(id, "John Doe");
    }
}

// Application core
public class UserService {
    private UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUser(int id) {
        return userRepository.getUser(id);
    }
}

// Usage
public class Main {
    public static void main(String[] args) {
        UserRepository userRepository = new MySQLUserRepository();
        UserService userService = new UserService(userRepository);
        User user = userService.getUser(1);
        System.out.println(user.getName());
    }
}
```
In this example, the `UserRepository` interface is a port that defines how the application interacts with the user data. The `MySQLUserRepository` class is an adapter that implements this port to interact with a MySQL database. The `UserService` class is the application core that uses the `UserRepository` port to retrieve user data.

### Example 2: Real-World Pattern
```python
# Port interface
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Adapter implementation
class StripePaymentGateway(PaymentGateway):
    def process_payment(self, amount):
        # Stripe API interaction
        return True

# Application core
class PaymentService:
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def process_payment(self, amount):
        return self.payment_gateway.process_payment(amount)

# Usage
payment_gateway = StripePaymentGateway()
payment_service = PaymentService(payment_gateway)
payment_service.process_payment(10.99)
```
In this example, the `PaymentGateway` interface is a port that defines how the application interacts with the payment gateway. The `StripePaymentGateway` class is an adapter that implements this port to interact with the Stripe API. The `PaymentService` class is the application core that uses the `PaymentGateway` port to process payments.

### Example 3: Advanced Usage
```javascript
// Port interface
class Logger {
    log(message) {}
}

// Adapter implementation
class ConsoleLogger extends Logger {
    log(message) {
        console.log(message);
    }
}

// Application core
class LoggerFactory {
    createLogger() {
        return new ConsoleLogger();
    }
}

// Usage
const loggerFactory = new LoggerFactory();
const logger = loggerFactory.createLogger();
logger.log("Hello World!");
```
In this example, the `Logger` interface is a port that defines how the application interacts with the logging system. The `ConsoleLogger` class is an adapter that implements this port to interact with the console logging system. The `LoggerFactory` class is the application core that creates a logger instance using the `Logger` port.

## Visual Diagram
```mermaid
graph LR
    A[Application Core] -->|uses|> B[Port]
    B -->|implemented by|> C[Adapter]
    C -->|interacts with|> D[Infrastructure]
    A -->|uses|> E[Port]
    E -->|implemented by|> F[Adapter]
    F -->|interacts with|> G[Presentation]
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#ccc,stroke:#333,stroke-width:4px
    style C fill:#ccc,stroke:#333,stroke-width:4px
    style D fill:#f0f,stroke:#333,stroke-width:4px
    style E fill:#ccc,stroke:#333,stroke-width:4px
    style F fill:#ccc,stroke:#333,stroke-width:4px
    style G fill:#f0f,stroke:#333,stroke-width:4px
```
This diagram shows the relationship between the application core, ports, adapters, infrastructure, and presentation layers in a Hexagonal Architecture.

> **Tip:** The key to a successful Hexagonal Architecture is to keep the application core decoupled from the infrastructure and presentation layers. This allows for greater flexibility and maintainability.

## Comparison
| Architecture Pattern | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Hexagonal Architecture | O(1) | O(1) | Decouples application core from infrastructure and presentation layers, makes application more maintainable and testable | Requires more planning and design upfront, can be over-engineered | Complex web applications, enterprise software systems |
| Layered Architecture | O(n) | O(n) | Simple and easy to understand, works well for small applications | Can become monolithic and rigid, difficult to maintain and test | Small web applications, prototypes |
| Microservices Architecture | O(n) | O(n) | Allows for greater scalability and flexibility, makes it easier to develop and deploy individual services | Can be more complex to manage and communicate between services, requires more infrastructure | Large-scale web applications, distributed systems |
| Event-Driven Architecture | O(1) | O(1) | Allows for greater scalability and flexibility, makes it easier to handle high volumes of data | Can be more complex to manage and debug, requires more infrastructure | Real-time data processing systems, streaming data applications |

> **Interview:** Can you explain the difference between Hexagonal Architecture and Layered Architecture? How would you decide which one to use for a given project?

## Real-world Use Cases
1. **Amazon**: Amazon uses a Hexagonal Architecture for its e-commerce platform, separating the business logic from the infrastructure and presentation layers.
2. **Netflix**: Netflix uses a combination of Hexagonal Architecture and Microservices Architecture for its streaming service, allowing for greater scalability and flexibility.
3. **Uber**: Uber uses a Hexagonal Architecture for its ride-hailing platform, separating the business logic from the infrastructure and presentation layers.

## Common Pitfalls
1. **Tight Coupling**: One common mistake is to tightly couple the application core to the infrastructure or presentation layers, making it difficult to maintain and test.
2. **Over-Engineering**: Another mistake is to over-engineer the Hexagonal Architecture, making it too complex and rigid.
3. **Lack of Planning**: A lack of planning and design upfront can lead to a poorly implemented Hexagonal Architecture.
4. **Insufficient Testing**: Insufficient testing can lead to bugs and issues that are difficult to debug and fix.

> **Warning:** A common mistake is to confuse the ports with the adapters. Ports are the interfaces that define how the application interacts with the outside world, while adapters are the implementations of these ports.

## Interview Tips
1. **What is Hexagonal Architecture?**: Be prepared to explain the basics of Hexagonal Architecture, including the ports, adapters, and application core.
2. **How does it differ from Layered Architecture?**: Be prepared to explain the differences between Hexagonal Architecture and Layered Architecture.
3. **What are the benefits of using Hexagonal Architecture?**: Be prepared to explain the benefits of using Hexagonal Architecture, including decoupling the application core from the infrastructure and presentation layers.

> **Tip:** When answering interview questions, be sure to provide specific examples and use cases to illustrate your points.

## Key Takeaways
* **Decouple the application core from the infrastructure and presentation layers**: This is the key principle of Hexagonal Architecture.
* **Use ports and adapters to define interactions with the outside world**: Ports and adapters are the interfaces that define how the application interacts with the outside world.
* **Keep the application core simple and focused on business logic**: The application core should be simple and focused on the business logic, without worrying about the infrastructure and presentation layers.
* **Use a combination of Hexagonal Architecture and other patterns**: Hexagonal Architecture can be used in combination with other patterns, such as Microservices Architecture and Event-Driven Architecture.
* **Plan and design the architecture upfront**: Planning and designing the architecture upfront is crucial to a successful implementation of Hexagonal Architecture.
* **Test and debug thoroughly**: Testing and debugging are crucial to ensuring that the application works correctly and is maintainable.