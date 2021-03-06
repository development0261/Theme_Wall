from django.db import models
from users.models import CustomeUser
# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.name

    def get_product_count(self):
        return item.objects.filter(category=self).count()

class item(models.Model):
    rating_list = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    ]
    serial_no = models.CharField(max_length=200,default="")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=50,decimal_places=2)
    offer_price = models.DecimalField(max_digits=50,decimal_places=2,default=0)
    image = models.FileField(upload_to='items',default="noImage.png",null=True,blank=True)
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
            sizes = item_size.objects.filter(item=self).distinct()

            return [size.size for size in sizes]
        except:
            return []

    def get_color(self):
        try:
            colors = item_color.objects.filter(item=self)
            return [color.color for color in colors]
        except:
            return []

    def get_qtys(self):
        try:
            qtys = item_qty.objects.filter(product = self)
            return qtys
        except:
            return []

    def check_if_no_size(self):

            sizes = item_qty.objects.filter(product=self).values_list('size__size',flat=True)

            if 'No_Size' in sizes:
                return True
            else:
                return False

    def get_extra_images(self):
        return Images.objects.filter(product=self)

class item_size(models.Model):
    size_list = [
        ('small','small'),
        ('medium','medium'),
        ('large','large'),
        ('No_Size','No_Size'),
    ]
    item = models.ForeignKey(item,on_delete=models.CASCADE)
    size = models.CharField(choices=size_list,max_length=20,null=True,blank=True)

    def __str__(self):
        return "Size : {} for item : {}".format(self.size,self.item)



class item_color(models.Model):
    color = models.CharField(max_length=100)
    item = models.ForeignKey(item, on_delete=models.CASCADE,related_name='color')
    def __str__(self):
        return "Color : {} for item : {}".format(self.color,self.item)

class Images(models.Model):
    image = models.FileField(upload_to='items',default="noImage.png",null=True,blank=True)
    size = models.ForeignKey(item_size, on_delete=models.CASCADE, related_name='size_image_qty',null=True,blank=True)
    color = models.ForeignKey(item_color, on_delete=models.CASCADE, related_name='color_image_qty',null=True,blank=True)
    product = models.ForeignKey(item,on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url

class item_qty(models.Model):
    product = models.ForeignKey(item,on_delete=models.CASCADE)
    size = models.ForeignKey(item_size,on_delete=models.CASCADE,related_name='size_qty')
    color = models.ForeignKey(item_color,on_delete=models.CASCADE,related_name='color_qty')
    image = models.ForeignKey(Images,on_delete=models.CASCADE,related_name='color_qty',null=True
                              ,blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return  "{} {} with size : {} and color {} ".format(self.quantity,self.product,self.size,self.color)

class SellerReview(models.Model):
    product = models.ForeignKey(item,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name="product_buyer")
    seller = models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name="product_seller")

    stars = models.IntegerField(verbose_name="thumbs")
    title = models.CharField(max_length=200,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class ProductReview(models.Model):
    product = models.ForeignKey(item,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name="product_review_buyer")
    stars = models.IntegerField(verbose_name="thumbs")
    title = models.CharField(max_length=200,null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Posters(models.Model):
    image = models.ImageField(upload_to="poster")
    title = models.CharField(null=True,blank=True,max_length=20)

