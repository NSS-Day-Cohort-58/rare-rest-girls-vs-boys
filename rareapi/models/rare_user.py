from django.db import models


class Rare_User(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name='rare_user_user')
    active = models.BooleanField()
    profile_image_url = models.CharField(max_length=250)
    created_on = models.DateField()
    bio = models.CharField(max_length=300)
