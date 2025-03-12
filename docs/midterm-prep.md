# stuff to prepare (bill of materials)

## RISC vs CISC

RISC and x86 are different architectures for computer processors that differ in the complexity of their instruction sets. RISC (Reduced Instruction Set Computing) is more efficient and uses less power, while x86 (Complex Instruction Set Computing) is more widely used. [1, 2, 3, 4, 5]

|  | RISC | x86  |
| --- | --- | --- |
| Instructions | Simple instructions that execute in one clock cycle | Complex instructions that can perform multiple tasks  |
| Design | Simpler design that's easier to pipeline | More complex design that's harder to design  |
| Power consumption | More efficient and uses less power | Less efficient and uses more power  |
| Performance | High performance per watt | Widely used for personal computers  |

RISC processors are good for battery-operated devices that need to be energy efficient. x86 processors are the most widely used instruction set for personal computers. [3, 4]
RISC-V is a new architecture that's more user-friendly for designers. Western Digital uses RISC-V cores in its storage controllers to increase throughput while reducing power consumption. [5, 6]

## RPC vs gRPC

Remote Procedure Call (RPC) is a general concept, while gRPC is a specific implementation of RPC. gRPC is an open-source framework that's designed to be more efficient, flexible, and language-agnostic than traditional RPC. [1, 2, 3, 4, 5, 6, 7]

|  | RPC | gRPC  |
| --- | --- | --- |
| Description | A method for software applications to communicate over a network | An implementation of RPC that uses HTTP/2 and Protocol Buffers  |
| Features | Batching, broadcasting, callbacks, and select subroutine | Authentication, bidirectional streaming, flow control, and more  |
| Benefits | Allows applications to call remote functions as if they were local | Faster, easier to implement, and more web-friendly than other RPC implementations  |

gRPC was developed by Google in 2015. It's an open-source framework that's used in distributed systems. [4]
When choosing between RPC and gRPC, you can consider your application's requirements and whether gRPC's advantages outweigh the disadvantages of RPC. [8]

## microkernel vs monolithic (marcokernel)

Microkernels and macro (or monolithic) kernels are two different approaches to operating system (OS) kernel design. Here’s how they compare:

<!-- ### Key Differences Summary -->

| Feature           | Microkernel                      | Macro (Monolithic) Kernel                |
|------------------|---------------------------------|----------------------------------          |
| Architecture     | Minimal, modular                 | Large, integrated                         |
| Performance      | Slower due to IPC overhead       | Faster due to direct function calls       |
| Stability        | More stable (isolated services)  | Less stable (crash affects entire system) |
| Security         | Higher (less trusted code in kernel) | Lower (more code in kernel)           |
| Maintainability  | Easier (modular structure)        | Harder (tightly coupled code)            |
| Example OS       | MINIX, QNX, Hurd                  | Linux, Windows, BSD                      |

<!-- --- -->

In modern operating systems, there's often a hybrid approach, where kernels like Windows NT and macOS use a mix of microkernel and monolithic design principles to balance performance and modularity.

## actual questions by `swany`

[Part 1](part-1.md)

[Part 2](part-1.md)

[Part 3](part-1.md)

[Part 4](part-1.md)

## References

1. <https://emteria.com/blog/arm-vs-x86>
2. <https://premioinc.com/blogs/blog/risc-vs-cisc-harnessing-arm-and-x86-computing-solutions-for-rugged-edge-ai>
3. <https://www.arm.com/glossary/risc>
4. <https://www.linkedin.com/advice/3/what-benefits-drawbacks-x86-x64-architectures>
5. <https://www.dfrobot.com/blog-13483.html>
6. <https://medium.com/@techAstheticrisc-v-arm-and-x86-the-battle-for-dominance-in-the-future-of-computing-a579a7770b3c>
7. <https://medium.com/@vinciabhinav7/whats-grpc-when-to-use-grpc-part-1-an-overview-86efd5fa78a6>
8. <https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/>
9. <https://pandaquests.medium.com/differences-between-grpc-and-rpc-76d122104b4c>
10. <https://blog.postman.com/grpc-vs-rest/>
11. <https://konghq.com/blog/learning-center/what-is-grpc>
12. <https://sites.ualberta.ca/dept/chemeng/AIX-43/share/man/info/C/a_doc_lib/aixprggd/progcomc/rpc_feat.htm>
13. <https://en.wikipedia.org/wiki/GRPC>
14. <https://www.linkedin.com/pulse/comparing-rpc-grpc-look-pros-cons-each-technology-hugo-pagniez>
