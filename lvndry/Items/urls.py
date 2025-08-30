from django.urls import path
from .views import ItemAdd , ItemEdit , ItemDelete


urlpatterns = [
    path('ItemAdd/', ItemAdd.as_view() , name='ItemAdd'),
    path('ItemEdit/', ItemEdit.as_view() , name='ItemEdit'),
    path('ItemDelete/', ItemDelete.as_view() , name='ItemDelete'),

]