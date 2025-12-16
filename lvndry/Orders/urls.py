from django.urls import path
from .views import (
    OrderCreate , OrderManagment ,  OrderTracking , AllActiveOrdersList , OrderStatusUpdate , Stats , CustomerOrders , OrderDetail , CheckCustomer 
)



urlpatterns = [
    path('ordercreate/', OrderCreate.as_view() , name='ordercreate'),
    path('ordermanagment/<int:pk>/', OrderManagment.as_view() , name='ordermanagment'),
    path('ordertracking/', OrderTracking.as_view() , name='ordertracking'),
    path('allactiveorderslist/', AllActiveOrdersList.as_view() , name='allactiveorderslist'),
    path('orderstatusupdate/<int:pk>/', OrderStatusUpdate.as_view() , name='orderstatusupdate'),
    path('stats/', Stats.as_view() , name='stats'),
    path('customerorders/<int:id>/', CustomerOrders.as_view() , name='customerorders'),
    path('detail/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
    path('checkcustomer/', CheckCustomer.as_view() , name='checkcustomer'),

]