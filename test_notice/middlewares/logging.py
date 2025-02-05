import json
from datetime import datetime
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from test_notice.logger import LoggerClient


class ActionLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger_client = LoggerClient(__name__)
        method = request.method
        path = request.url.path
        body = None

        if request.method in {"POST", "PUT", "PATCH"}:
            body = await request.body()
            try:
                body = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError:
                body = None

        response = await call_next(request)

        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": method,
            "path": path,
            "status_code": response.status_code,
            "body": body
        }

        logger_client.logger.info(json.dumps(log_data, ensure_ascii=False))
        return response