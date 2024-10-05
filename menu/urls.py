from django.urls import path
from .views import MenuItemListCreateView, MenuItemDetailView, CategoryListCreateView, CategoryDetailView, CustomerCategoryListView, CustomerMenuItemListView

urlpatterns = [
    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<uuid:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),
     path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('customer-menu-items/', CustomerMenuItemListView.as_view(), name='customer-menu-items-list'),
    path('customer-category/', CustomerCategoryListView.as_view(), name='customer-category-list'),
]
