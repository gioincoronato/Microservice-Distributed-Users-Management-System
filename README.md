# Distributed Microservices User Management System

A robust, containerized microservices architecture for managing user accounts and asynchronous notifications. 

Built as a proof-of-concept to demonstrate modern backend patterns, this project integrates heterogeneous technologies:
* **Python & Java**
* **Flask & gRPC**
* **REST APIs & MongoDB**
* **Message Brokers (STOMP/JMS)**
* **Fully orchestrated with Docker**

## Architecture Overview

The system is designed with scalability and decoupling in mind. The architecture consists of the following isolated components:

* **Test Client (Python):** Simulates external HTTP requests to interact with the system.
* **API Gateway (Python/Flask):** The single entry point for external REST/HTTP calls. It routes traffic and translates HTTP requests into gRPC calls for internal services.
* **User Service (Python/gRPC):** The core business logic service. It handles high-performance gRPC requests from the Gateway, performs CRUD operations, and manages data persistence.
* **Database (MongoDB):** A NoSQL database used by the User Service to store user documents.
* **Message Broker (Topic):** Handles asynchronous event-driven communication. Whenever a user is successfully created, an event is published here.
* **Notification Service (Java):** An independent background service acting as a subscriber. It listens to the message broker topic to trigger post-creation workflows.

![Architecture Diagram](assets/architecture_diagram.png)

## How It Works

The data flow is designed to be fast and non-blocking:

1. The **Client** sends a standard HTTP request to the **API Gateway**.
2. The Gateway translates the HTTP call into a high-speed gRPC request and forwards it to the **User Service**.
3. The User Service processes the logic and interacts with **MongoDB** (e.g., inserting a new user).
4. Upon successful user creation, the User Service publishes a message to the **Message Broker** via STOMP.
5. The **Notification Service** (Java) asynchronously receives the message via JMS and simulates sending a welcome notification, without blocking the main user request.

## Live Demo

Below is a real-time demonstration of the test client executing CRUD operations, alongside the live Docker logs showing the microservices communicating and the database updating:



https://github.com/user-attachments/assets/eac232f8-6d4d-426f-8ea3-f204225d0312

<video src="https://github.com/user-attachments/assets/eac232f8-6d4d-426f-8ea3-f204225d0312" autoplay loop muted playsinline width="100%"></video>


