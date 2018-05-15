import factory
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from signups.models import Signup, SignupTarget

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker('uuid4')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    class Meta:
        model = User


class SignupTargetFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('bs')
    identifier = factory.LazyAttribute(lambda o: slugify(o.name))

    class Meta:
        model = SignupTarget


class SignupFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    target = factory.SubFactory(SignupTargetFactory)

    class Meta:
        model = Signup
