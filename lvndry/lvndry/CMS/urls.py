from django.urls import path
from .views import (
    GalleryImageListCreate, GalleryImageDetail , AdminMagazine , Magazine , NotificationListCreate , NotificationDetail , ShowLastNotif
)


urlpatterns = [
    path('gallery/', GalleryImageListCreate.as_view(), name='gallery_list_create'),
    path('gallery/<int:pk>/', GalleryImageDetail.as_view(), name='gallery_detail'),
    path('admin_magazines/', AdminMagazine.as_view(), name='admin_magazines'),
    path('magazines/', Magazine.as_view(), name='magazines'),
    path('notifications/', NotificationListCreate.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/', NotificationDetail.as_view(), name='notifications-detail'),
    path('showlastnotif/', ShowLastNotif.as_view(), name='showlastnotif'),

]