"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from marketplace import views
from django.conf import settings
from django.conf.urls.static import static
from market import views as marketviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('accounts/',include('accounts.urls')),
    path('menu/',include('menu.urls')),
    path('market/',include('market.urls')),
    path('vendor/',include('vendor.urls')),
    path('customer/',include('customers.urls')),
    path('orders/',include('orders.urls')),

    #checkout
    path('checkout/',marketviews.checkout,name='checkout'),
    #cart
    path('cart/',marketviews.cart,name='cart'),
    #search
    path('search/',marketviews.search,name='search'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

