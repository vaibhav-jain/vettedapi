import uuid

from django.contrib.auth.models import User
from django.db import models

__all__ = [
    'Company',
    'Employee'
]


class Company(models.Model):
    """
    Company model
    """
    name = models.CharField(
        max_length=50, unique=True
    )
    hash = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    address = models.TextField()
    website = models.URLField(null=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return "{}-{}".format(self.name, self.hash)


class Employee(models.Model):
    """
    Employee model
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
