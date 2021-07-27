from etech.models import Product
from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout as dj_login
from django.urls import reverse

# Create your views here.
def index(request):
    products=Product.objects.all()

    #search code
    item_name=request.GET.get('item_name')
    if item_name!='' and item_name is not None:
        products=products.filter(name__icontains=item_name)
    context={'products':products}

    return render(request,'index.html',context)

def registeruser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!. Check out our Email later :)')

            return redirect('login')
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
    
    return redirect(reverse('login'))


def detail(request,id):
    product_object=Product.objects.get(id=id)
    return render(request,'details.html',{'product_object':product_object})
