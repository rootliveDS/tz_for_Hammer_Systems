from django.db import models


class UserProfile(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    authorization_code = models.CharField(max_length=4)
    is_authorized = models.BooleanField(default=False)
    personal_code = models.CharField(max_length=6, null=True, blank=True, unique=True)
    invited_phone = models.JSONField(default=list)

    def __str__(self):
        return self.phone_number