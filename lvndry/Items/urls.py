from django.urls import path
from .views import AllServices , AllClothes, ServicesAdd , ServicesEdit , ServicesDelete , ClothesAdd , ClothesEdit , ClothesDelete


urlpatterns = [
    path('allservices/', AllServices.as_view() , name='AllItems'),
    path('allclothes/', AllClothes.as_view() , name='AllItems'),


    path('servicesadd/', ServicesAdd.as_view() , name='ItemAdd'),
    path('servicesedit/<str:name>/', ServicesEdit.as_view() , name='ItemEdit'),
    path('servicesdelete/<str:name>/', ServicesDelete.as_view() , name='ItemDelete'),

    path('clothesadd/', ClothesAdd.as_view() , name='ItemAdd'),
    path('clothesedit/<str:name>/', ClothesEdit.as_view() , name='ItemEdit'),
    path('clothesdelete/<str:name>/', ClothesDelete.as_view() , name='ItemDelete'),

]