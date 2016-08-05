from rest_framework.exceptions import APIException


class NoYesOrNoException(APIException):
    status_code = 400
    default_detail = "yes_no parameter is required."
