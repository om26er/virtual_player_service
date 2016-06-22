from django.contrib import admin
from django.contrib.auth.models import Group

from player.models import User


class UserAdmin(admin.ModelAdmin):
    fields = (
        'is_active',
        'email',
        'password',
        'first_name',
        'last_name',
        'school',
    )

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
