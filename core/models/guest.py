from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .base import BaseModel


class Guest(BaseModel):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='guests')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True, null=True)
    is_attending = models.BooleanField(default=False)
    dietary_restrictions = models.TextField(blank=True, null=True)
