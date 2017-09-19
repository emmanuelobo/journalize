from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    age = models.IntegerField(null = True)
    profile_pic = models.ImageField()

    @receiver(post_save, sender=User)
    def register(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_changes(sender, instance, **kwargs):
        instance.profile.save()
