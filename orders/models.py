import uuid as uuid
from django.db import models

# Create your models here.
from products.models import item
from users.models import CustomeUser


class Order(models.Model):
    status_type = [
        (
            'Placed','Placed'
        ),
        (
            'Packed','Packed'
        ),
        (
            'Shipped','Shipped'
        ),
        (
            'Delivered','Delivered'
        )
    ]
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    amountPaid = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True, editable=False)

    status = models.CharField(choices=status_type,null=True,blank=True,max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)

    def __str__(self):
        return "{} has placed order with {} and price {} with id {} ".format(self.user,self.paymentMethod,self.totalPrice,self.pk)

    def get_order_items(self):
        items = OrderItem.objects.filter(order=self)
        return items
    def get_order_item_count(self):

        count = OrderItem.objects.filter(order=self).count()
        return count


class OrderItem(models.Model):
    product = models.ForeignKey(item, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,related_name='order_item')
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    image = models.ImageField(default=None, null=True, blank=True)
    id = models.AutoField(primary_key=True, editable=False)
    color = models.CharField(max_length=100,default="")
    size = models.CharField(max_length=100,default="")
    def __str__(self):
        return str(self.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zip = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    id = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return "{},{},{}".format(self.city,self.state,self.country)

class wishlist(models.Model):
    product = models.ForeignKey(item,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
