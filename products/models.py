from django.db import models
from users.models import CustomeUser
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class item(models.Model):
    rating_list = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=50,decimal_places=2)
    offer_price = models.DecimalField(max_digits=50,decimal_places=2,default=0)
    image = models.FileField(upload_to='items')
    quantity = models.IntegerField()
    item_category = models.ForeignKey(category,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.CharField(choices=rating_list,max_length=5,null=True,blank=True)
    is_available = models.BooleanField(default=True)
    seller = models.ForeignKey(CustomeUser,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

    def get_size(self):
        try:
            sizes = item_size.objects.filter(item=self)

            return [size.size for size in sizes]
        except:
            return []

    def get_color(self):
        try:
            colors = item_color.objects.filter(item=self)
            return [color.color for color in colors]
        except:
            return []

class item_size(models.Model):
    size_list = [
        ('s','s'),
        ('m','m'),
        ('l','l'),
    ]
    item = models.ForeignKey(item,on_delete=models.CASCADE)
    size = models.CharField(choices=size_list,max_length=5)

    def __str__(self):
        return "Size : {} for item : {}".format(self.size,self.item)

class item_color(models.Model):
    color = models.CharField(max_length=100)
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    def __str__(self):
        return "Color : {} for item : {}".format(self.color,self.item)



