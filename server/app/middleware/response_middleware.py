"""
Middleware for formatting all responses into a single template
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json
from datetime import datetime


class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    """Middleware for formatting all responses into a single template"""

    async def dispatch(self, request: Request, call_next):
        # Process the request
        response = await call_next(request)

        # Skip static files
        if request.url.path.startswith("/media") or request.url.path.startswith("/static"):
            return response

        # Skip non-JSON responses
        if response.headers.get("content-type") != "application/json":
            return response

        # Get response body
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        try:
            response_data = json.loads(body.decode())
        except:
            return response

        # If already formatted - skip
        if isinstance(response_data, dict) and "status_code" in response_data:
            return JSONResponse(
                status_code=response_data.get("status_code", response.status_code),
                content=response_data
            )

        # Determine access status
        access_status = request.headers.get("X-Access-Status", "granted")

        # Format response based on HTTP status
        if 200 <= response.status_code < 300:
            formatted = {
                "status_code": response.status_code,
                "status": "success" if response.status_code == 200 else "created",
                "access_status": access_status,
                "message": response_data.get("message", "Operation successful") if isinstance(response_data, dict) else "Operation successful",
                "timestamp": datetime.utcnow().isoformat(),
                "data": response_data if response_data else None,
                "errors": None
            }
        elif response.status_code == 400:
            formatted = {
                "status_code": 400,
                "status": "bad_request",
                "access_status": "denied",
                "message": response_data.get("detail", "Bad request") if isinstance(response_data, dict) else "Bad request",
                "timestamp": datetime.utcnow().isoformat(),
                "data": None,
                "errors": response_data.get("errors") if isinstance(response_data, dict) else None
            }
        elif response.status_code == 401:
            formatted = {
                "status_code": 401,
                "status": "unauthorized",
                "access_status": "missing",
                "message": response_data.get("detail", "Authentication required") if isinstance(response_data, dict) else "Authentication required",
                "timestamp": datetime.utcnow().isoformat(),
                "data": None,
                "errors": None
            }
        elif response.status_code == 403:
            formatted = {
                "status_code": 403,
                "status": "forbidden",
                "access_status": "denied",
                "message": response_data.get("detail", "Access forbidden") if isinstance(response_data, dict) else "Access forbidden",
                "timestamp": datetime.utcnow().isoformat(),
                "data": None,
                "errors": None
            }
        elif response.status_code == 404:
            formatted = {
                "status_code": 404,
                "status": "not_found",
                "access_status": "granted",
                "message": response_data.get("detail", "Resource not found") if isinstance(response_data, dict) else "Resource not found",
                "timestamp": datetime.utcnow().isoformat(),
                "data": None,
                "errors": None
            }
        else:
            formatted = {
                "status_code": response.status_code,
                "status": "error",
                "access_status": "denied",
                "message": response_data.get("detail", "Internal server error") if isinstance(response_data, dict) else "Internal server error",
                "timestamp": datetime.utcnow().isoformat(),
                "data": None,
                "errors": response_data.get("errors") if isinstance(response_data, dict) else None
            }

        return JSONResponse(
            status_code=formatted["status_code"],
            content=formatted
        )