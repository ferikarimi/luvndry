from django.urls import path
from django.shortcuts import render
from .views import (
    order_edit ,edit_order_page , recent_orders_page , home_page , admin_home_page , customer_acceptance , customer_management , site_management , laundry_management , customer_order , recent_orders_page , edit_order_page , magazine_detail , add_magazine , customer_edit
)


urlpatterns = [
    path('', home_page , name='home' ),
    path('editpage/<int:pk>/', order_edit , name='order_edit'),
    path('edit_order_page/<int:pk>/', edit_order_page , name='order_edit'),
    path('recent_orders_page/', recent_orders_page , name='order_edit'),
    path('admin_home_page', admin_home_page , name='admin_home_page' ),
    path('customer_acceptance', customer_acceptance , name='customer_acceptance' ),
    path('customer_management', customer_management , name='customer_management' ),
    path('site_management', site_management , name='site_management' ),
    path('laundry_management', laundry_management , name='laundry_management' ),
    path('customer_order/', customer_order , name='customer_order' ),
    path("recent_orders/", recent_orders_page, name="recent_orders"),
    path("order_edit/<int:order_id>/", edit_order_page, name="edit_order"),
    path('add_magazine/', add_magazine, name='add_magazine'),
    path('magazine/<int:id>/', magazine_detail, name='magazine_detail'),
    path('customer_edit/', customer_edit, name='customer_edit'),

]