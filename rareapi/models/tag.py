from django.db import models

class Tag(models.Model):
    """database model for tag"""

    label = models.CharField(max_length=55)

