from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer,ActivityLog
from .serializers import CustomerSerializer,VerifyOTPSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from random import randint
from .messenger import send_sms, verify_otp


class CustomerListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(responses={200: CustomerSerializer(many=True)})
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CustomerSerializer)
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            
            customer = serializer.save()
            otp = send_sms(phone=customer.phone_number)
            customer.otp = otp
            customer.save()
            ActivityLog.objects.create(activity=f"OTP sent successfully to {customer.phone_number}")
            return Response({
                "message": f"Customer created. OTP sent to   {customer.phone_number}.",
                "customer": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomerVerifyOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self, request):
        user_id = request.data.get('user_id')
        provided_otp = request.data.get('otp')
        
        print(f"User {user_id} provided OTP: {provided_otp}")
        
        try:
            customer = Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Call the verify_otp function
        is_valid_otp = verify_otp(provided_otp, customer.phone_number)
        
        if is_valid_otp:
            customer.is_verified = True  # Update the verified status
            customer.save()
            return Response({"message": "Customer verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        if customer is None:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)