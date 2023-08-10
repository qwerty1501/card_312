from django.urls import path

from .views import Service_categoryList, Service_categoryRetrieve


urlpatterns = [
    # Все три Категория
    path('service_category/', Service_categoryList.as_view()),
    path('service_category/<int:pk>', Service_categoryRetrieve.as_view()),

]