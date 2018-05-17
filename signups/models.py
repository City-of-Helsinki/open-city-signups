from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class SignupTarget(models.Model):
    identifier = models.CharField(max_length=100, verbose_name=_('identifier'), unique=True)
    name = models.CharField(max_length=100, verbose_name=_('name'))
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('users'), related_name='signup_targets', through='Signup'
    )

    class Meta:
        verbose_name = _('sign-up target')
        verbose_name_plural = _('sign-up targets')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Signup(models.Model):
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, editable=False)
    cancelled_at = models.DateTimeField(verbose_name=_('cancelled at'), null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name='signups', on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        SignupTarget, verbose_name=_('target'), related_name='signups', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('sign-up')
        verbose_name_plural = _('sign-ups')
        ordering = ('id',)

    def __str__(self):
        text = '{} {} {}'.format(self. user, self.target, self.created_at.replace(microsecond=0))
        if self.cancelled_at:
            text = '{} cancelled {}'.format(text, self.cancelled_at.replace(microsecond=0))
        return text
