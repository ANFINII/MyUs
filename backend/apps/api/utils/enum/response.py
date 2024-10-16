from enum import Enum

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from apps.api.utils.functions.index import message


class ApiResponse(Enum):
    unauthorized = (True, 'Un Authorized', HTTP_401_UNAUTHORIZED)
    not_found = (True, 'Not Found', HTTP_404_NOT_FOUND)

    def run(self):
        is_error, content, status_code = self.value
        return Response(message(is_error, content), status=status_code)
