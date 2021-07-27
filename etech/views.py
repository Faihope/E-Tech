from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib import messages
# Create your views here.
def index(request):

    return render(request,'index.html')

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