from django.contrib.auth.models import User
from rest_framework import viewsets, serializers

from apps.organization.models import *
from utils import DUPLICATE_USER_ERROR_MSG

# from utils.permissions import IsCompanyUser
from .serializers import *


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = lookup_url_kwarg = 'hash'


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = (IsCompanyUser,)
    http_method_names = [
        'get', 'patch', 'delete', 'options'
    ]

    def create(self, request, *args, **kwargs):
        duplicate = User.objects.filter(
            username=request.data['profile']['username']
        ).exists()

        if duplicate:
            raise serializers.ValidationError(DUPLICATE_USER_ERROR_MSG)
        return super(EmployeeViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        duplicate = User.objects.filter(
            username=request.data['profile']['username']
        ).exclude(pk=instance.profile.pk).exists()

        if duplicate:
            raise serializers.ValidationError(DUPLICATE_USER_ERROR_MSG)
        return super(EmployeeViewSet, self).update(request, *args, **kwargs)
