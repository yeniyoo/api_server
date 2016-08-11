from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Pick
from .models import Round
from .models import Comment
from .models import CommentLike


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ("question", "background_id", )

    # user field를 서버에서 채워줘야하므로 ModelSerializer의 create 메소드를 오버라이딩
    def create(self, validated_data):
        round = Round(**validated_data)
        # request context의 user에 접근
        # http://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        round.user = user
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
        fields = ("yes_no", "round", )


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
        user = self.context.get("request").user
        try:
            obj.commentlike_set.get(user=user)
            return True
        except ObjectDoesNotExist:
            return False

    def get_nickname(self, obj):
        # obj(Comment)의 정보를 가지고 nickname 값을 반환
        return obj.pick.nickname.nickname

    # Pick하지 않은 유저가 요청했을 경우에는 어떻게 처리하면 좋을까?
    # 1) get_object_or_404 메소드를 사용해서 404 Response를 발생
    # 2) 에러 핸들링 로직을 기술해서 유효한 에러 메시지를 담아서 반환
    def create(self, validated_data):
        comment = Comment(**validated_data)

        # Generic View가 Serializer를 사용할때, context를 채워준다.
        # 필요한 정보들을 얻을 수 있다.
        # http://stackoverflow.com/questions/14921552/rest-framework-serializer-method
        user = self.context.get("request").user
        round_id = int(self.context.get("view").kwargs["round_id"])
        try:
            pick = Pick.objects.get(user=user, round_id=round_id)
            comment.pick = pick
            comment.save()
            return comment
        except ObjectDoesNotExist:
            raise NotFound("Please, pick round first before requesting comments.")


class RecommentSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(method_name="like_or_not")
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "nickname", "content", "like", "is_liked", "create_date", "parent")
        read_only_fields = ("id", "like", "is_liked", "create_date", )

    def like_or_not(self, obj):
        user = self.context.get("request").user
        try:
            obj.commentlike_set.get(user=user)
            return True
        except ObjectDoesNotExist:
            return False

    def get_nickname(self, obj):
        # obj(Comment)의 정보를 가지고 nickname 값을 반환
        return obj.pick.nickname.nickname

    def create(self, validated_data):
        recomment = Comment(**validated_data)
        comment_id = int(self.context.get("view").kwargs["comment_id"])
        comment = Comment.objects.get(id=comment_id)

        # 1) Comment에서 해당 댓글의 pick을 얻은 후, pick에서 round를 구함.
        # 2) user와 round를 통해서 대댓글을 남기는 사람의 pick 정보를 이용
        comment_pick = comment.pick
        comment_round = comment_pick.round
        recomment_user = self.context.get("request").user
        recomment_pick = Pick.objects.get(user=recomment_user, round=comment_round)

        recomment.pick = recomment_pick
        recomment.parent = comment
        recomment.save()
        return recomment


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        exclude = ("user", "comment", )

    # 오버라이딩
    def create(self, validated_data):
        # CommentLike 인스턴스를 생성
        # user 정보는 request에서, comment 정보는 URI pattern에서 획득
        comment_like = CommentLike.objects.create(
            user=self.context.get("request").user,
            comment=Comment.objects.get(id=self.context.get("view").kwargs["comment_id"])
        )
        # 해당 Comment의 like 필드값을 update
        # 더 좋은 SQL 구문 하용을 유도하도록 F expression 사용
        Comment.objects.filter(id=comment_like.comment_id).update(like=F("like") + 1)
        return comment_like
