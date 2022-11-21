from django.db import models


class Subscription(models.Model):
    author = models.ForeignKey(
        "Rare_User", on_delete=models.CASCADE, related_name='user_subscriptions')
    follower = models.ForeignKey(
        "Rare_User", on_delete=models.CASCADE, related_name='follower_subscriptions')
    created_on = models.DateField()
    ended_on = models.DateField(null=True, blank=True)
