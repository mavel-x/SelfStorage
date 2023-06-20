from django.contrib import admin
from django.utils.safestring import mark_safe

from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'phone',
        'preview',
    )
    list_per_page = 20
    readonly_fields = ('preview',)

    @admin.display(description='Превью аватара')
    def preview(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" style="max-height: 100px;">'
            )
