from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .base import BaseModel


class Vendor(BaseModel):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='vendors')
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
