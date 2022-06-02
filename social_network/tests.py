from django.test import TestCase
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from factory import Faker, Sequence


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('last_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Sequence(lambda n: 'person{}@example.com'.format(n))
