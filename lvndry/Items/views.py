from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Clothes , Services
from .serializers import AllClothesSerializer , AllServicesSerializer , ServicesAddSerializer , ServicesEditSerializer , ClothesAddSerializer , ClothesEditSerializer 



class AllClothes (APIView):
    def get (self , request):
        clothes = Clothes.objects.all().order_by('-name')
        serializer = AllClothesSerializer (clothes , many=True)
        return Response (serializer.data , status=200)
    

class AllServices (APIView):
    def get (self , request):
        services = Services.objects.all().order_by('-name')
        serializer = AllServicesSerializer (services , many=True)
        return Response (serializer.data , status=200)


class ServicesAdd(APIView):
    def post(self, request):
        serializer = ServicesAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=40)


class ServicesEdit(APIView):
    def patch(self, request, name):
        try:
            item = Services.objects.get(name=name)
        except Services.DoesNotExist:
            return Response(
                {"error": f"Service '{name}' does not exist!"},
                status=404
            )

        serializer = ServicesEditSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ServicesDelete(APIView):
    def delete(self, request, name):
        try:
            item = Services.objects.get(name=name)
            item.delete()
            return Response(
                {"message": f"Service '{name}' deleted successfully."},
                status=200
            )
        except Services.DoesNotExist:
            return Response(
                {"error": f"Service '{name}' does not exist!"},
                status=404
            )


class ClothesAdd(APIView):
    def post(self, request):
        serializer = ClothesAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ClothesEdit(APIView):
    def patch(self, request, name):
        try:
            item = Clothes.objects.get(name=name)
        except Clothes.DoesNotExist:
            return Response(
                {"error": f"Cloth '{name}' does not exist!"},
                status=404
            )

        serializer = ClothesEditSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ClothesDelete(APIView):
    def delete(self, request, name):
        try:
            item = Clothes.objects.get(name=name)
            item.delete()
            return Response(
                {"message": f"Cloth '{name}' deleted successfully."},
                status=200
            )
        except Clothes.DoesNotExist:
            return Response(
                {"error": f"Cloth '{name}' does not exist!"},
                status=404
            )