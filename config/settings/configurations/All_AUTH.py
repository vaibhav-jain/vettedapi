""" all_auth settings """

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_ADAPTER = 'utils.adapter.SignupAdapter'
ACCOUNT_EMAIL_SUBJECT_PREFIX = 'VettedApp: '
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
