from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .exceptions import BadRequestException
from .models import MyUser
from .utils import get_facebook_info


# 추후 다른 SNS를 통한 auth를 구현할 경우를 대비
service_choices = [
    "facebook",
]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = MyUser
        fields = ("fb_id", "gender", "age", "password", )


class TokenSerializer(serializers.Serializer):
    service = serializers.ChoiceField(choices=service_choices)
    access_token = serializers.CharField()

    def create(self, validated_data):
        service = validated_data["service"]
        access_token = validated_data["access_token"]

        # Graph API에 요청해서 Facebook info를 받아온다.
        # 받아온 id 값의 User가 이미 존재하는지 확인한다.
        # 존재한다면, Token만 새로만들어서 반환한다.
        # 존재하지 않는다면, User도 만들고, Token도 만들어서 key 값을 반환한다.

        if service == "facebook":
            try:
                # Graph API에서 정보를 받아오고, MyUser에 맞춰 적절히 손질
                facebook_info = get_facebook_info(access_token)
                facebook_info["fb_id"] = facebook_info.pop("id")
                facebook_info["gender"] = True if facebook_info.pop("gender") == "male" else False

                # facebook id 값으로 확인해서 이미 존재하는 유저라면 Token 재생성
                # 존재하지 않는 유저라면 User, Token 생성
                user = MyUser.objects.get_or_create(**facebook_info)[0]
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)

                return token.key
            except KeyError:
                # invalid access token 케이스의 에러처리
                raise BadRequestException("access_token is invalid.")
