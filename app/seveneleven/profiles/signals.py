from django.db.model.signals import post_save
from app.seveneleven.authentication.models import User
from django.dispatch import receiver

from app.seveneleven.profiles.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
