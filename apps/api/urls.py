from django.conf.urls import url, include
from rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from rest_framework import routers

from .views import *
from .viewsets import *

router = routers.DefaultRouter()
router.register('companies', CompanyViewSet)
router.register('employees/(?P<company_id>[^/.]+)', EmployeeViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^count-widget/$', CountWidgetView.as_view(), name='count-widget'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^signup/', include('rest_auth.registration.urls')),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
]
