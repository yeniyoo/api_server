from django.contrib import admin

from .models import Round, BackgroundImage


# Define ModelAdmins
class BackgroundImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image"]
    list_display_links = ['image']

# Register your models here.
admin.site.register(BackgroundImage, BackgroundImageAdmin)
