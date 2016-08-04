from random import randint

from django.conf import settings
from django.db import models
from django.db.models import Max


# 닉네임 저장소
class Nickname(models.Model):
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.nickname


class BackgroundImage(models.Model):
    image = models.CharField(max_length=300)  # image name
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.image


class RoundManager(models.Manager):
    # Round 테이블에서 임의의 레코드를 하나 반환
    # queryset이 아니라 Round 인스턴스 자체를 반환함에 유의
    def get_random(self):
        candidate = self.get_queryset().filter(is_active=True, complete=False)
        count = candidate.count()
        # count = 0으로 유효한 라운드가 존재하지 않을 경우의 에러처리가 필요함
        index = randint(0, count-1)
        random_obj = candidate[index]
        return random_obj


class Round(models.Model):
    question = models.CharField(max_length=1000)  # 질문
    complete = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    complete_date = models.DateTimeField(null=True, default=None)  # 종료일
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    background_id = models.ForeignKey(BackgroundImage)

    objects = RoundManager()

    def __str__(self):
        return str(self.id)

    # 해당 Round를 Pick한 User의 숫자를 반환
    def get_member(self):
        return self.pick_set.count()


class PickManager(models.Manager):
    def next_nickname_id(self, round_id):
        # 해당 round의 pick들만 선택
        picks = self.get_queryset().filter(round_id=round_id)
        print(round_id)
        # 가장 큰 nickname(=가장 최근) pick를 선택
        max_nickname_pick = picks.aggregate(Max('nickname_id'))
        print(max_nickname_pick)
        # pick이 없다면 1, 존재한다면 해당 pick의 nickname id값에 1을 더해서 반환
        max_nickname_id = 0 if max_nickname_pick['nickname_id__max'] is None \
            else int(max_nickname_pick['nickname_id__max'])
        return max_nickname_id + 1


class Pick(models.Model):
    yes_no = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # MyUser, Round 레코드가 삭제될 경우 Pick 레코드도 삭제되어야 한다
    # 그러니 on_delete = models.CASCADE 옵션을 추가해줘야 할 것
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    round = models.ForeignKey(Round)
    # RoundNickname model을 제거하고, Pick에 nickname field를 추가
    nickname = models.ForeignKey(Nickname)

    objects = PickManager()

    class Meta:
        unique_together = ('user', 'round')

    def __str__(self):
        return str(self.id)

    def get_username(self):
        return self.user.fb_id


class Comment(models.Model):
    content = models.CharField(max_length=500)
    like = models.IntegerField(default=0)  # 좋아요 갯수
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    pick = models.ForeignKey(Pick)
    # default 값을 None으로 주려면 null=True가 필요
    # admin site에서 Comment를 조작하기 위해서는 blank=True가 필요
    parent = models.ForeignKey("self", null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)

    def get_user(self):
        return str(self.pick.user)

    def get_round(self):
        return str(self.pick.round)


class CommentLike(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.ForeignKey(Comment)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return str(self.id)
