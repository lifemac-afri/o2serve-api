from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from notifications_service.notify import notify_new_order, notify_order_assigned
from .utils import assign_waiter_to_order

class OrderListCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        self.permission_classes = [IsAuthenticated]
        try:
            orders = Order.objects.all().order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"error {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=OrderCreateSerializer)
    def post(self, request):
        self.permission_classes = [AllowAny]
    
        serializer = OrderCreateSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            order = serializer.save()
            # print(f"table number {order.table.table_number}")
            assigned_waiter = assign_waiter_to_order(order)
            if assigned_waiter:
                notify_order_assigned(order.order_number, assigned_waiter.username)
            response_serializer = OrderSerializer(order)
            print(f"response serializer {response_serializer}")
            notify_new_order(response_serializer.data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        print(f"pk {pk}")
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None
    
    def get(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        if order is None:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
