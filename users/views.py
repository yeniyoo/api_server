from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from utils import createResponseData, fbGraphApi
from users.serializers import UserSerializers
from users.models import MyUser


@api_view(['POST'])
def facebookAuth(request):
    if request.method == 'POST':
        access_token = request.POST['access_token']
        fb_info = fbGraphApi(access_token)
        if 'id' in fb_info:
            user = MyUser.objects.filter(fb_id=fb_info['id'], is_active=1)
            if not user:
                # 회원가입
                fb_info['gender'] = True if (fb_info['gender'] == 'male') else False
                fb_info['fb_id'] = fb_info.pop('id')  # insert serializer
                serializer = UserSerializers(data=fb_info)
                if serializer.is_valid():
                    user = MyUser.objects.filter(fb_id=serializer.save(), is_active=1)
                else:
                    return Response(
                        createResponseData(1, "server error", None),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            # 로그인
            # TODO: 토큰값이 고정됨. 뭔가 solt값이나 다른 방식이 필요
            token = Token.objects.update_or_create(user=user[0])
            return Response(createResponseData(0, "success", None), headers={"auth-token": token[0]})
        else:
            return Response(
                createResponseData(1, "incorrect access_token", None),
                status=status.HTTP_403_FORBIDDEN
            )


@api_view(['PUT'])
def ageSetting(request):
    if request.method == 'PUT':  # 더미
        return Response(createResponseData(0, "success", None))


"""
* My Round
"""
@api_view(['GET'])
def myOpenRound(request):
    if request.method == 'GET':  # 더미
        data = [
            {"id": 1, "question": "불라불라", "create_date": "2017-07-25", "member": 130, "complete": 0},
            {"id": 2, "question": "불라불라1234", "create_date": "2017-07-25", "member": 10, "complete": 2}
        ]
        return Response(createResponseData(0, "success", data))