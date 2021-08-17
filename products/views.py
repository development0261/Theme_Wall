import random
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from users.models import Address
from .models import category,item,item_size,item_color,item_qty
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


                name = request.POST['name']
                price = request.POST['price']
                offer = request.POST['offer']
                if offer == '':
                    offer = 0
                it_category = request.POST['category']
                qtys = request.POST.getlist('qty[]')
                image = request.FILES['image']
                serial_no = request.POST['serial_no']
                rating = request.POST['rating']
                description = request.POST['description']
                sizes = request.POST.getlist('size[]')
                colors = request.POST.getlist('color[]')

                print(name, price, offer, category, image, sizes, colors)

                prod = item(serial_no=serial_no,name=name, price=price, offer_price=offer,
                            item_category=category.objects.get(id=it_category),
                            image=image, description=description, seller=request.user,rating=rating)
                prod.save()

                added_sizes = []
                added_colors = []
                if sizes[0] != '':

                    if 'No_Size' not in sizes:
                        for size in sizes:
                            if not item_size.objects.filter(size=size, item=prod).exists():
                                it_size = item_size(size=size, item=prod)
                                it_size.save()
                                added_sizes.append(it_size)
                            else:
                                it_size = item_size.objects.get(size=size, item=prod)
                                added_sizes.append(it_size)
                    else:
                        it_size = item_size(size="No_Size", item=prod)
                        it_size.save()
                        for size in sizes:
                            added_sizes.append(it_size)

                if colors[0] != '':
                    colors = set(colors)
                    for color in colors:
                        it_color = item_color(color=str(color).lower(), item=prod)
                        it_color.save()
                        added_colors.append(it_color)

                if qtys[0] != '':
                    for i in range(0,len(qtys)):
                        if not item_qty.objects.filter(product= prod,size=added_sizes[i],color=added_colors[i]).exists():
                            prod_qty =  item_qty(quantity=qtys[i],product= prod,size=added_sizes[i],color=added_colors[i])
                            prod_qty.save()
                messages.success(request, "Your Product is added successfully")

                # messages.error(request, "Something Went Wrong")

        return redirect("sellerDash")
    else:
        return redirect("home")


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
        things = item_qty.objects.filter(product=product)
        things_list = []
        for thing in things:
            things_list.append({
                'color': thing.color.color,
                'size': thing.size.size,
                'qty': thing.quantity
            })
        categories_serialized = serializers.serialize('json', list(categories), fields=('name', 'id'))
        return JsonResponse({'msg':'success','item':serialized_product,'sizes':sizes,'colors':colors,'categories':categories_serialized,'things_list':things_list})
    except:
        return JsonResponse({'msg':'error'})

def updateProduct(request,id):
    if request.user.is_authenticated:
        if request.user.role == "seller":
            if item.objects.get(id=id).seller == request.user:

                    name = request.POST['name']
                    price = request.POST['price']
                    offer = request.POST['offer']
                    if offer == '':
                        offer = 0
                    it_category = request.POST['category']
                    qtys = request.POST.getlist('qty[]')
                    serial_no = request.POST['serial_no']

                    description = request.POST['description']
                    sizes = request.POST.getlist('size[]')
                    colors = request.POST.getlist('color[]')

                    prod = get_object_or_404(item,id=id)
                    if prod:
                        prod.name = name
                        prod.serial_no = serial_no
                        prod.price = price
                        prod.offer_price = offer
                        prod.item_category= category.objects.get(id=it_category)

                        prod.description = description

                        try:
                            if 'image' in request.FILES:
                                prod.image = request.FILES.get('image')

                            else:
                                prod.image = prod.image
                        except:
                            pass
                        prod.save()

                    added_sizes = []
                    added_colors = []
                    if sizes[0] != '':
                        item_size.objects.filter(item=prod).delete()
                        if 'No_Size' not in sizes:
                            for size in sizes:
                                if not item_size.objects.filter(size=size, item=prod).exists():
                                    it_size = item_size(size=size, item=prod)
                                    it_size.save()
                                    added_sizes.append(it_size)
                                else:
                                    it_size = item_size.objects.get(size=size, item=prod)
                                    added_sizes.append(it_size)
                        else:

                                it_size = item_size(size="No_Size", item=prod)
                                it_size.save()
                                for size in sizes:
                                    added_sizes.append(it_size)

                    if colors[0] != '':
                        colors = set(colors)
                        item_color.objects.filter(item=prod).delete()
                        for color in colors:
                            it_color = item_color(color=str(color).lower(), item=prod)
                            it_color.save()
                            added_colors.append(it_color)
                    if qtys[0] != '':
                        for i in range(0, len(qtys)):
                            if not item_qty.objects.filter(product=prod, size=added_sizes[i],
                                                           color=added_colors[i]).exists():
                                prod_qty = item_qty(quantity=qtys[i], product=prod, size=added_sizes[i],
                                                    color=added_colors[i])
                                prod_qty.save()
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
    all_items = item.objects.filter(is_available= True)
    if 'cat_id' in request.GET:
        id = request.GET['cat_id']
        all_items = all_items.filter(item_category=category.objects.get(id=int(id)))

    if 'filter' in request.GET:
        filter = request.GET['filter']
        if filter == 'latest':
            all_items = all_items.order_by('-created_at')
        elif filter == 'highest':
            all_items = all_items.order_by('-price')
        elif filter == 'lowest':
            all_items = all_items.order_by('price')

    if 'color' in request.GET:
        all_items = all_items.filter(color__color="#"+request.GET['color'])

    searched = None
    if request.method == "POST":
        searched = request.POST['searchBox']
        if str(searched).strip() != '':
            all_items = all_items.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        else:
            all_items = []


    paginator = Paginator(all_items, 15)
    page = request.GET.get('page')
    paged_items = paginator.get_page(page)

    all_categories = item.objects.all().values_list('item_category__pk','item_category__name').distinct()

    colors = item_color.objects.all().values_list('color',flat=True).distinct()
    colors_to_send = []
    # for color in colors:
    #     colors_to_send.append(webcolors.rgb_to_name(webcolors.hex_to_rgb(color)))

    return render(request,'products/index.html',{'all_items':paged_items,'all_categories':all_categories,'colors':colors,'searched':searched})

def singleProduct(request,id):

        single_item = get_object_or_404(item, id=id)
        from .models import category
        if 'cat_id' in request.GET:
            id = request.GET['cat_id']
            category = category.objects.get(pk=id).name
        return render(request, 'products/singleProduct.html', {"product": single_item,'category':category})


def buyerprofile(request):
    if request.method == "POST" and request.user.is_authenticated:
        name = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST.get('password','')
        confirmpassword = request.POST.get('confirmpassword','')
        city = request.POST['city']
        state = request.POST['state']
        contact = request.POST['contact']
        zip = request.POST['zip']
        country = request.POST['country']
        address = request.POST['address']


        if password != "":
            if password == confirmpassword:
                request.user.password = make_password(password)

            else:
                messages.error(request,'Password and Confirm Password not matched')
                return redirect('profile')
        request.user.fullname = name
        request.user.username = username
        request.user.email = email
        request.user.contact_no = contact
        request.user.save()
        address1 = Address.objects.filter(user=request.user).last()
        address1.city=city
        address1.state = state
        address1.country = country
        address1.pincode = zip
        address1.address = address
        address1.save()


        if password != "":
            update_session_auth_hash(request, request.user)
        messages.success(request,"Your Profile is updated successfully")
        return redirect("buyerprofile")


    address = Address.objects.filter(user=request.user).last()
    return render(request,'products/buyerProfile.html',{'address':address})

def checkwebcam(request):
    if request.method == 'POST':
        imageName = request.POST['ImageName']
        imageName = imageName.split(',')[1]
        import base64
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.b64decode(imageName))
    return render(request,'products/testWebcam.html')



def getColorBySize(request,size,id):
    try:
        product = item.objects.get(pk=id)
        things = item_qty.objects.filter(product=product,size__size__iexact=size)

        colors= []
        for thing in things:
            colors.append({
                'color':thing.color.color[1:],
                'qty':thing.quantity
            })
        return JsonResponse({'msg':'success','colors':colors})
    except:
        return JsonResponse({'msg':'error'})

