from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [

  path('',AccountViews.vendorDashboard,name='vendor')  ,
  path('profile/',views.v_profile,name='v_profile'),
  path('menu_builder/',views.menu_builder,name='menu_builder'),
  path('menu_builder/category/<int:pk>/',views.fooditem_by_category,name='fooditem_by_category'),

  #crud category

  path('menu_builder/category/add/',views.add_category,name='add_category'),
  path('menu_builder/category/edit/<int:pk>/',views.edit_category,name='edit_category'),
  path('menu_builder/category/delete/<int:pk>/',views.delete_category,name='delete_category'),



]