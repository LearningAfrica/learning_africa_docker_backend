from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_message = extract_error_message(response.data)
        if error_message:
            custom_error_message = {'detail': error_message}
            response = Response(custom_error_message, status=response.status_code)
    return response

def extract_error_message(data):
    for key, value in data.items():
        if isinstance(value, list):
            error_message = ", ".join(value)
            return error_message
        elif isinstance(value, str):
            return value
    return None