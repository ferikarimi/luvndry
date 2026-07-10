from django.contrib.admin import AdminSite
from django.contrib import admin
from CMS.models import GalleryImage
from Customers.models import Customers, Comments , CustomerLevel
from Items.models import Clothes, Services, ExtraServices, Discount
from Orders.models import Orders, OrderItems

from Items.admin import ClothesAdmin, ServicesAdmin, ExtraServicesAdmin, DiscountAdmin
from Orders.admin import OrderItemsAdmin , OrdersAdmin
from CMS.admin import GalleryImageAdmin , MagazineArticleAdmin , MagazineArticle , Notification , NotificationAdmin
from Customers.admin import CustomersAdmin , CommentsAdmin, CustomerLevelAdmin


class SuperUserAdminSite(AdminSite):
    site_header = "پنل مدیریتی سایت"
    site_title = "Admin"
    index_title = "داشبورد مدیریت"

    def has_permission(self, request):
        """فقط کاربرانی که فعال و سوپر‌یوزر هستند می‌توانند وارد شوند."""
        return request.user.is_active and request.user.is_superuser


superuser_admin_site = SuperUserAdminSite(name='superuser_admin')

superuser_admin_site.register(GalleryImage, GalleryImageAdmin)
superuser_admin_site.register(MagazineArticle, MagazineArticleAdmin)
superuser_admin_site.register(Notification, NotificationAdmin)

superuser_admin_site.register(Customers , CustomersAdmin)
superuser_admin_site.register(Comments , CommentsAdmin)
superuser_admin_site.register(CustomerLevel, CustomerLevelAdmin)
superuser_admin_site.register(Clothes, ClothesAdmin)
superuser_admin_site.register(Services, ServicesAdmin)
superuser_admin_site.register(ExtraServices, ExtraServicesAdmin)
superuser_admin_site.register(Discount, DiscountAdmin)
superuser_admin_site.register(Orders , OrdersAdmin)
superuser_admin_site.register(OrderItems , OrderItemsAdmin)
