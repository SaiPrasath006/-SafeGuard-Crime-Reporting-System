# Online Crime Reporting System: Technology Stack

This document provides a comprehensive overview of the technologies used in the development and deployment of the Online Crime Reporting System.

## 1. Backend Engine (Server-Side)
- **Programming Language**: **Python 3.10.12** - Chosen for its readability, vast library support, and efficiency in handling backend logic.
- **Web Framework**: **Flask** - A micro-framework that provides the core routing and request handling capabilities without unnecessary overhead.
- **RESTful API**: Designed to ensure seamless communication between the frontend interface and the backend server.
- **Process Manager**: **Gunicorn** - A production-grade WSGI HTTP Server used to handle multiple concurrent user requests reliably.

## 2. Frontend Interface (Client-Side)
- **Core Structure**: **HTML5** - Provides semantic structure for the web pages.
- **Styling**: **CSS3** - Implements a modern **Glassmorphism** design language using custom CSS variables, backdrop filters, and smooth transitions for a premium user experience.
- **Interactivity**: **Vanilla JavaScript (ES6+)** - Used for dynamic content updates, form validation, and asynchronous API calls without the need for heavy external frameworks.
- **Iconography**: **Lucide Icons** - Used for consistent, modern visual elements across the UI.

## 3. Database & Data Infrastructure
- **Database Engine**: **SQLite** - A self-contained, serverless relational database engine used for efficient storage of user data and crime reports.
- **ORM**: **SQLAlchemy** - Provides an Object-Relational Mapping (ORM) layer, allowing Pythonic interaction with the database and ensuring data integrity.
- **File Storage**: **Local Filesystem** - Used for storing uploaded evidence (images/videos) associated with crime reports.

## 4. Security & Authentication
- **Session Management**: **JWT (JSON Web Tokens)** - Implements secure, stateless authentication for both citizens and administrators.
- **Password Protection**: **Bcrypt** - Industry-standard hashing algorithm used to securely store user credentials.
- **Middleware**: Custom Python decorators for protected route access and role-based authorization.
- **CORS Policy**: Configured to manage cross-origin requests securely between the client and server.

---
**Online Crime Reporting System © 2026**
