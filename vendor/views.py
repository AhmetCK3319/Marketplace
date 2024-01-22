from django.shortcuts import render,get_object_or_404,redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def v_profile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)
    if request.method == 'POST':
        user_profile = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_profile = VendorForm(request.POST,request.FILES,instance=vendor)
        if user_profile.is_valid() and vendor_profile.is_valid():
            user_profile.save()
            vendor_profile.save()
            messages.info(request,'settings updated.')
            return redirect('v_profile')
        else:
            print(user_profile.errors)
            print(vendor_profile.errors)
    else:
        user_profile = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_profile = VendorForm(request.POST,request.FILES,instance=vendor)
        
    context = {
        'user_profile':user_profile,
        'vendor_profile':vendor_profile,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/v_profile.html',context)

