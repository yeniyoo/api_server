from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import UserSerializer
from .serializers import TokenSerializer
from .models import MyUser
from utils import createResponseData, fbGraphApi


@api_view(['POST'])
def facebookAuth(request):
    if request.method == 'POST':
        try:  # request data check
            access_token = request.data['access_token']
        except:
            return Response(createResponseData(1, "Invalid parameter", None),
                            status=status.HTTP_400_BAD_REQUEST)
        fb_info = fbGraphApi(access_token)
        if 'id' in fb_info:
            user = MyUser.objects.filter(fb_id=fb_info['id'], is_active=1)
            if not user:
                # 회원가입
                fb_info['gender'] = True if (fb_info['gender'] == 'male') else False
                fb_info['fb_id'] = fb_info.pop('id')  # insert serializer
                serializer = UserSerializer(data=fb_info)
                if serializer.is_valid():
                    user = MyUser.objects.filter(fb_id=serializer.save(), is_active=1)
                else:
                    return Response(
                        createResponseData(1, "server error", None),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            # 로그인
            token = Token.objects.get_or_create(user=user[0])
            Token.objects.filter(key=token[0]).delete()  # 토큰이 새로 생성되던 기존에 존재하던 한번 지우고
            token = Token.objects.create(user=user[0])  # 새로운 토큰을 부여함. (로그인 할때마다 재생성)
            return Response(headers={"auth-token": str('Token ' + str(token))})
        else:
            return Response(
                createResponseData(1, "incorrect access_token", None),
                status=status.HTTP_403_FORBIDDEN
            )


class UserDetail(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@api_view(['GET', 'POST', 'PATCH'])
@authentication_classes([TokenAuthentication, ])
def users(request):
    if request.method == 'POST':
        # TokenSerializer가 로직을 담당한다.
        # HTTP Response header에 auth_token: token를 넣은 뒤 반환한다.
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.save()
        return Response(status=status.HTTP_201_CREATED, headers={'auth-token': key})
    else:
        return UserDetail.as_view()(request)
