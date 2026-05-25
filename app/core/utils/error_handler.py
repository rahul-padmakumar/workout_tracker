def drf_exception_handler(exc, context):
    """Custom exception handler for DRF to return consistent error responses"""
    from rest_framework.views import exception_handler
    from .base_response import ErrorResponse

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the error response format
        return ErrorResponse(
            errors=_get_error_message(response.data),
            status_code=response.status_code
        )

    return response

def _get_error_message(exc):
    print(f"Extracting error message from: {exc}")
    if isinstance(exc, (dict)):
        print(f"Error detail found: {exc.get('detail', str(exc))}")
        return exc.get('detail', str(exc))
    return str(exc)