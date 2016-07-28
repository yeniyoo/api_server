from django.contrib import admin

from .models import BackgroundImage
from .models import Comment
from .models import Pick
from .models import Round


# Define ModelAdmins
class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image", ]
    list_display_links = ["id", ]


class RoundAdmin(admin.ModelAdmin):
    list_display = ["id", "question", ]
    list_display_links = ["question", ]

# Register your models here.
admin.site.register(BackgroundImage, BackgroundImageAdmin)
admin.site.register(Comment)
admin.site.register(Round, RoundAdmin)
admin.site.register(Pick)
