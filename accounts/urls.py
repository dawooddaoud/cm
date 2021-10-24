from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('',views.home ,name = 'home'),
    path('login/',views.loginPage ,name='login'),
    path('logout/',views.logoutUser ,name='logout'),
    path('register/',views.registerPage ,name='register'),
    path('user/', views.userPage , name = 'user'),
    path('account/',views.accountSettings ,name = 'account'),
    path('customer/<int:pk>', views.customer,name = 'customer'),
    path('products/', views.products,name='products'),
    path('create_order/<int:pk>', views.createOrder , name = 'create_order'),
    path('update_order/<int:pk>', views.updateOrder , name = 'update_order'),
    path('delete/<int:pk>', views.deleteOrder , name = 'delete'),
    path('done/', views.done, name = 'done'),
]