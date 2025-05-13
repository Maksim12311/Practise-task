from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('about/', views.about, name = "about"),
    path('add/', views.add, name = "add"),
]