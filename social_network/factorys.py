from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from factory import Faker, Sequence
import factory
from .models import Post


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('last_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Sequence(lambda n: 'person{}@example.com'.format(n))

    @factory.post_generation
    def set_password(obj, *args, **kwargs):
        obj.set_password(obj.username)


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker('last_name')
    content = Faker('first_name')
    author = factory.SubFactory(UserFactory)
