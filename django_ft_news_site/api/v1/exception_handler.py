from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .views import create_error_response


def ft_news_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.
    """

    if isinstance(exc, AuthenticationFailed):
        data = create_error_response(
            {"invalid_credentials": "Unable to login with provided credentials"})
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, exceptions.APIException):
        data = create_error_response({"Msg": exc.detail})
        return Response(data)

    return None
