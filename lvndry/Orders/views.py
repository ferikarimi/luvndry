from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrderUpdateSerializer , OrderCreateSerializer
from rest_framework.response import Response
from .models import Orders



class OrderCreate (APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrderUpdate (APIView):

    def patch (self , requset , pk):
        try :
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist :
            return Response({"ERROR : order can not found!"} , status=404)
        
        serilaizer = OrderUpdateSerializer(order , data=requset.data , partial=True)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response (serilaizer.data , status=200)
        return Response (serilaizer.errors , status=400)


class OrderDelete (APIView):
    def delete (self , request , pk):
        try :
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist :
            return Response ({"ERROR : order can not deleted. order not found!"} , status=404)
        order.delete()
        return Response({"MESSAGE : order deleted successfuly"} , status=204)

