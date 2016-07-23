from rest_framework import serializers
from users.models import MyUser


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(required=False)

    class Meta:
        model = MyUser
        field = ('fb_id', 'gender')