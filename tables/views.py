from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Table
from .serializers import TableSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class TableListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: TableSerializer(many=True)})
    def get(self, request):
        tables = Table.objects.all()
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=TableSerializer)
    def post(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Table.objects.get(pk=pk)
        except Table.DoesNotExist:
            return None

    def get(self, request, pk):
        table = self.get_object(pk)
        if table is None:
            return Response({"error": "Table not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    def put(self, request, pk):
        table = self.get_object(pk)
        if table is None:
            return Response({"error": "Table not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TableSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        table = self.get_object(pk)
        if table is None:
            return Response({"error": "Table not found"}, status=status.HTTP_404_NOT_FOUND)
        table.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
