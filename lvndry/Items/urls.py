from django.urls import path
from .views import AllItems , ItemAdd , ItemEdit , ItemDelete


urlpatterns = [
    path('all/', AllItems.as_view() , name='AllItems'),
    path('add/', ItemAdd.as_view() , name='ItemAdd'),
    path('edit/<str:name>/', ItemEdit.as_view() , name='ItemEdit'),
    path('delete/<str:name>/', ItemDelete.as_view() , name='ItemDelete'),

]