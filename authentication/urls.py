from django.urls import path
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    path('workers/', UserListCreateView.as_view(), name='user-list-create'),
    path('workers/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
]
