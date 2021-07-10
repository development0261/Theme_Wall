from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from .validators import file_size
class Post(models.Model):
	description = models.CharField(max_length=255, blank=True)
	pic = models.ImageField(upload_to='path/to/img',blank=True)
	video = models.FileField(upload_to='path/to/video',validators=[file_size],blank=True)
	date_posted = models.DateTimeField(default=timezone.now)
	user_name = models.ForeignKey(User, on_delete=models.CASCADE)
	tags = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.description


	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
 





class Notification(models.Model):
	NOTIFICATION_TYPES = ((1,'Like'),(2,'Comment'))
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
	notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
	text_preview = models.CharField(max_length=90, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)


class Comments(models.Model):
	post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)
	def user_comment_post(sender, instance, *args, **kwargs):
		comment = instance
		post = comment.post
		text_preview = comment.comment[:90]
		sender = comment.username
		notify = Notification(post=post, sender=sender, user=post.user_name, text_preview=text_preview ,notification_type=2)
		notify.save()

	def user_del_comment_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.username

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
		notify.delete()

class Like(models.Model):
	user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)


	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user
		notify = Notification(post=post, sender=sender, user=post.user_name, notification_type=1)
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		post = like.post
		sender = like.user

		notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
		notify.delete()	


#Likes
post_save.connect(Like.user_liked_post, sender=Like)
post_delete.connect(Like.user_unlike_post, sender=Like)
#comment
post_save.connect(Comments.user_comment_post, sender=Comments)
post_delete.connect(Comments.user_del_comment_post, sender=Comments)
