from django.contrib import admin
from django.contrib.auth import get_user_model

from signups.models import Signup

User = get_user_model()


class SignupInline(admin.TabularInline):
    model = Signup
    fields = ('target', 'created_at', 'cancelled_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (SignupInline,)
