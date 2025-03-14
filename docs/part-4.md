# Part 4 - Networking

## Topologies

* Data Center Network Topologies
* Multipath, Multistage, Multilink, challenges and benefits

| Feature          | Multipath          | Multistage          | Multilink          | Challenges             | Benefits                |
|------------------|----------------------|----------------------|----------------------|------------------------|-------------------------|
| **Definition**     | Multiple paths for data transmission.  Data travels through several paths before reaching its destination. | Series of optical switches or amplifiers to increase bandwidth and reduce signal loss. |  A single fiber optic link with multiple optical splitters to increase bandwidth and reduce distance. | High cost, complex implementation, potential for signal degradation | Increased bandwidth, reduced signal loss, improved reliability |
| **How it Works**   | Data travels along multiple paths, often with different wavelengths. |  Multiple optical switches/amplifiers placed in a sequence. |  Optical splitters create multiple paths from a single fiber. |  Difficult to implement, requires careful alignment and control. | Higher bandwidth, reduced signal loss, improved signal quality |
| **Complexity**     | Relatively simple conceptually. | Complex – requires careful design and control. | Moderate – requires managing multiple optical paths. | High complexity, requires specialized equipment and expertise. | Simplified system design, lower implementation costs |
| **Typical Use**   |  High-bandwidth applications like video streaming, large data transfers. |  Longer distances, high-capacity networks. |  Dense-mode fiber optic networks, long-haul connections. | High initial cost, difficult to troubleshoot, requires significant investment | Reduced bandwidth costs, improved network capacity, increased distance capabilities |
| **Main Benefit**  |  Increased bandwidth & reduced latency for certain applications. |  Increased bandwidth, improved reliability, reduced congestion. |  Increased bandwidth & reduced cost for long-distance connections. |  High initial cost & complexity, specialized expertise needed |  Enhanced network capacity, improved performance, reduced deployment costs |

## Virtualization

* Basic VLANs
* Other virtualization protocols and models

## SDN and NFV

* Software Defined Networking
* Routers and Routing, Switches and Switching
* Match, Action pairs and Flow Tables
* What is a firewall? What is a NAT?
* Network Function Virtualization

## Software Defined Networking (SDN)

| Characteristic | **Traditional Networking** | **Software Defined Networking** |
|----------------|----------------------------|--------------------------------|
| **Architecture** | Integrated control and data planes within each device | Separation of control plane and data plane |
| **Control** | Distributed control across network devices | Centralized control via SDN controller |
| **Programmability** | Limited programmability via CLI/SNMP | Highly programmable via APIs and software interfaces |
| **Management** | Device-by-device configuration | Network-wide policy implementation |
| **Flexibility** | Static configurations, limited automation | Dynamic configuration, highly automated |
| **Innovation Pace** | Slow, dependent on vendor development cycles | Rapid, software-driven innovation |
| **Protocols** | Vendor-specific or standard protocols (OSPF, BGP) | OpenFlow, NETCONF, REST APIs |
| **Visibility** | Limited network-wide visibility | Comprehensive network-wide visibility |

## Routers and Routing, Switches and Switching

| Characteristic | **Routers/Routing** | **Switches/Switching** |
|----------------|---------------------|------------------------|
| **OSI Layer** | Network layer (Layer 3) | Data link layer (Layer 2) |
| **Addressing** | Uses IP addresses | Uses MAC addresses |
| **Scope** | Between networks/subnets | Within the same network/broadcast domain |
| **Decision Making** | Route selection based on IP addressing and routing tables | Frame forwarding based on MAC address tables |
| **Protocols** | BGP, OSPF, RIP, EIGRP | Spanning Tree Protocol (STP), VLANs |
| **Function** | Connects different networks and routes traffic between them | Connects devices within a network segment |
| **Broadcast Handling** | Typically blocks broadcasts | Forwards broadcasts within a VLAN |
| **Intelligence** | Higher processing overhead for packet inspection | Lower processing overhead for frame switching |
| **Typical Use** | Internet connectivity, WAN connections | LAN connectivity, workgroup connections |

## Match, Action Pairs and Flow Tables

| Characteristic | **Description** | **Example** |
|----------------|-----------------|-------------|
| **Match Fields** | Packet header fields used for comparison | Source/destination IP, MAC, ports, protocol type |
| **Actions** | Operations performed on matching packets | Forward, drop, modify, count, queue |
| **Flow Table Structure** | Ordered collection of flow entries | Priority, match fields, counters, actions, timeouts |
| **Processing Pipeline** | Sequential evaluation through multiple tables | Packet enters → matched → actions applied → next table |
| **Entry Types** | Different rule types in flow tables | Exact match, wildcard match, priority-based entries |
| **Controller Interaction** | When no match is found in flow tables | Packet sent to controller, controller adds new flow entry |
| **Performance Factors** | Elements affecting flow table operation | Table size, lookup speed, update frequency |
| **Security Considerations** | Security aspects of flow tables | Flow rule verification, authentication of updates |

## Firewall and NAT

| Characteristic | **Firewall** | **Network Address Translation (NAT)** |
|----------------|--------------|--------------------------------------|
| **Primary Purpose** | Security - filters traffic based on rules | Addressing - maps private IPs to public IPs |
| **Function** | Controls incoming/outgoing network traffic | Modifies packet headers to enable shared public IP usage |
| **Types** | Stateless, stateful, next-gen, WAF, proxy | Static NAT, Dynamic NAT, PAT (Port Address Translation) |
| **OSI Layers** | Can operate at layers 3-7 depending on type | Primarily operates at layers 3-4 |
| **Security Role** | Primary security device | Security by obscuring internal addressing |
| **Configuration Focus** | Access control rules, inspection depth | Address pools, port mapping, timeouts |
| **Typical Placement** | Network perimeter, segments, hosts | Edge of private networks |
| **Scalability Impact** | Can become bottleneck under high traffic | Can limit connection capacity due to port exhaustion |
| **Modern Implementations** | Integrated in UTM, cloud security groups | Built into routers, load balancers, firewalls |

## Network Function Virtualization (NFV)

| Characteristic | **Traditional Network Functions** | **Network Function Virtualization** |
|----------------|----------------------------------|-------------------------------------|
| **Implementation** | Dedicated physical appliances | Software running on standard hardware |
| **Hardware Dependency** | Purpose-built proprietary hardware | Commodity x86 servers, storage, switches |
| **Deployment Time** | Days to weeks | Minutes to hours |
| **Scalability** | Hardware addition/replacement required | Dynamic scaling through virtualization |
| **Capital Expense** | High upfront costs for equipment | Reduced CAPEX, pay-as-you-grow model |
| **Operational Expense** | Higher power, cooling, space requirements | Lower operational costs through consolidation |
| **Function Examples** | Physical routers, firewalls, load balancers | vRouter, vFirewall, vLoadBalancer, vIDS/IPS |
| **Management** | Often device-specific management interfaces | Unified management platforms |
| **Service Chaining** | Manual, hardware-based connections | Dynamic, software-defined service chaining |
| **Vendor Dependency** | Often locked to specific vendors | Multi-vendor support on common infrastructure |
