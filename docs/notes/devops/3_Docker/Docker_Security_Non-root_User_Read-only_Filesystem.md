---
title: "Docker Security: Non-root User, Read-only Filesystem"
topic: "Docker Security: Non-root User, Read-only Filesystem"
section: "devops"
tags: "devops, docker-security, programming, notes, interview"
banner: "https://picsum.photos/seed/326/1200/630"
update_count: 0
---

![Docker Security](https://miro.medium.com/max/1400/1*oKuYd9jTj6fQ6T5eKbV2Fg.png)

## Introduction
Docker security is a critical aspect of containerization, as it ensures the integrity and confidentiality of applications running in containers. One of the key security features in Docker is the ability to run containers as non-root users and with a read-only filesystem. This feature is essential in preventing unauthorized access to sensitive data and reducing the attack surface of containers. In this section, we will explore the importance of Docker security, its relevance in real-world scenarios, and why every engineer needs to know about it.

> **Note:** Docker security is not just about running containers as non-root users and with a read-only filesystem. It also involves other aspects such as network security, volume mounting, and image scanning.

## Core Concepts
To understand Docker security, it's essential to grasp the core concepts involved. Here are some key terms and definitions:

* **Non-root user:** A user who is not the root user (UID 0) and does not have elevated privileges.
* **Read-only filesystem:** A filesystem that is mounted as read-only, preventing any modifications to the filesystem.
* **Docker image:** A template that contains the application code, dependencies, and configuration.
* **Docker container:** A runtime instance of a Docker image.

Mental models and analogies can help simplify complex concepts. Think of a Docker container as a virtual machine, but instead of running a full-fledged operating system, it runs a single application. The non-root user and read-only filesystem features are like additional layers of security that prevent unauthorized access to sensitive data.

## How It Works Internally
When a Docker container is created, it runs as the root user by default. However, this can be changed by specifying a non-root user in the Dockerfile or when running the container. The Docker daemon uses the `user` directive in the Dockerfile to set the user ID and group ID of the container.

Here's a step-by-step breakdown of how it works:

1. The Docker daemon creates a new container from the specified Docker image.
2. The `user` directive in the Dockerfile sets the user ID and group ID of the container.
3. The container runs as the specified non-root user.
4. The filesystem is mounted as read-only, preventing any modifications.

> **Warning:** Running containers as non-root users and with read-only filesystems can break some applications that rely on writing to the filesystem. Be sure to test your application thoroughly before deploying it to production.

## Code Examples
Here are three complete and runnable code examples that demonstrate Docker security features:

### Example 1: Basic Non-root User
```dockerfile
# Create a new Dockerfile
FROM ubuntu:latest

# Set the non-root user
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser

# Run the command
CMD ["echo", "Hello, World!"]
```
This example creates a new Docker image with a non-root user `myuser`. The `USER` directive sets the user ID and group ID of the container to `myuser`.

### Example 2: Read-only Filesystem
```dockerfile
# Create a new Dockerfile
FROM ubuntu:latest

# Set the read-only filesystem
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN chmod -R a-w /app

# Run the command
CMD ["echo", "Hello, World!"]
```
This example creates a new Docker image with a read-only filesystem. The `chmod` command sets the permissions of the `/app` directory to read-only.

### Example 3: Advanced Non-root User and Read-only Filesystem
```dockerfile
# Create a new Dockerfile
FROM ubuntu:latest

# Set the non-root user
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser

# Set the read-only filesystem
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN chmod -R a-w /app

# Run the command
CMD ["echo", "Hello, World!"]
```
This example combines the non-root user and read-only filesystem features. The `USER` directive sets the user ID and group ID of the container to `myuser`, and the `chmod` command sets the permissions of the `/app` directory to read-only.

## Visual Diagram
```mermaid
graph LR
    A[Docker Image] -->|Create|> B[Docker Container]
    B -->|Set User|> C[Non-root User]
    B -->|Mount Filesystem|> D[Read-only Filesystem]
    C -->|Run Command|> E[CMD]
    D -->|Run Command|> E
    E -->|Output|> F[Hello, World!]
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#f9f,stroke:#333,stroke-width:4px
    style C fill:#ccf,stroke:#333,stroke-width:4px
    style D fill:#ccf,stroke:#333,stroke-width:4px
    style E fill:#ff9,stroke:#333,stroke-width:4px
    style F fill:#ff9,stroke:#333,stroke-width:4px
```
This diagram illustrates the Docker security features, including non-root users and read-only filesystems. The Docker image is created, and the Docker container is set up with a non-root user and a read-only filesystem. The command is run, and the output is displayed.

> **Tip:** Use the `docker exec` command to verify that the container is running as a non-root user and with a read-only filesystem.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Non-root User | O(1) | O(1) | Improved security, reduced attack surface | May break some applications | Most use cases |
| Read-only Filesystem | O(1) | O(1) | Improved security, reduced data tampering | May break some applications | Most use cases |
| Combination of Both | O(1) | O(1) | Improved security, reduced attack surface and data tampering | May break some applications | Critical systems |
| Root User with Writeable Filesystem | O(1) | O(1) | Simplified application development, easier debugging | Reduced security, increased attack surface | Development environments |

## Real-world Use Cases
Here are three real-world use cases that demonstrate the importance of Docker security features:

1. **Google's Kubernetes:** Google's Kubernetes platform uses Docker containers to run applications. Kubernetes uses non-root users and read-only filesystems to improve security and reduce the attack surface.
2. **Amazon's ECS:** Amazon's ECS (EC2 Container Service) uses Docker containers to run applications. ECS uses non-root users and read-only filesystems to improve security and reduce the attack surface.
3. **Red Hat's OpenShift:** Red Hat's OpenShift platform uses Docker containers to run applications. OpenShift uses non-root users and read-only filesystems to improve security and reduce the attack surface.

## Common Pitfalls
Here are four common mistakes that engineers make when implementing Docker security features:

1. **Incorrect User ID and Group ID:** Using the wrong user ID and group ID can lead to permission issues and security vulnerabilities.
```dockerfile
# Wrong
USER 1000:1000
# Right
USER myuser:myuser
```
2. **Incorrect Filesystem Permissions:** Using the wrong filesystem permissions can lead to security vulnerabilities and data tampering.
```dockerfile
# Wrong
RUN chmod -R a+w /app
# Right
RUN chmod -R a-w /app
```
3. **Not Testing Thoroughly:** Not testing the application thoroughly can lead to unexpected behavior and security vulnerabilities.
```bash
# Wrong
docker build -t myimage .
docker run -it myimage
# Right
docker build -t myimage .
docker run -it myimage --rm
```
4. **Not Monitoring and Logging:** Not monitoring and logging the application can lead to security vulnerabilities and data tampering.
```bash
# Wrong
docker run -it myimage
# Right
docker run -it myimage --log-driver json-file
```
> **Interview:** Can you explain the importance of Docker security features, such as non-root users and read-only filesystems? How do you implement these features in your Dockerfiles and containers?

## Interview Tips
Here are three common interview questions related to Docker security features:

1. **What are the benefits of using non-root users and read-only filesystems in Docker containers?**
	* Weak answer: "It's more secure, I guess."
	* Strong answer: "Using non-root users and read-only filesystems in Docker containers improves security by reducing the attack surface and preventing unauthorized access to sensitive data."
2. **How do you implement non-root users and read-only filesystems in your Dockerfiles and containers?**
	* Weak answer: "I use the `USER` directive and `chmod` command, I think."
	* Strong answer: "I use the `USER` directive to set the user ID and group ID of the container, and the `chmod` command to set the filesystem permissions. I also test my application thoroughly to ensure that it works correctly with these security features."
3. **What are some common mistakes that engineers make when implementing Docker security features, and how can you avoid them?**
	* Weak answer: "I'm not sure, I guess you just have to be careful."
	* Strong answer: "Some common mistakes include incorrect user ID and group ID, incorrect filesystem permissions, not testing thoroughly, and not monitoring and logging. To avoid these mistakes, I use the correct syntax and test my application thoroughly, and I also monitor and log my containers to detect any security issues."

## Key Takeaways
Here are ten key takeaways to remember about Docker security features:

* **Non-root users and read-only filesystems improve security** by reducing the attack surface and preventing unauthorized access to sensitive data.
* **Use the `USER` directive** to set the user ID and group ID of the container.
* **Use the `chmod` command** to set the filesystem permissions.
* **Test your application thoroughly** to ensure that it works correctly with these security features.
* **Monitor and log your containers** to detect any security issues.
* **Use the correct syntax** to avoid common mistakes.
* **Be careful when using root users and writeable filesystems**, as they can reduce security.
* **Use Docker security features** in conjunction with other security measures, such as network security and volume mounting.
* **Keep your Docker images and containers up to date** to ensure that you have the latest security patches and features.
* **Use Docker security tools and plugins**, such as Docker Security Scanning and Docker Bench for Security, to improve security and detect vulnerabilities.