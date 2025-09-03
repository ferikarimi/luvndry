from django.shortcuts import render

# Create your views here.


def home_page (request):
    return render (request , 'front/index.html')

def customer_home_page (request):
    return render (request , 'front/customerhome.html')



def customer_acceptance (request):
    return render (request , 'front/customer_acceptance.html')

def customer_management (request):
    return render (request , 'front/customer_management.html')

def order_management (request):
    return render (request , 'front/order_management.html')

def site_management (request):
    return render (request , 'front/site_management.html')

def laundry_management (request):
    return render (request , 'front/laundry_management.html')

def order_edit (request):
    return render (request , 'front/order_edit.html')