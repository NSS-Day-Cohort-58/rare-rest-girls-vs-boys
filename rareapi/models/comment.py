from django.db import models


class Comment(models.Model):
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(
        "Rare_User", on_delete=models.CASCADE, related_name='user_comments')
    content = models.CharField(max_length=250)
    created_on = models.DateField()


    @property
    def created(self):
        return self.__created

    @created.setter
    def created(self, value):
        self.__created = value
