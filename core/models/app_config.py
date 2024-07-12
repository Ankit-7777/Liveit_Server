from django.db import models
from .base import BaseModel

class AppConfig(BaseModel):
    message = models.TextField(max_length=255)
    business_config = models.JSONField(default=dict)
    
    