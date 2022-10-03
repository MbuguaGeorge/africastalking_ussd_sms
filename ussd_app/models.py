from email.policy import default
from enum import unique
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    phone = models.CharField(max_length=200, unique=True, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    age = models.IntegerField(default=18, null=True, blank=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    village = models.CharField(max_length=200, blank=True, null=True)
    group_no = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return self.name