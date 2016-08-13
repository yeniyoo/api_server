from rest_framework import serializers
from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = MyUser
        fields = ("fb_id", "gender", "age", "password", )