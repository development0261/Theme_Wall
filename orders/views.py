from django.shortcuts import render

# Create your views here.
def ordersIndex(request):
    pass

def cart(request):
    return render(request,'products/cartPage.html')