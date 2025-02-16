# users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Only create profile for new users
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Try to access profile, create if not exists
    profile, created = UserProfile.objects.get_or_create(user=instance)
    if not created:
        profile.save()  # Save the existing profile if needed
