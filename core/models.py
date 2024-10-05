from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from users.models import ObjectEventTracker, UUIDPrimaryKey


class Note(UUIDPrimaryKey, ObjectEventTracker):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title
