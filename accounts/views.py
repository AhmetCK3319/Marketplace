from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from .models import User
from django.contrib import messages

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # user oluşturmak için form methodu kullanıldı
            # user=form.save(commit=False)
            # user.role = User.COSTUMER
            # user.save()

            # user oluşturmak için model methodu kullanıldı
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'Tebrikler hesabınız başarıyla oluşturuldu.')
            return redirect('userRegister')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        'form':form,
        }   
    return render(request,'accounts/userRegister.html',context)