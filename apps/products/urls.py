from django.urls import path

from .views import ProductCreateListView, ProductDeleteView

urlpatterns = [
    path('product/', ProductCreateListView.as_view()),
    path('product/<int:pk>', ProductDeleteView.as_view()),
]