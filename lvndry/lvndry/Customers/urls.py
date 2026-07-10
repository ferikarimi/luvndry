from django.urls import path
from django.views.generic import TemplateView

from .views import (
    CustomerRegister , CustomerUpdateProfile ,CustomerCommentsCreate ,  AdminCommentList , AdminCommentStatus , CommentRecently , AllCustomers , CustomerDelete , CustomerLevel
)


urlpatterns = [
    path('customerregister/', CustomerRegister.as_view() , name='CustomerRegister'),
    path('customerupdateprofile/', CustomerUpdateProfile.as_view() , name='customerUpdateProfile'),
    path('delete/<int:code>/', CustomerDelete.as_view() , name='CustomerDelete'),
    path('customercommentscreate/', CustomerCommentsCreate.as_view() , name='CustomerCommentsCreate'),
    path('admincommentlist/', AdminCommentList.as_view() , name='AdminCommentList'),
    path('admincommentstatus/<int:pk>/', AdminCommentStatus.as_view() , name='AdminCommentStatus'),
    path('commentrecently/', CommentRecently.as_view() , name='CommentRecently'),
    path('allcustomers/', AllCustomers.as_view() , name='allcustomers'),
    path('customerlevel/', CustomerLevel.as_view() , name='customerlevel'),
]