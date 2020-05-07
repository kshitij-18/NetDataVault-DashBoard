from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    pin_code = models.IntegerField()

    def __str__(self):
        return self.user.username


class AuthKeyModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_key = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name


'''@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()'''


'''@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()'''
