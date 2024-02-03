from django.shortcuts import render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.http import JsonResponse,HttpResponse
from .models import Cart
from .context_processors import get_cart_counter

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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items =None    

    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request,'market/market_detail.html',context)




def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                
                # Check if the food item is already in the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'success', 'message': 'Increase the cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except Cart.DoesNotExist:
                    Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Added the food to the cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})

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
                    return JsonResponse({'status': 'success', 'cart_counter':get_cart_counter(request),'qty' : chkCart.quantity})
                except Cart.DoesNotExist:
                    Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Failed', 'message': 'you do not have this item in your cart !','cart_counter':get_cart_counter(request),})

            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist'})

        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})

