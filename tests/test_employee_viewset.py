from django.core import mail
from django.urls import reverse_lazy
from rest_framework import status

from apps.organization.models import Employee
from utils.messages import *
from .base import BaseViewSetTestCase
from .factories import *

TEMPLATES_LIST = [
    'account/email/email_confirmation_signup_subject.txt',
    'account/email/email_confirmation_subject.txt',
    'account/email/email_confirmation_signup_message.txt',
    'account/email/email_confirmation_message.txt',
    'account/messages/email_confirmation_sent.txt'
]


class EmployeeViewSetTestCase(BaseViewSetTestCase):
    """
    To test the integrity of EmployeeAPI
    """

    def setUp(self):
        super(EmployeeViewSetTestCase, self).setUp()
        self.company = CompanyFactory()
        self.signup_url = reverse_lazy('api:rest_register')
        self.employees_url = reverse_lazy('api:employee-list')

    def test_post_empty_json_failing(self):
        """
        Ensure POSTing form over /signup/ with invalid data fails.
        """
        payload = {
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
            'username': '',
            'company': '',
            'is_admin': ''
        }
        response = self.client.post(self.signup_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_permission(self):
        """
        Ensure Patching form over /employees/<company_id>/<pk>/ with invalid permission fails.
        """
        url = reverse_lazy(
            'api:employee-detail', kwargs={
                'company_id': self.company.hash,
                'pk': 'pk'
            })
        self.payload = {}
        response = self.client.patch(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], INVALID_PERMISSION_ERROR_MSG)

    def test_valid_form_passing_signup(self):
        """
        Ensure POSTing form over /signup/ with valid payload passes
        """
        payload = {
            'email': 'vaibhav10jain@gmail.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'testusername',
            'company': self.company.hash,
            'is_admin': False
        }
        response = self.client.post(self.signup_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['vaibhav10jain@gmail.com'])
        for template in TEMPLATES_LIST:
            self.assertTemplateUsed(response, template)

    def test_post_invalid_data_failing(self):
        """
        Ensure POSTing over /signup/ with invalid data fails.
        """
        payload = {
            'email': '',
            'password1': '',
            'password2': '',
            'first_name': '',
            'last_name': '',
            'username': '',
            'company': '',
            'is_admin': ''
        }
        employee = Employee.objects.create(
            company=self.company, profile=self.user
        )
        response = self.client.post(self.signup_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['username'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['first_name'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['last_name'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['last_name'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['password1'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['password2'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['company'], [INVALID_UUID_ERROR_MSG])
        self.assertEqual(response.json()['is_admin'], [INVALID_BOOLEAN_ERROR_MSG])

        payload['email'] = 'invalidemail'
        response = self.client.post(self.signup_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'], [INVALID_EMAIL_ID_ERROR_MSG])

        payload['email'] = self.user.email
        response = self.client.post(self.signup_url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['email'], [DUPLICATE_EMAIL_ID_ERROR_MSG])

    def test_get_invalid_hash_failing(self):
        """
        Ensure GETing over /employees/<company_id>/<pk>/ with invalid pk fails.
        """
        url = reverse_lazy(
            'api:employee-detail', kwargs={
                'company_id': self.company.hash,
                'pk': 'INVALID-PK'
            })
        employee = Employee.objects.create(
            company=self.company, profile=self.user
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_pk_passing(self):
        """
        Ensure GETing over /employees/<company_id>/<pk>/ with valid pk passes.
        """
        employee = EmployeeFactory(company=self.company, profile=self.user)
        url = reverse_lazy(
            'api:employee-detail', kwargs={
                'company_id': self.company.hash,
                'pk': employee.pk
            })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['profile']['first_name'], employee.profile.first_name)
        self.assertEqual(response.json()['profile']['last_name'], employee.profile.last_name)
        self.assertEqual(response.json()['profile']['email'], employee.profile.email)

    def test_patch_invalid_pk_failing(self):
        """
        Ensure PATCHing json over /employees/<company_id>/<pk>/ with invalid hash fails.
        """
        url = reverse_lazy(
            'api:employee-detail', kwargs={
                'company_id': self.company.hash,
                'pk': 'INVALID'
            })
        self.payload = {
            'profile': {
                'first_name': 'Test first name',
                'last_name': 'Test last name'
            }
        }
        employee = Employee.objects.create(
            company=self.company, profile=self.user
        )
        response = self.client.patch(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_valid_pk_passing(self):
        """
        Ensure PATCHing over /employees/<company_id>/<pk>/ with valid pk passes.
        """
        employee = EmployeeFactory(company=self.company, profile=self.user)
        url = reverse_lazy(
            'api:employee-detail', kwargs={
                'company_id': self.company.hash,
                'pk': employee.pk
            })
        self.payload = {
            'profile': {
                'first_name': 'Test First Name',
                'last_name': 'Test Last Name',
                'username': self.user.username,
                'email': self.user.email
            },
            'company': employee.company.id,
            'id': employee.pk
        }
        response = self.client.patch(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking new updated employee
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['profile']['first_name'], 'Test First Name')
        self.assertEqual(response.json()['profile']['last_name'], 'Test Last Name')
