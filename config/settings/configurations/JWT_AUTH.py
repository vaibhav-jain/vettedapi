""" Django REST JWT settings """

import datetime

from .ENV import ENV_VAR

JWT_AUTH = {
    'JWT_SECRET_KEY': ENV_VAR('SECRET_KEY'),
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    # Time Up-to which tokens should not expire
    # Client Should refresh tokens before this time
    # to prevent them from expiring, Set to 7 days
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=604800),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_ALLOW_REFRESH': True,
    # Maximum time up-to which tokens can be refreshed
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
