from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from utils.messages import *
from ..organization.models import *

__all__ = [
    'RegisterSerializer',
    'CompanySerializer',
    'UserDetailsSerializer',
    'UserSerializer',
    'EmployeeSerializer'
]


class SignupSerializer(RegisterSerializer):
    first_name = serializers.CharField(min_length=3, max_length=30, validators=[
        RegexValidator(r'^[ a-zA-Z ]*$', INVALID_FIRST_NAME_ERROR_MSG)
    ])
    last_name = serializers.CharField(min_length=3, max_length=30, validators=[
        RegexValidator(r'^[ a-zA-Z ]*$', INVALID_LAST_NAME_ERROR_MSG)
    ])
    company = serializers.UUIDField(required=True)

    def validate_company(self, company):
        try:
            return Company.objects.get(hash=company)
        except Company.DoesNotExist:
            raise serializers.ValidationError(COMPANY_DOES_NOT_EXIST_ERROR_MSG)

    def get_cleaned_data(self):
        """
        Needed to override to include user's
        first_name & last_name, This is handled by rest_auth internally
        """
        return {
            'username': self.validated_data.get('username', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'company': self.validated_data.get('company', '')
        }

    def save(self, request):
        user = super(SignupSerializer, self).save(request)
        Employee.objects.create(
            company=self.cleaned_data.get('company'), profile=user
        )
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Needed to override rest_auth default UserDetailsSerializer
    Used By JWTSerializer

    Returns User details in Read Only mode.
    Used By rest_auth in LoginView and JWTSerializer
    """
    company = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'company'
        )
        read_only_fields = ('id', 'email', 'first_name', 'last_name')

    @staticmethod
    def get_company(user):
        try:
            company = user.employee.company.hash
        except ObjectDoesNotExist:
            company = None
        return company


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email',
        )
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


class EmployeeSerializer(serializers.ModelSerializer):
    profile = UserSerializer(required=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of employee
        :return: returns a successfully created employee record
        """
        user_data = validated_data.pop('profile')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        employee = Employee.objects.create(
            profile=user,
            company=validated_data.pop('company')
        )
        return employee

    def update(self, employee, validated_data):
        user_data = validated_data.pop('profile')
        user = UserSerializer.update(
            UserSerializer(),
            validated_data=user_data,
            instance=employee.profile
        )
        employee.user = user
        employee.company = validated_data.pop('company')
        employee.save()
        return employee
