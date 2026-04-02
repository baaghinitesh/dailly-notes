---
title: "Redis Cluster: Sharding, Hash Slots (0-16383)"
topic: "Redis Cluster: Sharding, Hash Slots (0-16383)"
section: "databases"
tags: "databases, redis-cluster, programming, notes, interview"
banner: "https://image.pollinations.ai/prompt/databases%20Redis%20Cluster%20Sharding,%20Hash%20Slots%20(0-16383)%20programming%20abstract?width=1200&height=630&nologo=true"
update_count: 0
---

![Redis Cluster](https://redis.io/images/redis-white.png)

## Introduction
**Redis Cluster** is a distributed, in-memory data store that provides high availability and horizontal scalability for Redis databases. It's designed to handle large amounts of data and provide low-latency access to that data. In a Redis Cluster, data is automatically sharded across multiple Redis nodes, allowing the system to scale horizontally and providing high availability. Every engineer needs to know about Redis Cluster because it's a crucial component in many modern web applications, and understanding how it works is essential for designing and implementing scalable and reliable systems.

## Core Concepts
- **Sharding**: The process of dividing a large dataset into smaller, more manageable pieces called shards. In Redis Cluster, sharding is done using a concept called **hash slots**, which are 16384 (0-16383) possible slots that can be used to map keys to nodes.
- **Hash Slots**: A hash slot is a 14-bit integer that represents a specific range of keys in the Redis Cluster. Each node in the cluster is responsible for a subset of the 16384 possible hash slots.
- **Node**: A Redis instance that is part of the cluster. Each node is responsible for a subset of the hash slots and stores the corresponding data.
- **Master Node**: A node that is responsible for a specific subset of hash slots and stores the primary copy of the data.
- **Slave Node**: A node that replicates the data from a master node and can take over as the master node if the original master node fails.

## How It Works Internally
When a client connects to a Redis Cluster, it sends a request to one of the nodes in the cluster. The node then uses the **CRC16** algorithm to calculate the hash slot for the key in the request. The node then checks if it is responsible for the calculated hash slot. If it is, the node processes the request. If not, the node redirects the client to the node that is responsible for the hash slot.

Here's a step-by-step breakdown of how Redis Cluster works:

1. The client connects to a node in the cluster.
2. The client sends a request to the node.
3. The node calculates the hash slot for the key in the request using the CRC16 algorithm.
4. The node checks if it is responsible for the calculated hash slot.
5. If the node is responsible for the hash slot, it processes the request.
6. If the node is not responsible for the hash slot, it redirects the client to the node that is responsible for the hash slot.

> **Note:** The CRC16 algorithm is used to calculate the hash slot for a key because it's a fast and efficient algorithm that produces a fixed-size hash value.

## Code Examples
### Example 1: Basic Redis Cluster Setup
```python
import redis

# Create a Redis Cluster client
cluster = redis.RedisCluster(
    startup_nodes=[
        {'host': 'localhost', 'port': '7000'},
        {'host': 'localhost', 'port': '7001'},
        {'host': 'localhost', 'port': '7002'}
    ]
)

# Set a key-value pair
cluster.set('foo', 'bar')

# Get the value for the key
print(cluster.get('foo'))
```

### Example 2: Redis Cluster with Master and Slave Nodes
```python
import redis

# Create a Redis Cluster client
cluster = redis.RedisCluster(
    startup_nodes=[
        {'host': 'localhost', 'port': '7000'},  # Master node
        {'host': 'localhost', 'port': '7001'},  # Slave node
        {'host': 'localhost', 'port': '7002'}  # Slave node
    ]
)

# Set a key-value pair
cluster.set('foo', 'bar')

# Get the value for the key
print(cluster.get('foo'))

# Simulate a failure of the master node
# cluster.node('localhost:7000').down()

# Get the value for the key again
print(cluster.get('foo'))
```

### Example 3: Redis Cluster with Hash Tags
```python
import redis

# Create a Redis Cluster client
cluster = redis.RedisCluster(
    startup_nodes=[
        {'host': 'localhost', 'port': '7000'},
        {'host': 'localhost', 'port': '7001'},
        {'host': 'localhost', 'port': '7002'}
    ]
)

# Set a key-value pair with a hash tag
cluster.set('{user:1}:foo', 'bar')

# Get the value for the key
print(cluster.get('{user:1}:foo'))
```

## Visual Diagram
```mermaid
flowchart TD
    A[Client] -->|Request|> B[Node 1]
    B -->|Hash Slot|> C[Hash Slot 1]
    C -->|Redirect|> D[Node 2]
    D -->|Process Request|> E[Response]
    E -->|Return Response|> A
    B -->|Hash Slot|> F[Hash Slot 2]
    F -->|Redirect|> G[Node 3]
    G -->|Process Request|> H[Response]
    H -->|Return Response|> A
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#f9f,stroke:#333,stroke-width:4px
    style C fill:#f9f,stroke:#333,stroke-width:4px
    style D fill:#f9f,stroke:#333,stroke-width:4px
    style E fill:#f9f,stroke:#333,stroke-width:4px
    style F fill:#f9f,stroke:#333,stroke-width:4px
    style G fill:#f9f,stroke:#333,stroke-width:4px
    style H fill:#f9f,stroke:#333,stroke-width:4px
```
The diagram shows how a client request is redirected to the correct node in the Redis Cluster based on the hash slot calculated for the key.

## Comparison
| Approach | Time Complexity | Space Complexity | Pros | Cons | Best For |
| --- | --- | --- | --- | --- | --- |
| Consistent Hashing | O(1) | O(n) | Provides a good distribution of keys across nodes | Can be complex to implement | Large-scale Redis Clusters |
| Modulo Hashing | O(1) | O(n) | Simple to implement | Can lead to hotspots | Small-scale Redis Clusters |
| Range-Based Hashing | O(log n) | O(n) | Provides a good distribution of keys across nodes | Can be complex to implement | Medium-scale Redis Clusters |
| Redis Cluster | O(1) | O(n) | Provides a good distribution of keys across nodes, supports automatic failover | Can be complex to set up and manage | Large-scale Redis Clusters |

## Real-world Use Cases
- **Instagram**: Uses Redis Cluster to store user data and provide low-latency access to that data.
- **Pinterest**: Uses Redis Cluster to store image metadata and provide low-latency access to that data.
- **Twitter**: Uses Redis Cluster to store tweet data and provide low-latency access to that data.

## Common Pitfalls
- **Incorrect hash slot calculation**: If the hash slot is not calculated correctly, the client may be redirected to the wrong node, leading to errors.
- **Insufficient node configuration**: If the nodes in the cluster are not configured correctly, the cluster may not be able to handle the load, leading to errors.
- **Inadequate failover configuration**: If the failover configuration is not set up correctly, the cluster may not be able to recover from node failures, leading to downtime.
- **Inconsistent data**: If the data is not consistent across the nodes in the cluster, the client may receive incorrect data, leading to errors.

> **Warning:** Incorrect hash slot calculation can lead to errors and downtime. Make sure to use the correct hash slot calculation algorithm.

## Interview Tips
- **What is Redis Cluster and how does it work?**: A strong answer should describe the basics of Redis Cluster, including sharding, hash slots, and node configuration.
- **How do you handle node failures in a Redis Cluster?**: A strong answer should describe the process of configuring failover and automatic failover in a Redis Cluster.
- **What are some common pitfalls when using Redis Cluster?**: A strong answer should describe some of the common pitfalls, including incorrect hash slot calculation, insufficient node configuration, and inadequate failover configuration.

> **Interview:** Be prepared to answer questions about Redis Cluster, including how it works, how to handle node failures, and common pitfalls.

## Key Takeaways
- **Redis Cluster is a distributed, in-memory data store**: Redis Cluster provides high availability and horizontal scalability for Redis databases.
- **Hash slots are used to shard data across nodes**: Hash slots are 16384 possible slots that can be used to map keys to nodes.
- **Nodes are responsible for a subset of hash slots**: Each node in the cluster is responsible for a subset of the 16384 possible hash slots.
- **Master nodes store primary data, slave nodes replicate data**: Master nodes store the primary copy of the data, while slave nodes replicate the data and can take over as the master node if the original master node fails.
- **CRC16 algorithm is used to calculate hash slots**: The CRC16 algorithm is used to calculate the hash slot for a key because it's a fast and efficient algorithm that produces a fixed-size hash value.
- **Redis Cluster provides low-latency access to data**: Redis Cluster provides low-latency access to data by automatically sharding data across nodes and using a fast and efficient algorithm to calculate hash slots.
- **Redis Cluster supports automatic failover**: Redis Cluster supports automatic failover, which allows the cluster to recover from node failures and provide high availability.
- **Incorrect hash slot calculation can lead to errors**: Incorrect hash slot calculation can lead to errors and downtime. Make sure to use the correct hash slot calculation algorithm.
- **Insufficient node configuration can lead to errors**: Insufficient node configuration can lead to errors and downtime. Make sure to configure the nodes correctly to handle the load.
- **Inadequate failover configuration can lead to downtime**: Inadequate failover configuration can lead to downtime. Make sure to configure failover correctly to provide high availability.