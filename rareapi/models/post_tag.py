from django.db import models

class PostTag(models.Model):
    """database model for post tag"""

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_tags_post')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='post_tags_tags')