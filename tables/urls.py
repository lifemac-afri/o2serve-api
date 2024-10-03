from django.urls import path
from .views import TableListCreateView,TableDetailView

urlpatterns = [
    path('tables/', TableListCreateView.as_view(), name='table-list-create'),
    path('tables/<uuid:pk>/', TableDetailView.as_view(), name='table-detail'),
]
