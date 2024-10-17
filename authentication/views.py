from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Worker
User = get_user_model()


class UserListCreateView(APIView):
    # Apply different permissions for GET and POST
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes=[AllowAny]
    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user = User.objects.get(username=user)
            if user.role == 'waiter':
                user.is_logged_in = True
                user.save()
                Worker.objects.get_or_create(user=user)
                
            user_serializer = UserSerializer(user)
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Login successful",
                "user":  user_serializer.data,
                "accessToken": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkerLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'waiter':
            return Response({"error": "Only waiters can log out as workers"}, status=status.HTTP_403_FORBIDDEN)
        
        user.is_logged_in = False
        user.save()
        return Response({"message": "Worker logged out successfully"}, status=status.HTTP_200_OK)

class WorkerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        workers = User.objects.filter(role='waiter', is_logged_in=True)
        serializer = UserSerializer(workers, many=True)
        return Response(serializer.data)
