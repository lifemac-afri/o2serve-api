from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView,CustomerVerifyOTPView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customers-list-create'),
    path('customers/<uuid:pk>/', CustomerDetailView.as_view(), name='customers-detail'),
    path('customers/verify/', CustomerVerifyOTPView.as_view(), name='customers-verify-otp'),
]
