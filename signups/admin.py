import datetime

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .exports import export_participants_as_csv
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
    actions = ["export_participants"]

    def export_participants(self, request, queryset):
        if queryset.count() > 1:
            return self.message_user(
                request,
                _(u"Choose only one Signup Target"),
                messages.ERROR
            )

        signup_target = queryset.first()
        participants = signup_target.users\
            .filter(signups__cancelled_at=None).distinct()
        filename = signup_target.identifier + \
            "_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename
        export_participants_as_csv(participants, response)
        return response
    export_participants.short_description = _("Download participants' list in CSV format")
