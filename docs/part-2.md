# Part 2 - Processes

- What does it take to run a program?
- What has to be stored about a process when it starts and stops?

## Threads

- What is a thread?
- How does a thread differ from a process?

## Functions / Co-routines

- What does it take to run a function?

## Communicating Processes

- Messages allow for coordinating processes
- Shared memory is another approach
- Communicating Sequential Processes

## Virtualization (Virtual Machines)

- What are Virtual Machines?
- Entities that act like a computer systems.

### Emulation

- Software that mimics the operation of hardware by interpreting instructions.
- An interpreter manages translation and updates the state of the emulated
  device based on the semantics of the instructions.

### System Virtualization

- Allows part of a machine to act as a distinct Virtual Machine, running native
  code for efficiency.

### Paravirtualization

- Runs native code for user code and calls the local OS for privileged actions

### Servers and code migration

- Another form of virtualization in a sense.
- Where do the code and data come from and where do they execute?

## Containers

- Another technology for providing Virtual Machines.
- Partitions a physical system differently
- Containers leverage existing systems to create VMs
- Elements are namespaces, control groups, and security policies.

### Orchestration

- We discussed in the context of containers, but orchestrators are not tied to
  containers.

## Virtual Machines - Aspects of Use

- Adaptability, Elasticity
- Isolation of software dependencies

