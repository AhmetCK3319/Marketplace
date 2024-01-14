from django.shortcuts import render,redirect
from .forms import UserRegisterForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.
def userRegister(request):
    if request.user.is_authenticated:
        messages.warning(request,'Zaten giriş yaptınız.')
        return redirect('myAccount')
    elif request.method == 'POST':
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
            password = form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'Tebrikler hesabınız başarıyla oluşturuldu.')
            return redirect('login')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        'form':form,
        }   
    return render(request,'accounts/userRegister.html',context)

def vendorRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor_license = v_form.cleaned_data['vendor_license']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,'Tebrikler hesabınız başarıyla oluşturuldu. Lütfen yönetici onayı bekleyiniz.Kaydınız onaylandığında giriş yapabilirsiniz.')
            return redirect('vendorRegister')
        else:
            print('Form is not valid')
            print(form.errors)
            print(v_form.errors)
    else:
        form = UserRegisterForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form,
        }
    return render(request,'accounts/vendorRegister.html',context)   

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'Zaten giriş yaptınız.')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Giriş başarılı')
            return redirect('myAccount')
        else:
            messages.error(request,'Şifre veya email yanlış, lütfen tekrar deneyiniz.')
            return redirect('login')
        
    return render(request,'accounts/login.html')



def logout(request):
    auth.logout(request)
    messages.info(request,'Çıkış başarılı')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')

