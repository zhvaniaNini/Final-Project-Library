from django.db import models
from django.contrib.auth.models import User
from booklibrary.models import Reservation, Borrow
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    reserved_books = models.ManyToManyField(Reservation, blank=True, related_name='reserved_by')
    borrowed_books = models.ManyToManyField(Borrow, blank=True, related_name='borrowed_by')

    def __str__(self):
        return str(self.user)

    class Meta:
      verbose_name = "Profile"
      verbose_name_plural = "Profiles"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)