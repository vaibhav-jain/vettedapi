from django.conf import settings
from django.conf.urls import include, url, static
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_jwt.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Vetted API",
      default_version='v1',
      description='POC for vetted',
      terms_of_service="",
      contact=openapi.Contact(email="contact@vettedapi.in"),
      license=openapi.License(name="Proprietary License"),
   ),
   validators=['flex', 'ssv'],
   public=False,
   permission_classes=(AllowAny,),
)

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(('apps.api.urls', 'apps.api'), namespace='api')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_title = 'Vettedapi Administration'
admin.site.index_title = 'Vettedapi Administration'
admin.site.site_header = 'Vettedapi Administration'
