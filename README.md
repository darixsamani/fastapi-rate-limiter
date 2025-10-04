# FastAPI Rate Limiter Middleware

## Project Description

This project implements a **Rate Limiting Middleware** for a FastAPI application. The middleware restricts how many requests a client (identified by IP address) can make within a defined time window. It helps protect your API from abuse, excessive traffic, and denial-of-service (DoS) attacks by throttling requests at the middleware level before they reach the main application logic.

---

## Key Features

- 🔒 **Per-IP Rate Limiting**: Limits each unique IP address to a fixed number of requests within a given time window.
- ⏱️ **Configurable Limits**: Easily set the number of allowed requests and time window (e.g., 5 requests per 60 seconds).
- 🧠 **Smart Storage with Redis**: Uses Redis to efficiently store and manage request counters with TTL (time-to-live).
- 📉 **Fail-Open Strategy**: If Redis is unavailable, the middleware gracefully lets requests through to avoid blocking legitimate users.
- 🔄 **Auto Reset**: Counters reset automatically after the time window expires.
- 📦 **Reusable Component**: Designed as a plug-and-play middleware class for any FastAPI project.

---

## How It Works

1. When a request comes in, the middleware checks the client’s IP address.
2. It creates or updates a Redis key that tracks the number of requests from that IP.
3. If the request count exceeds the allowed limit:
   - The request is rejected with HTTP `429 Too Many Requests`.
   - A message is returned including the `retry_after_seconds` field indicating how long to wait before retrying.
4. If under the limit, the request proceeds normally to the API endpoint.

---

## Tech Stack

| Technology  | Purpose                              |
|-------------|--------------------------------------|
| **FastAPI** | Web framework for building APIs      |
| **Redis**   | In-memory data store for counters    |
| **Uvicorn** | ASGI server to run the FastAPI app   |
| **Starlette** | Base for FastAPI and middleware     |

---

## Example


```python
# main.py
from fastapi import FastAPI
from fastapi_rate_limiter import RateLimiterMiddleware

app = FastAPI()

# Add middleware with Redis URL
app.add_middleware(
    RateLimiterMiddleware,
    redis_url="redis://localhost:6379",  # Adjust to your Redis config
    max_requests=5,
    window_seconds=60
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

```
