from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.enums import NotificationType
from notifications.utils import send_notification
from signups.models import Signup


@receiver(post_save, sender=Signup)
def signup_notification_handler(sender, **kwargs):
    signup = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
        send_notification(signup.user, NotificationType.SIGNUP_CREATED, signup.get_notification_context())


if settings.NOTIFICATIONS_ENABLED:
    post_save.connect(signup_notification_handler, Signup)
