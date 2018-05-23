from django.utils.translation import ugettext_lazy as _
from enumfields import Enum


class NotificationType(Enum):
    SIGNUP_CREATED = 'signup_created'

    class Labels:
        SIGNUP_CREATED = _('Sign-up created')
