from django.core import mail

from notifications.enums import NotificationType
from notifications.models import NotificationTemplate
from signups.tests.factories import SignupFactory
from signups.utils import localize_datetime


def test_signup_creation_email(user, signup_target, settings):
    settings.DEFAULT_FROM_EMAIL = 'noreply@foo.bar'

    NotificationTemplate.objects.language('fi').create(
        type=NotificationType.SIGNUP_CREATED,
        subject="test subject, {{ user__first_name }} {{ user__last_name }} {{ created_at }}",
        html_body="test <b>html body</b>, {{ user__first_name }} {{ user__last_name }} {{ created_at }}",
        text_body="test text body, {{ user__first_name }} {{ user__last_name }} {{ created_at }}"
    )

    signup = SignupFactory(user=user, target=signup_target)

    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    subject = message.subject
    text_body = message.body
    html_body = next(a[0] for a in message.alternatives if a[1] == 'text/html')

    assert message.to == [user.email]
    assert message.from_email == 'noreply@foo.bar'
    assert 'test subject' in subject
    assert 'test text body' in text_body
    assert 'test <b>html body</b>' in html_body

    for field in (subject, text_body, html_body):
        assert user.first_name in field
        assert user.last_name in field
        assert localize_datetime(signup.created_at) in field
