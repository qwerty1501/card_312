from django.urls import path

from .views import Service_categoryList, Service_categoryRetrieve , Product_categoryList , Product_categoryRetrieve,Sale_categoryList ,Sale_categoryRetrieve


urlpatterns = [
    # Все три Категория
    path('service_category/', Service_categoryList.as_view()),
    path('service_category/<int:pk>', Service_categoryRetrieve.as_view()),
    
    path('product_category/', Product_categoryList.as_view()),
    path('product_category/<int:pk>', Product_categoryRetrieve.as_view()),
    
    path('sale_category/', Sale_categoryList.as_view()),
    path('sale_category/<int:pk>', Sale_categoryRetrieve.as_view()),
]