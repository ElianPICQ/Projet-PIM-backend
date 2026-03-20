from django.urls import path
from . import views

urlpatterns = [
#    path('register/', views.Register.as_view()),
    path('', views.RedirectionDashboard.as_view()),
]