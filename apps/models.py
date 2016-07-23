from django.db import models
from users.models import MyUser


# 닉네임 저장소
class Nickname(models.Model):
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname


class BackgroundImage(models.Model):
    image = models.CharField(max_length=300)  # 이미지 path
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image


class Round(models.Model):
    question = models.CharField(max_length=1000)  # 질문
    complete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    complete_date = models.DateTimeField(null=True, default=None)  # 종료일
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(MyUser)
    background_id = models.ForeignKey(BackgroundImage)

    def __str__(self):
        return self.id


class RoundNickname(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(MyUser)
    round_id = models.ForeignKey(Round)
    nickname_id = models.ForeignKey(Nickname)

    class Meta:
        unique_together = ('user_id', 'round_id')

    def __str__(self):
        return self.nickname_id.nickname


class Pick(models.Model):
    yes_no = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_id = models.ForeignKey(MyUser)
    round_id = models.ForeignKey(Round)

    def __str__(self):
        return self.yes_no


class Comment(models.Model):
    content = models.CharField(max_length=500)
    like = models.IntegerField(default=0)  # 좋아요 갯수
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    pick_id = models.ForeignKey(Pick)
    comment_id = models.ForeignKey("self", null=True, default=None)

    def __str__(self):
        return self.id


class CommentLike(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(MyUser)
    comment_id = models.ForeignKey(Comment)

    class Meta:
        unique_together = ('user_id', 'comment_id')

    def __str__(self):
        return self.user_id