from django.urls import path
from .views import MenuItemListCreateView, MenuItemDetailView, CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<uuid:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),
     path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
