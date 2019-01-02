from django.urls import reverse_lazy
from rest_framework import status

from utils.messages import *
from .base import BaseViewSetTestCase
from .factories import CompanyFactory


class CompanyViewSetTestCase(BaseViewSetTestCase):
    """
    To test the integrity of CompanyAPI
    """

    def setUp(self):
        super(CompanyViewSetTestCase, self).setUp()
        self.companies_url = reverse_lazy('api:company-list')

    def test_post_empty_data_failing(self):
        """
        Ensure POSTing form over /companies/ with empty data fails.
        """
        response = self.client.post(self.companies_url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], [REQUIRED_FIELD_ERROR_MSG])

    def test_post_invalid_data_failing(self):
        """
        Ensure POSTing over /companies/ with invalid data fails.
        """
        self.payload = {'name': '', 'website': '', 'address': ''}
        response = self.client.post(self.companies_url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['website'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['address'], [BLANK_FIELD_ERROR_MSG])

        self.payload = {'name': ''}
        response = self.client.post(self.companies_url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['address'], [REQUIRED_FIELD_ERROR_MSG])

        self.payload = {'website': ''}
        response = self.client.post(self.companies_url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], [REQUIRED_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['website'], [BLANK_FIELD_ERROR_MSG])
        self.assertEqual(response.json()['address'], [REQUIRED_FIELD_ERROR_MSG])

    def test_post_valid_data_passing(self):
        """
        Ensure POSTing form over /companies/ with valid data passes.
        """
        self.payload = {
            'name': 'Test Company',
            'website': 'http://www.testcompany.com',
            'address': 'Test Road'
        }
        response = self.client.post(self.companies_url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_invalid_hash_failing(self):
        """
        Ensure GETing over /companies/<hash>/ with invalid hash fails.
        """
        url = reverse_lazy(
            'api:company-detail', kwargs={
                'hash': 'INVALID-HASH'
            })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_valid_hash_passing(self):
        """
        Ensure GETing over /companies/<hash>/ with valid hash passes.
        """
        company = CompanyFactory()
        url = reverse_lazy(
            'api:company-detail', kwargs={
                'hash': company.hash
            })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], company.name)

    def test_patch_invalid_hash_failing(self):
        """
        Ensure PATCHing json over /companies/<hash>/ with invalid hash fails.
        """
        url = reverse_lazy(
            'api:company-detail', kwargs={
                'hash': 'INVALID-HASH'
            })
        self.payload = {
            'name': 'Test Company', 'website': '', 'address': 'New Address'
        }
        response = self.client.patch(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_valid_hash_passing(self):
        """
        Ensure PATCHing over /companies/<hash>/ with valid hash passes.
        """
        company = CompanyFactory()
        url = reverse_lazy(
            'api:company-detail', kwargs={
                'hash': company.hash
            })
        self.payload = {
            'name': 'New Company', 'website': 'http://www.company.coom', 'address': 'New Address'
        }
        response = self.client.patch(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'New Company')
        self.assertEqual(response.json()['address'], 'New Address')

    def test_for_existing_company(self):
        """
        Test for existing company over /company/ fails.
        """
        company = CompanyFactory(name='Test Company')
        self.payload = {
            'name': 'Test Company', 'website': '', 'address': 'New Address'
        }
        url = reverse_lazy('api:company-list')
        response = self.client.post(url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], [DUPLICATE_COMPANY_ERROR_MSG])
