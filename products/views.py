from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import category,item,item_size,item_color
from django.contrib import messages
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def allProducts(request):


    return render(request,"products.html")


def sellerDash(request):
    if request.user.is_authenticated and request.user.role == "seller":
        all_categories = category.objects.all()
        my_products = item.objects.filter(seller=request.user,seller__role='seller')
        return render(request,'products/sellerDash.html',{'all_categories':all_categories,'my_products':my_products})
    else:
        return redirect("home")

@csrf_exempt
def addCategory(request):
    if request.method == "POST":
        cat = request.POST['category']
        category_isnt = category(name=cat)
        category_isnt.save()
        #category = serializers.serialize('json', [docs], ensure_ascii=False)
        return JsonResponse({'msg':'success','category':category_isnt.name})

def deleteProduct(request,id):
    try:
        prod = get_object_or_404(item, id=id)
        prod.delete()
        messages.success(request,"Your Product {} is deleted".format(prod.name))
    except:
        messages.error(request,"Product Not Available")
    return redirect('sellerDash')


def addProduct(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            try:
                name = request.POST['name']
                price = request.POST['price']
                offer = request.POST['offer']
                it_category = request.POST['category']
                quantity = request.POST['quantity']
                image = request.FILES['image']
                description = request.POST['description']
                sizes = request.POST.getlist('size[]')
                colors = request.POST.getlist('color[]')

                print(name, price, offer, category, quantity, image, sizes, colors)

                prod = item(name=name, price=price, offer_price=offer,
                            item_category=category.objects.get(id=it_category),
                            quantity=quantity, image=image, description=description, seller=request.user)
                prod.save()

                if sizes[0] != '':
                    sizes = set(sizes)
                    for size in sizes:
                        it_size = item_size(size=size, item=prod)
                        it_size.save()
                if colors[0] != '':
                    colors = set(colors)
                    for color in colors:
                        it_color = item_color(color=color, item=prod)
                        it_color.save()
                messages.success(request, "Your Product is added successfully")
            except:
                messages.error(request, "Something Went Wrong")

            return redirect("sellerDash")
    else:
        return redirect("home")

def buyproducts(request):
    return redirect(request,'products/ecommerceIndex.html')

def profile(request):
    if request.method == "POST" and request.user.is_authenticated:
        name = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST.get('password','')
        confirmpassword = request.POST.get('confirmpassword','')

        if password != "":
            if password == confirmpassword:
                request.user.password = make_password(password)

            else:
                messages.error(request,'Password and Confirm Password not matched')
                return redirect('profile')
        request.user.fullname = name
        request.user.username = username
        request.user.email = email
        request.user.save()

        if password != "":
            update_session_auth_hash(request, request.user)
        messages.success(request,"Your Profile is updated successfully")
        return redirect("profile")

    return render(request,'products/sellerProfile.html')

def getProduct(request,id):
    try:
        product = item.objects.get(id=id)
        serialized_product = serializers.serialize('json',[product])
        sizes = product.get_size()
        colors = product.get_color()
        categories = category.objects.all()
        categories_serialized = serializers.serialize('json', list(categories), fields=('name', 'id'))
        return JsonResponse({'msg':'success','item':serialized_product,'sizes':sizes,'colors':colors,'categories':categories_serialized})
    except:
        return JsonResponse({'msg':'error'})

def updateProduct(request,id):
    if request.user.is_authenticated:
        if request.user.role == "seller":
            if item.objects.get(id=id).seller == request.user:

                    name = request.POST['name']
                    price = request.POST['price']
                    offer = request.POST['offer']
                    it_category = request.POST['category']
                    quantity = request.POST['quantity']

                    description = request.POST['description']
                    sizes = request.POST.getlist('size[]')
                    colors = request.POST.getlist('color[]')

                    prod = get_object_or_404(item,id=id)
                    if prod:
                        prod.name = name
                        prod.price = price
                        prod.offer_price = offer
                        prod.item_category= category.objects.get(id=it_category)
                        prod.quantity =quantity
                        prod.description = description
                        print(request.FILES['image'])
                        if request.FILES['image'] != '':
                            prod.image = request.FILES.get('image')

                        else:
                            prod.image = prod.image
                        prod.save()

                    if sizes[0] != '':
                        sizes = set(sizes)
                        item_size.objects.filter(item=prod).delete()

                        for size in sizes:
                             it_size = item_size(size=size,item=prod)
                             it_size.save()
                    if colors[0] != '':
                        colors = set(colors)
                        item_color.objects.filter(item=prod).delete()
                        for color in colors:
                            it_color = item_color(color=color, item=prod)
                            it_color.save()
                    messages.success(request, "Your Product is Updated successfully")

            else:
                messages.error(request,"Product which you are trying to update is not your product")
            return redirect('sellerDash')
        else:
            messages.warning(request,'You are not approved seller')
            return redirect("home")
    else:
        messages.error(request,'Please make login first')
        return redirect("login")


def buyproducts(request):
    all_items = item.objects.order_by("-created_at").all()


    if 'cat_id' in request.GET:
        id = request.GET['cat_id']
        all_items = all_items.filter(item_category=category.objects.get(id=id))

    paginator = Paginator(all_items, 15)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)

    all_categories = category.objects.all()
    return render(request,'products/index.html',{'all_items':paged_items,'all_categories':all_categories})