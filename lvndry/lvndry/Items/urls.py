from django.urls import path
from .views import (
    ServicesManagment , ClothesManagment , ExtraServicesManagment , DiscountManagment , DeletedItems , OrderPageData 
)
urlpatterns = [
    path('services/', ServicesManagment.as_view()),
    path('services/<int:id>/', ServicesManagment.as_view()),

    path('clothes/', ClothesManagment.as_view()),          
    path('clothes/<int:id>/', ClothesManagment.as_view()), 

    path('extraservices/', ExtraServicesManagment.as_view()),         
    path('extraservices/<int:id>/', ExtraServicesManagment.as_view()),  

    path('discounts/', DiscountManagment.as_view()),          
    path('discounts/<int:id>/', DiscountManagment.as_view()), 


    path('deleteditems/', DeletedItems.as_view() , name='deleteditems'),
    path('orderpagedata/', OrderPageData.as_view() , name='orderpagedata'),
]