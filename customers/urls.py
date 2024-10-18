from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView,CustomerVerifyOTPView, CustomerOrderUpdateView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customers-list-create'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customers-detail'),
    path('customers/verify/', CustomerVerifyOTPView.as_view(), name='customers-verify-otp'),
    path('customers/update-order/', CustomerOrderUpdateView.as_view(), name='customer-update-order'),
]
