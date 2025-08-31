from django.urls import path
from .views import CustomerRegister , CustomerUpdateProfile ,CustomerFind,CustomerCommentsCreate ,  AdminCommentList , AdminCommentStatus , CommentRecently


urlpatterns = [
    path('customerregister/', CustomerRegister.as_view() , name='CustomerRegister'),

    path('customerupdateprofile/', CustomerUpdateProfile.as_view() , name='customerUpdateProfile'),

    path('customerfind/', CustomerFind.as_view() , name='CustomerFind'),

    path('customercommentscreate/', CustomerCommentsCreate.as_view() , name='CustomerCommentsCreate'),

    path('admincommentlist/', AdminCommentList.as_view() , name='AdminCommentList'),

    path('admincommentstatus/<int:pk>/', AdminCommentStatus.as_view() , name='AdminCommentStatus'),
    
    path('commentrecently/', CommentRecently.as_view() , name='CommentRecently'),

]