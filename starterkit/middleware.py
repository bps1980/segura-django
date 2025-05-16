import logging

logger = logging.getLogger(__name__)

class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        path = request.get_full_path()
        logger.warning(f"[REQUEST] IP: {ip} | PATH: {path}")
        return self.get_response(request)
