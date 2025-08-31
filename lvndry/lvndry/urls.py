"""
URL configuration for lvndry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from conf.views import home_page , customer_home_page , customer_acceptance , customer_management , site_management , laundry_management , order_management


urlpatterns = [
    path('', home_page , name='home' ),
    path('customer_home_page', customer_home_page , name='customer_home_page' ),

    path('customer_acceptance', customer_acceptance , name='customer_acceptance' ),
    path('customer_management', customer_management , name='customer_management' ),
    path('site_management', site_management , name='site_management' ),
    path('laundry_management', laundry_management , name='laundry_management' ),
    path('order_management', order_management , name='order_management' ),



    path('admin/', admin.site.urls),
    path('customers/', include('Customers.urls')),
    path('items/', include('Items.urls')),
    path('orders/', include('Orders.urls')),

]