from django.urls import path
from .views import OrderCreate , OrderUpdate , OrderDelete


urlpatterns = [
    path('ordercreate/', OrderCreate.as_view() , name='OrderCreate'),
    path('orderupdate/<int:pk>/', OrderUpdate.as_view() , name='OrderUpdate'),
    path('orderdelete/<int:pk>/', OrderDelete.as_view() , name='OrderDelete'),

]