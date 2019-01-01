import factory.fuzzy
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

from apps.organization.models import *

USER_MODEL = get_user_model()


__all__ = [
    'CompanyFactory',
    'UserFactory'
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
    first_name = factory.fuzzy.FuzzyText(length=15)
    middle_name = factory.fuzzy.FuzzyText(length=15)
    last_name = factory.fuzzy.FuzzyText(length=15)
    phone_number = '+919999999999'
    gender = 'M'
    email = ''

    class Meta:
        model = Employee

#
# class ProfileFactory(factory.DjangoModelFactory):
#     class Meta:
#         model = Profile
