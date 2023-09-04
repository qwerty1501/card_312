from django.urls import path
from . import views

urlpatterns = [
    path('event_create/', views.EventCreateView.as_view()),
    path('event_list/', views.MyEventListView.as_view()),
    path('event_update/<int:pk>/', views.EventUpdateView.as_view()),
]
