from rest_framework import serializers

from .models import Round, Pick


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ("question", "background_id", )

    # user_id field를 서버에서 채워줘야하므로 ModelSerializer의 create 메소드를 오버라이딩
    def create(self, validated_data):
        round = Round(**validated_data)
        # request context의 user에 접근
        # http://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        round.user_id = user
        round.save()
        return round


# GET method 사용만 고려해서 설계
class MyRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ("id", "question", "create_date", "complete", )


class PickSerializer(serializers.ModelSerializer):
    yes_no = serializers.NullBooleanField(required=True)

    class Meta:
        model = Pick
        fields = ("yes_no", "round_id", )