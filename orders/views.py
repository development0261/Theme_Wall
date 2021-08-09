from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Order,ShippingAddress,OrderItem,wishlist
from products.models import item
from users.models import  Address


# Create your views here.
def ordersIndex(request):
    pass

def cart(request):
    if request.user.is_authenticated:
        return render(request,'products/cartPage.html')
    else:
        return redirect('login')

def checkout(request):
    if request.user.is_authenticated:
        return render(request,'products/checkout.html')
    else:
        return redirect('login')

def placeOrder(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            address1 = request.POST['address1']
            address2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            zip = request.POST['zip']
            country = request.POST['country']

            payment_type = request.POST['payment_type']
            final_total = request.POST['final_total']
            shipment_charge = request.POST['shipment_charge']
            tax_price = request.POST['tax_price']

            print(shipment_charge,tax_price,final_total)
            colors = request.POST.getlist('color[]')
            sizes = request.POST.getlist('size[]')
            prod_ids = request.POST.getlist('prod[]')
            qtys = request.POST.getlist('qty[]')

            order = Order(user= request.user,paymentMethod=payment_type,taxPrice=float(tax_price.strip()),shippingPrice=float(shipment_charge.strip()),totalPrice=float(final_total.strip()),
                          isPaid=False,isDelivered=False,status='Placed'
                          )
            order.save()
            address = ShippingAddress(order= order,address=address1+" "+address2,city=city,state=state,country=country,zip=zip)
            address.save()
            for it in range(0,len(list(prod_ids))):
                product = item.objects.get(pk=prod_ids[it])
                order_product = OrderItem(product=product,order=order,name=product.name,qty=qtys[it],price=float(product.price),image=product.image,
                                          color = colors[it],size=sizes[it]
                                          )
                order_product.save()

                product.quantity = int(product.quantity) - int(qtys[it])
                product.save()

            if not Address.objects.filter(user=request.user).exists():
                user_address = Address(city=city,state=state,country=country,pincode=zip,user=request.user,address=address1+" "+address2)
                user_address.save()


            return redirect('invoice')

        else:
            messages.error(request,'Not Valid Request')
            return redirect('checkout')
    else:
        return redirect('home')

def invoice(request):
    return render(request,'products/invoice.html')


def myOrders(request):
    if request.user.is_authenticated:
        if request.user.role == 'buyer':
            totalDeliveredOrders = Order.objects.filter(user=request.user,isDelivered=True).count()
            totalPendigOrders = Order.objects.filter(user=request.user,isDelivered=False).count()
            totalPaidOrders = Order.objects.filter(user=request.user,isPaid=True).count()
            totalUnPaidOrders = Order.objects.filter(user=request.user,isPaid=False).count()

            totalOrders =  Order.objects.filter(user=request.user)

            return render(request,'products/buyerOrders.html',{
                'totalDeliveredOrders':totalDeliveredOrders,
                'totalPendigOrders':totalPendigOrders,
                'totalPaidOrders':totalPaidOrders,
                'totalUnPaidOrders':totalUnPaidOrders,
                "totalOrders":totalOrders
            })
    else:
        return redirect('home')

def orderProducts(request,id):

    order_products = OrderItem.objects.filter(order_id=id)
    order_products = serializers.serialize('json', order_products, ensure_ascii=False)

    return JsonResponse({'msg':'success','products':order_products})

def sellerOrders(request):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            seller_orders = OrderItem.objects.filter(product__seller=request.user).values_list('order__id').distinct()
            totalDeliveredOrders =[]
            totalPendigOrders = []
            totalPaidOrders = []
            totalUnPaidOrders = []

            totalOrders = []

            for order_id in seller_orders:
                order = Order.objects.get(pk=order_id[0])
                totalOrders.append(order)
                if order.isDelivered:
                    totalDeliveredOrders.append(order)
                else:
                    totalPendigOrders.append(order)
                if order.isPaid:
                    totalPaidOrders.append(order)
                else:
                    totalUnPaidOrders.append(order)
            return render(request, 'products/sellerOrders.html', {
                'totalDeliveredOrders': len(totalDeliveredOrders),
                'totalPendigOrders': len(totalPendigOrders),
                'totalPaidOrders': len(totalPaidOrders),
                'totalUnPaidOrders': len(totalUnPaidOrders),
                "totalOrders": totalOrders
            })
    else:
        return redirect('home')


def fetchStatus(request,id):
    if request.user.is_authenticated:

        try:
            order = Order.objects.get(id=id)
            return JsonResponse({'msg':'success','status':order.status})
        except:
            return JsonResponse({'msg':'error'})

    else:
        return redirect('login')


def updateStatus(request):
    if request.user.is_authenticated:
        try:
            id = request.POST['orderId']
            status = request.POST['status']
            order = Order.objects.get(id=id)
            order.status = status
            order.save()
            messages.success(request,'Status for Order {} is updated to {}'.format(order.uuid,status))
            return redirect('sellerOrders')
        except:
            messages.error(request,'Something went wrong')
            return redirect('sellerOrders')
    else:
        return redirect(
            'login'
        )

@csrf_exempt
def addToWishList(request):
    if request.POST:
            products_list = []
            id = request.POST['productId']
            product = item.objects.get(pk=id)
            if wishlist.objects.filter(product=product,user=request.user).exists():
                wishes = wishlist.objects.all()
                for wish in wishes:
                    products_list.append(wish.product)
                return JsonResponse({'msg':'alreadyExist','products':serializers.serialize('json',products_list,ensure_ascii=False),'count':len(products_list)})
            else:
                wish = wishlist(product=product, user=request.user)
                wish.save()
                wishes = wishlist.objects.all()
                for wish in wishes:

                    products_list.append(wish.product)
                return JsonResponse({'msg':'success','products':serializers.serialize('json',products_list,ensure_ascii=False),'count':len(products_list)})

    else:
        return JsonResponse({'msg':'Invalid Request'})


def fetchWishlist(request):
    products_list = []
    wishs = wishlist.objects.filter(user = request.user)
    for wish in wishs:
        products_list.append(wish.product)
    return JsonResponse({'msg': 'success', 'products': serializers.serialize('json', products_list, ensure_ascii=False)})

