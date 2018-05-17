from django.contrib import admin

from .models import Signup, SignupTarget


class SignupInline(admin.TabularInline):
    model = Signup
    fields = ('user', 'target', 'created_at', 'cancelled_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('user', 'target', 'created_at', 'cancelled_at')
    fields = ('user', 'target', 'created_at', 'cancelled_at')
    readonly_fields = ('created_at',)


@admin.register(SignupTarget)
class SignupTargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier')
    fields = ('name', 'identifier')
    prepopulated_fields = {'identifier': ('name',)}
    inlines = (SignupInline,)
