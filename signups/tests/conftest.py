import factory.random
import pytest
from rest_framework.test import APIClient

from signups.tests.factories import SignupFactory, SignupTargetFactory, UserFactory


@pytest.fixture(autouse=True)
def no_more_mark_django_db(transactional_db):
    pass


@pytest.fixture(autouse=True)
def set_random_seed():
    factory.random.reseed_random(777)


@pytest.fixture(autouse=True)
def email_setup(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
    settings.NOTIFICATIONS_ENABLED = True


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_api_client(user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def signup_target():
    return SignupTargetFactory()


@pytest.fixture
def signup(signup_target, user):
    return SignupFactory(user=user, target=signup_target)
