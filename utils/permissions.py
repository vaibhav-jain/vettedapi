"""
Custom permission module
"""

from apps.organization.models import Employee


class BasePermission(object):
    """
    A base class from which all permission classes should inherit.
    Needed to make the methods static.
    Otherwise rest_condition will through error.
    """

    @staticmethod
    def has_permission(request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    @staticmethod
    def has_object_permission(request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class IsCompanyUser(BasePermission):
    """
    Allow access to only users related to company.
    """

    @staticmethod
    def has_permission(request, view):
        queryset = Employee.objects.filter(
            company__hash=view.kwargs['company_id'],
            profile=request.user
        )
        return True if queryset else False
