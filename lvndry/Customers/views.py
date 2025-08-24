from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerUpdateProfileSerializer , CustomerRegisterSerializer

# Create your views here.



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
    

class CustomerComments ():
    pass



