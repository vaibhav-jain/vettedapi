from rest_framework import test
from rest_framework_jwt import utils

from .factories import *


class BaseViewSetTestCase(test.APITestCase):
    """
    BaseViewTestCase from which all TestCase must inherit.
    """

    def setUp(self):
        self.payload = {}
        self.user = UserFactory()
        self.user.set_password(self.user.password)
        payload = utils.jwt_payload_handler(self.user)
        self.token = utils.jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.token))

    def set_new_client(self, user=None):
        """
        Sets new client with new credentials
        """
        user = user if user is not None else self.user
        payload = utils.jwt_payload_handler(user)
        token = utils.jwt_encode_handler(payload)
        return self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(token))
