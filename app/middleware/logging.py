"""
Request logging middleware
"""

import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.utils.logger import log_request


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests in development mode"""
    
    async def dispatch(self, request: Request, call_next):
        if not settings.DEBUG:
            return await call_next(request)
        
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Log the request
        log_request(
            method=request.method,
            url=str(request.url),
            response_time=response_time
        )
        
        return response
