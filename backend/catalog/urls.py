from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProductListView, ProductDetailView
from .admin_views import AdminProductListCreateView, AdminProductDetailView

urlpatterns = [
    path("products/", ProductListView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("auth/login/", obtain_auth_token),
    path("admin/products/", AdminProductListCreateView.as_view()),
    path("admin/products/<int:pk>/", AdminProductDetailView.as_view()),
]
