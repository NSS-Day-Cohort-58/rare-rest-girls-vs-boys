from django.db import models
from django.contrib.auth.models import User


class Rare_User(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_rare_user')
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

    @property
    def is_staff(self):
        return f'{self.user.is_staff}'

    @property
    def my_profile(self):
        return self.__my_profile

    @my_profile.setter
    def my_profile(self, value):
        self.__my_profile = value

    @property
    def sub_info(self):
        return self.__sub_info

    @sub_info.setter
    def sub_info(self, value):
        self.__sub_info = value
