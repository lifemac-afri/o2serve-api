from django.urls import path
from .views import UserListCreateView, UserDetailView,UserLoginView

urlpatterns = [
    path('workers/', UserListCreateView.as_view(), name='user-list-create'),
    path('workers/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('workers/login/', UserLoginView.as_view(), name='user-login'),
]
