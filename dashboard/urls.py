from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('coming-soon/', views.coming_soon, name='coming_soon'),
]
