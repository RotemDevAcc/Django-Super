from django.urls import path, include
from . import views
from .views import Product_view, Category_view
urlpatterns = [
    #path('', views.products),
    #path('register/',views.register),
    path('categories/', Category_view.as_view(), name='category-list'),
    path('products/', Product_view.as_view(), name='product-list'),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('purchase/',views.purchase)
]

