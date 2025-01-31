import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException, ValidationError, NotAuthenticated, AuthenticationFailed, NotFound

logger = logging.getLogger(__name__)

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except ValidationError as e:
            return self.handle_exception(e, status=400, message="Validation error")
        except NotAuthenticated as e:
            return self.handle_exception(e, status=401, message="User not authenticated")
        except AuthenticationFailed as e:
            return self.handle_exception(e, status=403, message="Authentication failed")
        except PermissionDenied as e:
            return self.handle_exception(e, status=403, message="Permission denied")
        except NotFound as e:
            return self.handle_exception(e, status=404, message="Resource not found")
        except Http404 as e:
            return self.handle_exception(e, status=404, message="Page not found")
        except APIException as e:
            return self.handle_exception(e, status=500, message="API exception occurred")
        except Exception as e:
            return self.handle_exception(e, status=500, message="Internal server error", log_traceback=True)

    def handle_exception(self, exception, status=500, message="An error occurred", log_traceback=False):
        if log_traceback:
            logger.error(f"Unhandled exception: {str(exception)}\n{traceback.format_exc()}")
        else:
            logger.warning(f"Exception: {str(exception)}")

        return JsonResponse({
            "success": False,
            "error": {
                "type": exception.__class__.__name__,
                "message": str(exception),
                "detail": message
            }
        }, status=status)
