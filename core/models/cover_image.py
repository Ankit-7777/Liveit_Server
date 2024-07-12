from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from PIL import Image
from .base import BaseModel

class CoverImage(BaseModel):
    image = models.ImageField(upload_to='covers/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png','webp'])])
    event_category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='events_category_type')
    
    def __str__(self):
        return f"{self.event_category} Theme CoverImage"
