from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Event, Group


@receiver(post_save, sender=Event)
def create_group_for_event(sender, instance, created, **kwargs):
    if created:
        group_name = f"{instance.event_category.category_name} Group"
        Group.objects.create(name=group_name, event=instance, member=instance.user, is_active=True)
