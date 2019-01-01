"""
Rest Auth settings
"""

REST_USE_JWT = True

REST_AUTH_REGISTER_SERIALIZERS = {
    # Custom Signup serializer, Used by rest_auth
    # Needed to set some extra settings like School data during signup
    'REGISTER_SERIALIZER': 'apps.api.serializers.SignupSerializer'
}
REST_AUTH_SERIALIZERS = {
    # Custom User Details Serializer used only for fetching User details
    # Its not used during Login
    'USER_DETAILS_SERIALIZER': 'apps.api.serializers.UserDetailsSerializer'
}
