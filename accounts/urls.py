from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.myAccount,name='myAccount'),
    path('userRegister/',views.userRegister,name='userRegister'),
    path('vendorRegister/',views.vendorRegister,name='vendorRegister'),

    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),

   
]