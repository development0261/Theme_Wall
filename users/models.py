from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField

class CustomeUser(AbstractUser):
	role_list = [
		('buyer', 'buyer'),
		('seller', 'seller')
	]
	role = models.CharField(max_length=10, choices=role_list,null=True,blank=True,default='buyer')
	contact_no = models.BigIntegerField(null=True,blank=True)
	address = models.TextField(null=True,blank=True)
	fullname = models.CharField(max_length=100,default="",null=True,blank=True)


	def __str__(self):
		return self.username


class SellerRequest(models.Model):
	email = models.CharField(max_length=200)
	user = models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
	message = models.TextField()
	proof = models.FileField(upload_to='proofs',default="")
	date = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return "{} want to be seller on email {}".format(self.user,self.email)


class Profile(models.Model):
	user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	slug = AutoSlugField(populate_from='user')
	bio = models.CharField(max_length=255, blank=True)
	friends = models.ManyToManyField("Profile", blank=True)


	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return "/users/{}".format(self.slug)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:

            Profile.objects.create(user=instance)

        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

# class FriendRequest(models.Model):
# 	to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
# 	from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
# 	timestamp = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return "From {}, to {}".format(self.from_user.username, self.to_user.username)



