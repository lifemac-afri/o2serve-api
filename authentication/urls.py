from django.urls import path
from .views import UserListCreateView, UserDetailView,UserLoginView, WorkerLogoutView, WorkerListView

urlpatterns = [
    path('workers/', UserListCreateView.as_view(), name='user-list-create'),
    path('workers/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('workers/login/', UserLoginView.as_view(), name='worker-login'),
    path('workers/logout/', WorkerLogoutView.as_view(), name='worker-logout'),
    path('workers/loggedin/', WorkerListView.as_view(), name='active-waiters'),
]
