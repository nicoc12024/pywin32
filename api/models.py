from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    email = models.CharField(max_length=255 , default="default")
    username = models.CharField(max_length=255 , null=True, blank=True , default="default")
    profilePicture = models.CharField(max_length=500, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)


class Blog(models.Model):
    body = models.CharField(max_length=255, default="default")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'blog')

