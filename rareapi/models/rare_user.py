from django.db import models
from django.contrib.auth.models import User


class Rare_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField()
    profile_image_url = models.CharField(max_length=250)
    created_on = models.DateField()
    bio = models.CharField(max_length=300)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'

    @property
    def email(self):
        return f'{self.user.email}'
