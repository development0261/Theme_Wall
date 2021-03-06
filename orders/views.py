import datetime

from django.conf import settings
from django.contrib import messages
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Order,ShippingAddress,OrderItem,wishlist
from products.models import item, item_qty, Images
from users.models import Address, CustomeUser
import stripe
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
stripe.api_key = settings.STRIPE_PRIVATE_KEY
YOUR_DOMAIN = "https://themes-wall.herokuapp.com/"

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
        past_address = ShippingAddress.objects.filter(order__user = request.user).values_list('address','zip').distinct()
        addresses = []
        for add in past_address:
            addresses.append(ShippingAddress.objects.filter(address=add[0],zip=add[1]).first())

        return render(request,'products/checkout.html',{'addresses':addresses})
    else:
        return redirect('login')

def placeOrder(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            addressID = request.POST['addressID']
            print(addressID)
            print(request.POST['address'].strip())

            if addressID != '':
                add = ShippingAddress.objects.get(pk=addressID)
                address = add.address
                city = add.city
                state = add.state
                zip = add.zip
                country = add.country

            elif request.POST['address'].strip() != '':
                address = request.POST['address']
                city = request.POST['city']
                state = request.POST['state']
                zip = request.POST['zip']
                country = request.POST['country']
            else:
                messages.error(request, 'Please Enter or Select Complete Address')
                return redirect('checkout')

            contact = request.POST['contact']
            payment_type = request.POST['payment_type']
            final_total = request.POST['final_total']
            shipment_charge = request.POST['shipment_charge']
            tax_price = request.POST['tax_price']
            colors = request.POST.getlist('color[]')
            sizes = request.POST.getlist('size[]')
            prod_ids = request.POST.getlist('prod[]')
            qtys = request.POST.getlist('qty[]')

            request.user.contact_no = contact
            request.user.save()
            amountPaid = float(final_total)+(float(final_total)*8)/100 + 0.0028
            print(float(final_total))
            print(amountPaid)
            order = Order(user= request.user,paymentMethod=payment_type,totalPrice=float(final_total.strip()),
                          isPaid=False,status='Placed',amountPaid=amountPaid
                          )
            order.save()
            address = ShippingAddress(order= order,address=address,city=city,state=state,country=country,zip=zip)
            address.save()
            for it in range(0,len(list(prod_ids))):
                product = item.objects.get(pk=prod_ids[it])
                price_to_add = product.price
                if product.offer_price > 0:
                    price_to_add = product.offer_price
                order_product = OrderItem(product=product,order=order,name=product.name,qty=qtys[it],price=price_to_add,image=product.image,
                                          color = colors[it],size=sizes[it]
                                          )
                order_product.save()

                prod_qty = item_qty.objects.get(product=order_product.product,color__color__iexact='#'+order_product.color,size__size__iexact=order_product.size)
                prod_qty.quantity = int(prod_qty.quantity) - int(qtys[it])
                prod_qty.save()

            if not Address.objects.filter(user=request.user).exists():
                user_address = Address(city=city,state=state,country=country,pincode=zip,user=request.user,address=address)
                user_address.save()

            if payment_type == 'cod':
                context = {'order': order}
                html_content = render_to_string('products/email.html', context=context).strip()
                msg = EmailMultiAlternatives("Your Order has been Placed with The Men's Wall",html_content,
                          settings.EMAIL_HOST_USER,[order.user.email]
                          )
                msg.content_subtype = 'html'  # Main content is text/html
                msg.mixed_subtype = 'related'
                msg.send()
                order_products = order.get_order_items()
                orders_sellers = order_products.values_list('product__seller',flat=True).distinct()
                products_of_same_seller = {}

                for seller in orders_sellers:
                    products_of_same_seller[seller] = order_products.filter(product__seller=seller)

                for seller,products in products_of_same_seller.items():
                    context = {'order': order,'products':products,'YOUR_DOMAIN':YOUR_DOMAIN}
                    html_content = render_to_string('products/emailProducts.html', context=context).strip()
                    cmsg = EmailMultiAlternatives("You have received orders for your products on men's wall", html_content,
                                                 settings.EMAIL_HOST_USER, [CustomeUser.objects.get(pk=seller).email]
                                                 )
                    msg.content_subtype = 'html'  # Main content is text/html
                    msg.mixed_subtype = 'related'
                    msg.send()
                return redirect('/orders/invoice/'+str(order.pk))
            else:
                session = stripe.checkout.Session.create(
                    client_reference_id=request.user.id if request.user.is_authenticated else None,
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'USD',
                            'product_data': {
                                'name': "Payment to The Men's Wall",
                            },
                            'unit_amount': int(order.amountPaid * 100),
                        },
                        'quantity': 1,
                    }],
                    metadata={
                        "order_id": order.uuid
                    },
                    mode='payment',

                    success_url=YOUR_DOMAIN + '/orders/invoice/'+str(order.pk),
                    cancel_url=YOUR_DOMAIN + '/orders/paymentFail/'+str(order.pk),
                )
                return redirect('/orders/stripecheckout/'+session.id)

        else:
            messages.error(request,'Not Valid Request')
            return redirect('checkout')
    else:
        return redirect('home')

def stripecheckout(request,session_id):
    return render(request,'products/stripe.html',{'session_id':session_id})

def invoice(request,id):
   if request.user.is_authenticated:
       order = Order.objects.get(pk=int(id))
       if 'access' in request.GET:
           print('access')
           pass
       else:

           if order.paymentMethod == 'stripe':
               order.isPaid = True
               order.paidAt = datetime.datetime.now()
               order.save()
               context = {'order': order}
               html_content = render_to_string('products/email.html', context=context).strip()
               msg = EmailMultiAlternatives("Your Order has been Placed with The Men's Wall", html_content,
                                            settings.EMAIL_HOST_USER, [order.user.email]
                                            )
               msg.content_subtype = 'html'  # Main content is text/html
               msg.mixed_subtype = 'related'
               msg.send()

               order_products = order.get_order_items()
               orders_sellers = order_products.values_list('product__seller', flat=True).distinct()
               products_of_same_seller = {}

               for seller in orders_sellers:
                   products_of_same_seller[seller] = order_products.filter(product__seller=seller)

               for seller, products in products_of_same_seller.items():
                   context = {'order': order, 'products': products, 'YOUR_DOMAIN': YOUR_DOMAIN}
                   html_content = render_to_string('products/emailProducts.html', context=context).strip()
                   msg = EmailMultiAlternatives("You have received orders for your products on men's wall",
                                                html_content,
                                                settings.EMAIL_HOST_USER, [CustomeUser.objects.get(pk=seller).email]
                                                )
                   msg.content_subtype = 'html'  # Main content is text/html
                   msg.mixed_subtype = 'related'
                   msg.send()

       address = ShippingAddress.objects.get(order=order)
       return render(request, 'products/invoice.html', {'order': order, 'address': address})
   else:
        return redirect('login')


def myOrders(request):
    if request.user.is_authenticated:
        if request.user.role == 'buyer' or request.user.is_superuser:
            totalDeliveredOrders = Order.objects.filter(user=request.user,status='Delivered').count()
            totalPendigOrders = Order.objects.filter(Q(user=request.user) and ~Q(status='Delivered')).count()
            totalPaidOrders = Order.objects.filter(user=request.user,isPaid=True).count()
            totalUnPaidOrders = Order.objects.filter(user=request.user,isPaid=False).count()
            totalOrders =  Order.objects.filter(user=request.user).order_by(
                '-createdAt'
            )
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
            seller_orders = OrderItem.objects.filter(product__seller=request.user).values_list('order__id').distinct().order_by(
                '-order__createdAt'
            )
            totalDeliveredOrders =[]
            totalPendigOrders = []
            totalPaidOrders = []
            totalUnPaidOrders = []
            totalOrders = []
            for order_id in seller_orders:
                order = Order.objects.get(pk=order_id[0])
                totalOrders.append(order)
                if order.status == 'Delivered':
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
            if status == 'Delivered':
                order.isPaid = True
                order.deliveredAt = datetime.datetime.now()

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

@csrf_exempt
def webhook(request):
    print("Webhook")
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
        ID=session["metadata"]["order_id"]
        order = Order.objects.get(id=ID)
        order.isPaid = True
        order.save()

    return HttpResponse(status=200)

def paymentFail(request,id):

    order = Order.objects.get(pk=id)
    order.delete()

    return render(request,'products/paymentFail.html')


def removeFromWishList(request,id):

        product = wishlist.objects.get(product__pk=id)
        product.delete()
        return JsonResponse({'msg':'success'})

