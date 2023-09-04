from django.urls import path
from . import views

urlpatterns = [
    path('product_create/<int:pk>/', views.ProductCreateView.as_view()),
    path('product_update/<int:pk>/', views.ProductUpdateView.as_view()),
    path('my_products/', views.MyProductListView.as_view()),
    path('promotion_create/', views.PromotionCreateView.as_view()),
    path('promotion_update/<int:pk>/', views.PromotionUpdateView.as_view()),
]
