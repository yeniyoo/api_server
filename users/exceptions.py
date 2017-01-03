from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    """
    model instance를 생성하는 로직에서 에러가 발생하는 경우에 사용한다.
    적절한 detail 문자열을 생성자에 넣어준다.
    """
    status_code = 400
