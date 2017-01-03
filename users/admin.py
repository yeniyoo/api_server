from django.contrib import admin

from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MyUserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["password"].required = False
        return form

# Register your models here.
admin.site.register(MyUser, MyUserAdmin)