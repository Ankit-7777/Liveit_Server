from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from .base import BaseModel

class Event(BaseModel):
    
    event_id = models.CharField(_("Event ID"), max_length=255,)
    cover_image_id = models.ForeignKey('CoverImage', on_delete=models.PROTECT, related_name= 'event_cover_image')
    image = models.ImageField(upload_to='EventImages/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name = 'events_user')
    event_category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='events_category')
    additional_fields = models.JSONField(_("Fields"), null=False, default = dict())
    event_date = models.DateField(_("date"), null=True, blank=True)
    role = models.CharField(_("role"), max_length=100, blank=True, null=True)
    is_published = models.BooleanField(_("Is Published"), default=False)
    invited = models.ManyToManyField('UserProfile', related_name='shared_events', blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_seen = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.event_category}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.event_id:
            self.generate_unique_event_id()
            self.save()

    def generate_unique_event_id(self):
        category_name = self.event_category.category_name
        self.event_id = f"{category_name}_{self.id}"
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


