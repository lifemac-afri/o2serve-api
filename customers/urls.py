from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customers-list-create'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customers-detail'),
]
