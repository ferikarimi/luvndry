from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerUpdateProfileSerializer , CustomerRegisterSerializer , CustomerInfoSerializer
from .models import Customers



class CustomerRegister(APIView):
    def post (self , request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status=201)
        return Response (serializer.errors , status=400)
    

class CustomerUpdateProfile (APIView):
    def get (self , request):
        customer = request.customer
        serializer = CustomerUpdateProfileSerializer(customer)
        return Response(serializer.data , status=200)

    def patch (self , request):
        customer = request.customer
        serializer = CustomerUpdateProfileSerializer(customer , data=request.data ,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=200)
        return Response(serializer.errors , status=400)


class CustomerFind (APIView):
    def get(self , request):
        code = request.GET.get('code')
        phone = request.GET.get('phone')

        if code :
            customer = Customers.objects.get(code=code)
        elif phone :
            customer = Customers.objects.get(phone=phone)
        else :
            return Response("ERROR : phone or code is required.", status=400)
        
        if not customer :
            return Response("ERROR : customer not found" , status=404)
        serializer = CustomerInfoSerializer(customer)
        return Response(serializer.data)


class CustomerComments ():
    pass