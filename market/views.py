from django.shortcuts import render,redirect
from vendor.models import Vendor,OpeningHour
from menu.models import Category, FoodItem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import JsonResponse,HttpResponse
from .models import Cart
from .context_processors import get_cart_counter,get_cart_amounts
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from datetime import date,datetime

# Create your views here.

def market(request):
    markets = Vendor.objects.filter(is_approved=True,user__is_active=True)[:10]
    market_count = markets.count()
    context = {
        'markets':markets,
        'market_count':market_count,
    }
    return render(request,'market/listining.html',context)

def market_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)

    # eğer foreignkey ile tek yönlü bir bağlantı var ise modelde related_name kullanarak viewde prefect related ile birbirlerine bağlayabiliyoruz ...
    
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True),
        )
    )
    # current day 
      #check current day's opening hours.
    date_today = date.today()
    today=date_today.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor,day=today)
   
    opening_hour = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items =None    

    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
        'opening_hour':opening_hour,
        'current_opening_hours':current_opening_hours,
    }
    return render(request,'market/market_detail.html',context)




def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                chkCart = None
                # Check if the food item is already in the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increase the cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except Cart.DoesNotExist:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added the food to the cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})

            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    



def decrease_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                
                # Check if the food item is already in the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1 :
                    #decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0    
                    return JsonResponse({'status': 'success', 'cart_counter':get_cart_counter(request),'qty' : chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except Cart.DoesNotExist:
                    Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Failed', 'message': 'you do not have this item in your cart !','cart_counter':get_cart_counter(request),'cart_amount':get_cart_amounts(request)})

            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    


login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user = request.user).order_by('created_at')
    context={
        'cart_items':cart_items,
        }
    return render(request,'market/cart.html',context)




def delete_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #check if the cart item exists
                cart_item = Cart.objects.get(user = request.user, id=food_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'success','message':'Cart item has been deleted!!!','cart_counter':get_cart_counter(request)})
            except:
                return JsonResponse({'status':'Failed','message':'Cart item does not exists !!'})          
        else:
            return JsonResponse({'status':'Failed','message':'İnvalid Request'})        
        


def search(request):
    address = request.GET['address']
    # latitude = request.GET['lat']
    # longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    fooditems = FoodItem.objects.filter(food_title__icontains = keyword,is_available = True).values_list('vendor',flat=True)
    vendors = Vendor.objects.filter(Q(id__in = fooditems) | Q(vendor_name__icontains = keyword, is_approved = True, user__is_active = True))
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request,'market/listining.html',context)      
      