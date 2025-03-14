# Part 3 - Communication

- Patterns, Paradigms, Programming, Protocols

## Sockets

- System level communication interface
- Streams vs Datagrams

### Addressing

- Resolving hostnames

## MPI

- Message-oriented
- Maximizes potential efficiency

## Messaging Interfaces

- Variety of higher-level interfaces with different use targets

### Pub/Sub

- Publication and Subscription are decoupled via brokers

## Messaging comparisons

- Blocking vs Non-blocking
- Synchronous vs Asynchronous
- Direct vs Indirect

| Characteristic | **Blocking** | **Non-blocking** |
|---------------|--------------|------------------|
| **Definition** | Sender is suspended until message is received or processed | Sender continues execution after sending a message without waiting |
| **Control Flow** | Halts execution of sending process until operation completes | Allows sending process to continue execution immediately |
| **Resource Utilization** | Can lead to inefficient use of CPU time while waiting | Better CPU utilization as processes don't wait idle |
| **Programming Model** | Simpler programming model, sequential execution | More complex programming with callbacks or polling |
| **Use Cases** | Critical operations where processing order matters | I/O-bound applications, user interfaces, high-throughput systems |

| Characteristic | **Synchronous** | **Asynchronous** |
|----------------|-----------------|------------------|
| **Definition** | Communication follows a defined timing sequence | Communication occurs without timing coordination between parties |
| **Message Handling** | Sender waits for receiver to process message | Sender doesn't wait for receiver to process message |
| **Coordination** | Both parties must be available during communication | Parties can operate independently at their own pace |
| **Performance Impact** | Can create performance bottlenecks | Better throughput in high-latency environments |
| **Error Handling** | Immediate feedback on errors | Error handling requires separate mechanisms |
| **Example** | Remote procedure calls, HTTP requests | Message queues, email, event-driven architectures |

| Characteristic | **Direct** | **Indirect** |
|----------------|------------|--------------|
| **Addressing** | Messages sent to specific, known recipients | Messages sent to intermediaries (queues, topics, channels) |
| **Coupling** | Tighter coupling between sender and receiver | Looser coupling, participants may not know each other |
| **Scalability** | Limited by direct connections between components | Better scalability as components don't need direct connections |
| **Fault Tolerance** | More vulnerable to receiver unavailability | Better fault tolerance with message persistence |
| **Routing Control** | Limited routing options | Flexible routing based on content, topics, or patterns |
| **Implementation Examples** | Socket communication, named pipes | Message brokers, publish-subscribe systems, event buses |
