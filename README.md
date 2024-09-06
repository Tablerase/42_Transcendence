# Project Overview

The modules are labeled as either major (*[1]*) or minor ([½]) components.

## Web and Backend

- *[1]* **Use a Framework as backend**: Implemented using Django, providing a structured and scalable backend architecture.
- *[½]* **Use a front-end framework or toolkit**: Bootstrap was utilized to enhance the frontend design and responsiveness.
- *[½]* **Use a database for the backend**: PostgreSQL was used to manage and maintain data consistency across the application.

## User Management

- *[1]* **Standard user management, authentication, users across tournaments**: Includes user registration, profile management, and game history tracking.
- *[1]* **Implementing a remote authentication (with 42 and Google)**: OAuth 2.0 integration for secure and convenient user authentication.

## Gameplay and User Experience

- *[1]* **Remote players**: Supports gameplay between players on different devices.
- *[½]* **Game Customization Options**: Offers features such as power-ups, attacks, and different maps to enhance gameplay.
- *[½]* **Expanding Browser Compatibility:** Ensures the application works seamlessly across different web browsers.

## Security

- *[½]* **Monitoring system**: Implements Prometheus and Grafana for real-time system monitoring and alerting.

## Rendering and Performance

- *[½]* **Server-Side Rendering (SSR) Integration**: Enhances performance by pre-rendering content on the server for faster page loads.

## Game Implementation

- *[1]* **Server-Side Pong**: Replaces the basic Pong game with a server-side version, enhancing gameplay through API integration.

## Total Points Calculation

Each major module contributes 1 point, and each minor module contributes 0.5 points.

- **Major Modules (6 points):** 6 major modules x 1 point each
- **Minor Modules (3 points):** 6 minor modules x 0.5 points each
- **Total:** 9 points

## Modules Breakdown Pie Chart

```mermaid
pie
    title Module Points Distribution for categories
    "Web and Backend" : 2
    "User Management" : 2
    "Gameplay and User Experience" : 2
    "Security" : 0.5
    "Rendering and Performance" : 0.5
    "Game Implementation" : 1
```

```mermaid
pie
    title Module Points Distribution for each module
    "Use a Framework as backend (1 point)" : 1
    "Use a front-end framework or toolkit (0.5 points)" : 0.5
    "Use a database for the backend (0.5 points)" : 0.5
    "Standard user management (1 point)" : 1
    "Implementing a remote authentication (1 point)" : 1
    "Remote players (1 point)" : 1
    "Game Customization Options (0.5 points)" : 0.5
    "Expanding Browser Compatibility (0.5 points)" : 0.5
    "Monitoring system (0.5 points)" : 0.5
    "Server-Side Rendering (SSR) Integration (0.5 points)" : 0.5
    "Server-Side Pong (1 point)" : 1

```