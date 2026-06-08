from rest_framework import status
from rest_framework.exceptions import APIException


class ProtectedDeleteError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Dit object kan niet worden verwijderd, omdat het nog wordt gebruikt.'
    default_code = 'protected_delete'
