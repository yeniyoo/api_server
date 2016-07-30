from django.contrib import admin

from .models import BackgroundImage
from .models import Comment
from .models import Pick
from .models import Round
from .models import RoundNickname


# Define ModelAdmins
class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", ]
    list_display_links = ["id", ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["get_user_id", "get_round_id", "pick_id", "id", "content", ]
    list_display_links = ["content", ]


class PickAdmin(admin.ModelAdmin):
    list_display = ["id", "get_username", "round_id"]


class RoundAdmin(admin.ModelAdmin):
    list_display = ["id", "question", ]
    list_display_links = ["question", ]

# Register your models here.
admin.site.register(BackgroundImage, BackgroundImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(RoundNickname)
