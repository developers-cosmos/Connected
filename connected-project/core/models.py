from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile/images/', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post/images/')
    caption = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user

    def num_likes(self):
        return self.likes

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowersCount(models.Model):
    user = models.CharField(max_length=100)
    follower = models.CharField(max_length=100)

    def __str__(self):
        return self.user
