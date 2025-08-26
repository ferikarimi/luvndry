from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerUpdateProfileSerializer , CustomerRegisterSerializer , CustomerInfoSerializer , CommentCreateSerializer , CommentAdminSerializer
from .models import Customers , Comments



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


class CustomerCommentsCreate (APIView):
    def post (self , request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save()
            return Response ({"MESSAGE : Your comment has been submitted and will be displayed after approval."} , status=201)
        return Response (serializer.errors , status=400)


class AdminCommentList (APIView):
    def get (self , request):
        comments = Comments.objects.all().order_by('-created_at')
        serializer = CommentAdminSerializer(comments , many=True)
        return Response (serializer.data , status=200)
    

class AdminCommentStatus (APIView):
    def patch (self , request , pk):
        try :
            comment = Comments.objects.get(id=pk)
        except Comments.DoesNotExist :
            return Response ({"ERROR : comment not found!"} , status=404)
        
        serilizer = CommentAdminSerializer (comment , data=request.data , partial=True)
        if serilizer.is_valid():
            serilizer.save()
            return Response (serilizer.data , status=200)
        return Response (serilizer.errors , status=400)