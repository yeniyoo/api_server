from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Pick
from .models import Round
from .models import Comment


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
    member = serializers.IntegerField(source="get_member")

    class Meta:
        model = Round
        fields = ("id", "question", "create_date", "complete", "member", )


class PickSerializer(serializers.ModelSerializer):
    yes_no = serializers.NullBooleanField(required=True)

    class Meta:
        model = Pick
        fields = ("yes_no", "round_id", )


class CommentSerializer(serializers.ModelSerializer):

    # http://www.django-rest-framework.org/api-guide/fields/#serializermethodfield 참고
    # read_only field
    is_liked = serializers.SerializerMethodField(method_name="like_or_not")

    class Meta:
        model = Comment
        fields = ("id", "content", "like", "is_liked", "create_date", )
        read_only_fields = ("id", "like", "is_liked", "create_date", )

    def like_or_not(self, obj):
        user_id = self.context.get("request").user.id
        try:
            obj.commentlike_set.get(user_id=user_id)
            return True
        except ObjectDoesNotExist:
            return False

    # Pick하지 않은 유저가 요청했을 경우에는 어떻게 처리하면 좋을까?
    # 1) get_object_or_404 메소드를 사용해서 404 Response를 발생
    # 2) 에러 핸들링 로직을 기술해서 유효한 에러 메시지를 담아서 반환
    def create(self, validated_data):
        comment = Comment(**validated_data)

        # Generic View가 Serializer를 사용할때, context를 채워준다.
        # 필요한 정보들을 얻을 수 있다.
        # http://stackoverflow.com/questions/14921552/rest-framework-serializer-method
        user_id = self.context.get("request").user.id
        round_id = int(self.context.get("view").kwargs["round_id"])
        pick_id = Pick.objects.get(user_id=user_id, round_id=round_id)

        comment.pick_id = pick_id
        comment.save()
        return comment


class RecommentSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(method_name="like_or_not")

    class Meta:
        model = Comment
        fields = ("id", "content", "like", "is_liked", "create_date", "comment_id")
        read_only_fields = ("id", "like", "is_liked", "create_date", )

    def like_or_not(self, obj):
        user_id = self.context.get("request").user.id
        try:
            obj.commentlike_set.get(user_id=user_id)
            return True
        except ObjectDoesNotExist:
            return False

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment_id = int(self.context.get("view").kwargs["comment_id"])
        pick_id = Comment.objects.get(id=comment_id).pick_id

        comment.pick_id = pick_id
        comment.comment_id_id = comment_id
        comment.save()
        return comment