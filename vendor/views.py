from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from accounts.forms import UserProfileForm
from menu.forms import CategoryForm, FoodItemForm 
from .forms import VendorForm ,OpeningHourForm
from accounts.models import UserProfile
from .models import Vendor,OpeningHour
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from .utils import get_vendor
from  django.template.defaultfilters import slugify



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


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditem_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'fooditems':fooditems,
        'category':category,
        }
    return render(request,'vendor/fooditem_by_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)

            category.save() #here teh category id will be generated
            category.slug =slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request,'category added successfuly.')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
            'form':form,
        }
    return render(request,'vendor/category/add_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug =slugify(category_name)
            form.save()
            messages.success(request,'category updated successfuly.')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
            'form':form,
            'category':category,
        }
    return render(request,'vendor/category/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'category has been deleted successfuly.')
    return redirect('menu_builder')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug =slugify(food_title)
            form.save()
            messages.success(request,'FoodItem added successfuly!')
            return redirect('fooditem_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        #modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
            'form':form,
        }
    return render(request,'vendor/food/add_food.html',context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    fooditem = get_object_or_404(FoodItem,pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES,instance=fooditem)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug =slugify(food_title)
            form.save()
            messages.success(request,'FoodItem updated successfuly!')
            return redirect('fooditem_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=fooditem)
        #modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
            'form':form,
            'fooditem':fooditem,
        }
    return render(request,'vendor/food/edit_food.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request,pk=None):
    fooditem = get_object_or_404(FoodItem,pk=pk)
    fooditem.delete()
    messages.success(request,'fooditem has been deleted successfuly.')
    return redirect('fooditem_by_category',fooditem.category.id)

def opening_hours(request):

    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()

    context = {
        'form':form,
        'opening_hours':opening_hours,
    }

    return render(request,'vendor/opening_hours.html',context)

def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method =='POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')

            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request),day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                if hour:
                    day = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status':'success','id':hour.id,'day':day.get_day_display(),'is_closed':'closed'}
                    else:
                        response = {'status':'success','id':hour.id,'day':day.get_day_display(),'from_hour':hour.from_hour,'to_hour':hour.to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status':'Failed','message':from_hour+'-'+to_hour+'already exists for this day!','error':str(e)}
                return JsonResponse(response) 
        else:
            HttpResponse('invalid request')    


def remove_opening_hours(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' :
            hour = get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({'status':'success','id':pk})