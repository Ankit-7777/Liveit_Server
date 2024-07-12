from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .base import BaseModel

class ContactUs(BaseModel):
    name = models.CharField(_("Name"), max_length=100,  null=False)
    email = models.EmailField(_("Email"),null=False)
    message = models.TextField(_("Message"), max_length=300,null=False)

