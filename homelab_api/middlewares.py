import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware

from homelab_api.loggings import get_logger

logger = get_logger('http')


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        log_id = str(uuid4())

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(f'[bold red]Unhandled Exception[/] id={log_id} {request.method} {request.url}')
            raise

        elapsed = time.perf_counter() - start

        response.headers['X-Process-Time'] = f'{elapsed:.3f}'

        logger.info(
            f'[cyan]{request.method:<6}[/] '
            f'[green]{response.status_code}[/] '
            f'[yellow]{elapsed:.3f}s[/] '
            f'{request.url} '
            f'[dim]id={log_id}[/]'
        )

        return response
