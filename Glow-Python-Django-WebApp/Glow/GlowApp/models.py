from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/')


class Follow(models.Model):
    follow_follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follow_followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follow_follower', 'follow_followed')

    def __str__(self):
        return f'{self.follow_follower} follows {self.follow_followed}'

    def follow(self, user):
        if not self.follow_follower.is_following(user):
            Follow.objects.create(follow_follower=self.follow_follower, follow_followed=user)

    def unfollow(self, user):
        if self.follow_follower.is_following(user):
            Follow.objects.filter(follow_follower=self.follow_follower, follow_followed=user).delete()

    def is_following(self, user):
        return self.following.filter(follow_followed=user).exists()

    def is_followed_by(self, user):
        return self.followed.filter(follow_follower=user).exists()


class Media(models.Model):
    MEDIA_TYPES = [
        ('picture', 'Picture'),
        ('video', 'Video')
    ]
    media_title = models.CharField(max_length=30, blank=False, null=False)
    media_description = models.TextField(max_length=500, blank=True)
    media_uploaddate = models.DateTimeField(auto_now_add=True)
    media_likes = models.ManyToManyField(User, related_name='liked_media', blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    media_file = models.FileField(upload_to='media_files/', blank=True, null=True)
    media_uploader = models.ForeignKey(User, on_delete=models.CASCADE)

    def likes_count(self):
        return self.media_likes.count()

    def __str__(self):
        return self.media_title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    comment_description = models.TextField(max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True)


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_description = models.TextField()
