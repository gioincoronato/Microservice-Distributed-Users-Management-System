# Distributed Microservices User Management System

A robust, containerized microservices architecture built to demonstrate inter-service communication using REST, gRPC, and asynchronous message brokering (STOMP/JMS).

## Architecture Overview

The system is designed with independent services handling specific domains, connected through an API Gateway. The flow matches the following architecture:

```mermaid
graph TD
    Client[Client Python] -->|http / status| API[API GATEWAY Flask]
    API -->|gRPC Request / Response ACK-ERR| US[User Service Py gRPC]
    US -->|insert / ACK-ERR| DB[(MongoDB)]
    US -->|STOMP pub if success| Topic{Topic}
    Topic -->|JMS sub| NS[Notification SERVICE JAVA]
