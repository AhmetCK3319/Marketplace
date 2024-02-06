from django.urls import path
from . import views

urlpatterns = [
path('cart/',views.cart,name='cart'),
path('',views.market,name='market'),
path('<slug:vendor_slug>/',views.market_detail,name='market_detail'),
# add to cart
path('add_to_cart/<int:food_id>/',views.add_to_cart,name='add_to_cart'),
#decrease to cart
path('decrease_to_cart/<int:food_id>/',views.decrease_to_cart,name='decrease_to_cart'),
# delete cart item
path('delete_to_cart/<int:food_id>/',views.delete_to_cart,name='delete_to_cart'),

]

