from django.urls import path
from .views import OrderCreate , OrderUpdate , OrderTracking , OrderDelete , OrderRecent , OrderStatusUpdate , OrderStatusChoices , order_edit

urlpatterns = [
    path('ordercreate/', OrderCreate.as_view() , name='OrderCreate'),
    path('orderupdate/<int:pk>/', OrderUpdate.as_view() , name='OrderUpdate'),
    path('orderdelete/<int:pk>/', OrderDelete.as_view() , name='OrderDelete'),
    path('ordertracking/', OrderTracking.as_view() , name='OrderTracking'),
    path('orderrecent/', OrderRecent.as_view() , name='orderrecent'),
    path('orderstatusupdate/<int:pk>/', OrderStatusUpdate.as_view() , name='orderstatusupdate'),
    path('orderstatuschoices/', OrderStatusChoices.as_view() , name='orderstatuschoices'),

    path('editpage/<int:pk>/', order_edit , name='order_edit'),


]