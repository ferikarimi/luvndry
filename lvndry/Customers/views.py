from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomerUpdateProfileSerializer , CustomerRegisterSerializer , CustomerInfoSerializer , CommentCreateSerializer , CommentAdminSerializer , CommentRecentlySerializer
from .models import Customers , Comments




class CustomerRegister(APIView):
    def post (self , request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status=201)
        return Response (serializer.errors , status=400)
    

class CustomerUpdateProfile (APIView):
    # def get (self , request):
    #     customer = request.customer
    #     serializer = CustomerUpdateProfileSerializer(customer)
    #     return Response(serializer.data , status=200)

    def patch (self , request):
        code = request.data.get('code')
        phone = request.data.get('phone')

        if code :
            customer = get_object_or_404 (Customers , code=code)
        elif phone :
            customer = get_object_or_404 (Customers , phone=phone)
        else :
            return Response({"ERROR : code or phone is required."} , status=400)

        serializer = CustomerUpdateProfileSerializer(customer , data=request.data ,  partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=200)


class CustomerFind (APIView):
    def get(self, request):
        code = request.GET.get('code')
        phone = request.GET.get('phone')

        if not code and not phone:
            return Response({"error": "phone or code is required."}, status=400)

        try:
            if code:
                customer = Customers.objects.get(code=code)
            else:
                customer = Customers.objects.get(phone=phone)
        except Customers.DoesNotExist:
            return Response({"error": "customer not found"}, status=404)

        serializer = CustomerInfoSerializer(customer)
        return Response(serializer.data)


class CustomerCommentsCreate (APIView):
    def post (self , request):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        
        serializer = CommentAdminSerializer (comment , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status=200)
        return Response (serializer.errors , status=400)
    


class CommentRecently (APIView):
    def get(self , request):
        recent_comments = Comments.objects.filter(status='approved').order_by('-created_at')[:4]
        serializer = CommentRecentlySerializer(recent_comments , many=True)
        return Response (serializer.data , status=200)