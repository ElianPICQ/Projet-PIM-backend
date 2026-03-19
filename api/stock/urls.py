from django.urls import path
from . import views

urlpatterns = [
    path('', views.RedirectionGetStock.as_view()),
    path('add/', views.RedirectionAddStock.as_view()),
    path('remove/', views.RedirectionRemoveStock.as_view()),
]