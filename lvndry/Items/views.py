from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Items
from .serializers import ItemAddSerializer , ItemEditSerializer 



class ItemAdd (APIView):
    def post(self,request):
        serilaizer = ItemAddSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response (serilaizer.data , status=201)
        return Response (serilaizer.errors , status=400)


class ItemEdit (APIView):

    def patch (self , request , pk):
        try :
            item = Items.objects.get(pk=pk)
        except :
            return Response("ERROR : item can not edited. item does not exists!")
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
            return Response ("MESSAGE : item delete successfully." , status=204)
        except :
            return Response ("ERROR : item can not deleted. item does not exists!" , status=404)