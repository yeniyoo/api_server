from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin)


class MyUserManager(BaseUserManager):
    # 수정했습니다.
    def create_user(self, fb_id, nickname, password=None):
        if not fb_id:
            raise ValueError('Users must have an fb_id')

        user = self.model(
            fb_id=MyUserManager.normalize_email(fb_id),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fb_id, nickname, password):
        u = self.create_user(fb_id=fb_id,
                             nickname=nickname,
                             password=password,
                             )
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser,  PermissionsMixin):

    # facebook id는 email일 수도 있고, phone number일 수도 있다.
    fb_id = models.CharField(
        verbose_name='fb_id',
        max_length=250,
        unique=True,
    )

    # 혹시몰라서 남겨둔 field 이다.
    # 원칙적으로 nickname은 어떤 round에 참여한 어떤 user마다 매겨진다.
    nickname = models.CharField(
        max_length=10,
        null=True,
        default=None,
        blank=True
    )
    gender = models.BooleanField(default=True)
    age = models.IntegerField(null=True, default=None, blank=True)
    point = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    withdraw_date = models.DateTimeField(null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'fb_id'
    REQUIRED_FIELDS = ['nickname']

    def get_full_name(self):
        # The user is identified by their fb_id
        return self.fb_id

    def get_short_name(self):
        # The user is identified by their fb_id
        return self.fb_id

    def __str__(self):
        return self.fb_id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin