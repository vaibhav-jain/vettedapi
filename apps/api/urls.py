from django.conf.urls import url, include
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from rest_framework import routers

from .viewsets import *

router = routers.DefaultRouter()
router.register('companies', CompanyViewSet)
router.register('employees', EmployeeViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^signup/', include('rest_auth.registration.urls')),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view(), name='rest_password_change'),
]
