from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        "Rare_User", on_delete=models.CASCADE, related_name='user_posts')
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name='category_posts')
    title = models.CharField(max_length=250)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=250)
    content = models.CharField(max_length=250)
