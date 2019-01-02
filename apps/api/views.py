"""
Contains API Views for Widgets
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.organization.models import *

__all__ = [
    'CountWidgetView'
]


class CountWidgetView(APIView):
    """
    Returns Stats like : Number of companies & employees etc
    """
    permission_classes = (IsAuthenticated,)
    #
    # def get_permissions(self):
    #     permission_classes = super(SchoolStatsWidgetView, self).get_permissions()
    #     permission_classes += (Or(IsSchoolAdmin, IsTeacher),)
    #     return permission_classes

    def get(self, request, *args, **kwargs):
        companies = Company.objects.count()
        employees = Employee.objects.count()
        return Response({
            'companies': companies,
            'employees': employees
        })
