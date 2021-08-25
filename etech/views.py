from etech.models import Customer, Order, OrderItem, Product,Profile
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout as dj_login
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required




# Create your views here.
def index(request):
    if request.user.is_authenticated:
        try:

            customer=request.user.customer
        except ObjectDoesNotExist:

            customer = Customer.objects.create(user=request.user)
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    products=Product.objects.all()

    #search code
    item_name=request.GET.get('item_name')
    if item_name!='' and item_name is not None:
        products=products.filter(name__icontains=item_name)
    context={'products':products,'cartItems':cartItems}

    return render(request,'index.html',context)

def registeruser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!. Check out our Email later :)')

            return redirect('loginuser')
    else:
        form = CreateUserForm
    context = {
            
            'form':form,
                        }

    return render(request,'registration/register.html',context)

def loginpage(request):
    if request.user.is_authenticated:

            return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')

      
    return render(request,'registration/login.html')

def logoutuser(request):
    
    return redirect(reverse('loginuser'))

@login_required(login_url='login')
def detail(request,id):
    product_object=Product.objects.get(id=id)
    return render(request,'details.html',{'product_object':product_object})


def checkout(request):
    if request.user.is_authenticated:

        try:

            customer=request.user.customer
        except ObjectDoesNotExist:

            customer = Customer.objects.create(user=request.user)

        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']

    return render(request,'checkout.html',{'items':items,'order':order,'cartItems':cartItems})


def cart(request):
    if request.user.is_authenticated:
        try:

            customer=request.user.customer
        except ObjectDoesNotExist:

            customer = Customer.objects.create(user=request.user)

        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems=order['get_cart_items']
    return render(request,'cart.html',{'items':items,'order':order,'cartItems':cartItems})


def updateItem(request):
    data=json.loads(request.data)
    productId=data['productId']
    action=data['action']
    print('Action:',action)

    customer=request.user.customer
    customer = Customer.objects.create(user=request.user)

    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)


    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product,complete=False)
    if action =='add':
        orderItem.quantity=(orderItem.quantity + 1)

    elif action =='remove':
        orderItem.quantity=(orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)

@login_required(login_url='login')
def profile(request,id):
    profile_data = User.objects.get(id=id)
    current_user = request.user
    if request.method =='POST':
        profile=ProfileUpdateForm(request.POST,request.FILES,instance=current_user.profile)
        if profile.is_valid():
            messages.success(request,'Your profile has been updated!')
            return redirect('profile')
    else:
        profile=ProfileUpdateForm(instance=request.user)
    context={"profile":profile,"current_user": current_user,"profile_data":profile_data}
    return render(request, 'profile.html',context)

@login_required(login_url='login')
def updateprofile(request):
    current_user = request.user
    profile=Profile.objects.all()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES) 

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'updateprofile.html',{"form": form ,'profile':profile,'current_user':current_user} )