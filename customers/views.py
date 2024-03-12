from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
from orders.models import Order,OrderedFood
import simplejson as json

# Create your views here.
login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_profile = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_profile.is_valid() and user_form.is_valid():
            user_profile.save()
            user_form.save()
            messages.success(request,'Profile Updated')
            return redirect('cprofile')
        else:
            print(user_profile.errors)
            print(user_form.errors)
    else:     
        user_profile = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'user_profile':user_profile,
        'user_form':user_form,
        'profile':profile,
    }

    return render(request,'customer/cprofile.html',context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=False).order_by('-created_at')

    context = {
        'orders':orders,
    }
    return render(request,'customer/my_orders.html',context)

def order_detail(request,order_number):
    try:
        order = Order.objects.get(order_number=order_number,is_ordered = False)
        food = OrderedFood.objects.filter(order=order)
        print(food)
    except:
        return redirect('customer')

    tax_data = json.loads(order.tax_data)
    print(tax_data)
    context = {
        'order':order,
        'food':food,
        'tax_data':tax_data,
    }    
    return render(request,'customer/order_detail.html',context)
    

    