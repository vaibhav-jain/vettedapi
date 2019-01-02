import factory.fuzzy
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

from apps.organization.models import *

USER_MODEL = get_user_model()


__all__ = [
    'CompanyFactory',
    'UserFactory',
    'EmployeeFactory'
]


class CompanyFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()

    class Meta:
        model = Company


class EmailAddressFactory(factory.DjangoModelFactory):
    primary = True
    verified = True
    email = "test@example.com"

    class Meta:
        model = EmailAddress


class UserFactory(factory.DjangoModelFactory):
    username = "testuser"
    email = "testuser@example.com"
    password = "testpassword"

    class Meta:
        model = USER_MODEL


class EmployeeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Employee
