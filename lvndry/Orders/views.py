from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import OrderUpdateSerializer , OrderCreateSerializer , OrderTrackingSerializer , OrderListSerializer , OrderStatusUpdateSerializer
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
    def get(self , request , pk):
        try:
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return Response({"ERROR": f"order '{pk}' not found!"}, status=404)
        
        serializer = OrderUpdateSerializer(order)
        return Response(serializer.data, status=200)

    def patch (self , request , pk):
        try :
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist :
            return Response({f"ERROR : order '{pk}' can not found!"} , status=404)
        
        serilaizer = OrderUpdateSerializer(order , data=request.data , partial=True)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response (serilaizer.data , status=200)
        return Response (serilaizer.errors , status=400)




class OrderTracking (APIView):
    def post (self , request):
        serializer = OrderTrackingSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data , status=200)
        return Response (serializer.errors , status=400)
    




class OrderRecent(APIView):
    def get(self, request):
        orders = Orders.objects.all().order_by('-order_time')[:30]
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=200)
    

class OrderDelete (APIView):
    def delete (self , request , pk):
        try :
            order = Orders.objects.get(pk=pk)
            order.delete()
            return Response({"MESSAGE : order deleted successfuly"} , status=200)

        except Orders.DoesNotExist :
            return Response ({"ERROR : order can not deleted. order not found!"} , status=404)



class OrderStatusUpdate(APIView):
    def patch(self, request, pk):
        try:
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return Response({"error": f"Order {pk} does not exist."}, status=404)

        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Order {pk} status updated.", "data": serializer.data}, status=200)
        return Response(serializer.errors, status=400)


class OrderStatusChoices(APIView):
    def get(self, request):
        choices = [ {"value": c[0], "label": c[1]} for c in Orders.STATUS_CHOICE_FIELDS ]
        return Response(choices, status=200)


def order_edit(request, pk):
    # اینجا می‌توانید سفارش را با pk دریافت کنید
    order = Orders.objects.get(pk=pk)
    return render(request, 'front/order_edit.html', {'order': order})
