from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import redis.asyncio as redis

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, max_requests: int = 5, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis = redis.from_url(redis_url, decode_responses=True)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        try:
            # Increment the request count
            current_count = await self.redis.incr(key)

            if current_count == 1:
                # Set TTL (time to live) for key when it's first created
                await self.redis.expire(key, self.window_seconds)

            if current_count > self.max_requests:
                ttl = await self.redis.ttl(key)
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Too Many Requests",
                        "retry_after_seconds": ttl
                    }
                )
        except Exception as e:
            # Fail-open: in case Redis fails, allow the request
            print(f"Rate limiting failed: {e}")

        # Proceed to actual route handler
        response = await call_next(request)
        return response

