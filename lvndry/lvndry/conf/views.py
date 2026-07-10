from django.shortcuts import render , get_object_or_404 , redirect
from CMS.models import GalleryImage , MagazineArticle
from Orders.models import Orders



"""
    این دکوراتور برای محافظ از صفحه های ادمین ساخته شده است
    اگه کاربری که درخواست داده است ادمین سایت نباشد ، به صفحه ی اصلی هدایت می شود
"""
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper



"""
    صفحه های عمومی سایت
"""
def home_page (request):
    gallery_images = GalleryImage.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'front/index.html', {
        'gallery_images': gallery_images,
    })


def magazine_detail(request, id):
    article = get_object_or_404(MagazineArticle, id=id, is_active=True)
    all_articles = MagazineArticle.objects.filter(is_active=True).order_by('-id')
    return render(request, 'front/magazine_detail.html', {'article': article, 'all_articles': all_articles})



"""
    صفحه های خصوصی سایت (مخصوص ادمین)
"""
@admin_required
def admin_home_page (request):
    return render (request , 'front/adminhome.html')


@admin_required
def customer_acceptance (request):
    return render (request , 'front/customer_acceptance.html')


@admin_required
def customer_management (request):
    return render (request , 'front/customer_management.html')


@admin_required
def site_management (request):
    return render (request , 'front/site_management.html')


@admin_required
def laundry_management (request):
    return render (request , 'front/laundry_management.html')


@admin_required
def order_edit (request):
    return render (request , 'front/order_edit.html')


@admin_required
def customer_order(request):
    return render(request , 'front/customer_order.html')


@admin_required
def recent_orders_page(request):
    return render(request, "front/recent_orders.html")


@admin_required
def edit_order_page(request, order_id):
    return render(request, "front/order_edit.html", {"order_id": order_id})


@admin_required
def order_edit(request, pk):
    order = Orders.objects.get(pk=pk)
    return render(request, 'front/order_edit.html', {'order': order})


@admin_required
def add_magazine(request):
    return render(request, "front/add_magazine.html")


@admin_required
def customer_edit(request):
    return render(request, "front/customer_edit.html")


def custom_404(request, exception):
    return render(request, "error_404/404.html", status=404)