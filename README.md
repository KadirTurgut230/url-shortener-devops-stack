URL SHORTENER DEVOPS STACK

A high-performance, containerized URL shortener platform with asynchronous analytics processing. Developed as a comprehensive DevOps and backend architecture demonstration.

OVERVIEW
This project is a fully Dockerized URL shortener that handles redirection and tracks click analytics in real-time. To ensure high availability and low latency, it utilizes Redis for caching and RabbitMQ for asynchronous event processing, preventing database I/O bottlenecks during peak traffic.

ARCHITECTURE
- API (FastAPI): Handles URL creation and HTTP 302 redirections.
- Cache (Redis): Stores short codes and original URLs for ultra-fast routing.
- Message Broker (RabbitMQ): Queues click events asynchronously without blocking the main API thread.
- Worker (Python): Consumes queued click events, parses user agents, and writes analytics to the database.
- Database (PostgreSQL): Persists URL mappings and detailed analytics (device type, country, timestamp).
- Reverse Proxy (Nginx): Routes incoming external traffic safely to the internal API.
- Monitoring (Grafana): Visualizes click analytics and system health metrics.

TECH STACK
- Backend: Python, FastAPI
- Data and Message Brokers: PostgreSQL, Redis, RabbitMQ
- Infrastructure and DevOps: Nginx, Docker, Docker Compose
- Observability: Grafana

QUICK START

Prerequisites:
- Docker
- Docker Compose

Installation and Run:
1. Open your terminal and navigate to the project directory.
2. Build and start the services in the background:
   docker compose up -d
3. The API will be available at http://localhost.

MONITORING
Grafana is pre-configured to visualize real-time click analytics (Country and Device Type distributions).
- Dashboard URL: http://localhost:3000
- Default Credentials: admin / admin

GRACEFUL SHUTDOWN
To cleanly stop all services and remove the network without losing database volumes:
docker compose down

To completely reset the project (including all database and queue records):
docker compose down -v
