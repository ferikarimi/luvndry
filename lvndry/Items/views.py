from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Items
from .serializers import AllItemsSerializer , ItemAddSerializer , ItemEditSerializer 




class AllItems (APIView):
    def get (self , request):
        items = Items.objects.all().order_by('-name')
        serializer = AllItemsSerializer (items , many=True)
        return Response (serializer.data , status=200)


class ItemAdd (APIView):
    def post(self,request):
        serializer = ItemAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data , status=201)
        return Response (serializer.errors , status=400)


class ItemEdit (APIView):

    def patch (self , request , name):
        try :
            item = Items.objects.get(name=name)
        except Items.DoesNotExist :
            return Response(f"ERROR : item '{name}' does not exists!")
        
        serializer = ItemEditSerializer(item , data=request.data , partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=200)
        return Response(serializer.errors , status=400)


class ItemDelete (APIView):

    def delete (self , request , name):
        try :
            item = Items.objects.get(name=name)
            item.delete()
            return Response (f"MESSAGE : item '{item.name}' deleted successfully." , status=200)
        except Items.DoesNotExist :
            return Response (f"ERROR :  item '{name}' does not exists!" , status=404)