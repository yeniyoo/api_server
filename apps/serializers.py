from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from .models import Pick
from .models import Round
from .models import RoundNickname
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
    # method_name 값을 설정하지 않으면, default로 get_nickname을 호출
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "nickname", "content", "like", "is_liked", "create_date", )
        read_only_fields = ("id", "like", "is_liked", "create_date", )

    def like_or_not(self, obj):
        user_id = self.context.get("request").user.id
        try:
            obj.commentlike_set.get(user_id=user_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_nickname(self, obj):
        # obj(Comment)의 정보를 가지고 대응되는 RoundNickname 인스턴스를 검색
        pick_id = obj.pick_id
        roundnickname = RoundNickname.objects.get(user_id=pick_id.user_id, round_id=pick_id.round_id)
        return roundnickname.nickname_id.nickname

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
        # Pick 레코드가 존재하지 않는 경우에 대한 에러 처리 필요함.
        # get_object_or_404 메소드를 사용하는 방법이 하나 있겠음.
        pick_id = Pick.objects.get(user_id=user_id, round_id=round_id)

        comment.pick_id = pick_id
        comment.save()
        return comment


class RecommentSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(method_name="like_or_not")
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "nickname", "content", "like", "is_liked", "create_date", "comment_id")
        read_only_fields = ("id", "like", "is_liked", "create_date", )

    def like_or_not(self, obj):
        user_id = self.context.get("request").user.id
        try:
            obj.commentlike_set.get(user_id=user_id)
            return True
        except ObjectDoesNotExist:
            return False

    def get_nickname(self, obj):
        # obj(Comment)의 정보를 가지고 대응되는 RoundNickname 인스턴스를 검색
        pick_id = obj.pick_id
        roundnickname = RoundNickname.objects.get(user_id=pick_id.user_id, round_id=pick_id.round_id)
        return roundnickname.nickname_id.nickname

    def create(self, validated_data):
        comment = Comment(**validated_data)
        comment_id = int(self.context.get("view").kwargs["comment_id"])

        # 1) Comment에서 해당 댓글의 pick_id를 얻은 후, Pick에서 round_id를 구함.
        # 2) user_id와 round_id를 통해서 대댓글을 남기는 사람의 pick_id 정보를 이용
        comment_pick_id = Comment.objects.get(id=comment_id).pick_id_id
        round_id = Pick.objects.get(id=comment_pick_id).round_id
        user_id = self.context.get("request").user.id
        pick_id = Pick.objects.get(user_id=user_id, round_id=round_id)

        comment.pick_id = pick_id
        comment.comment_id_id = comment_id
        comment.save()
        return comment