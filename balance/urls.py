from django.urls import path
from . import views

urlpatterns = [
    path('shipment-planner/', views.shipment_planner, name='shipment_planner'),
    path('insights/', views.insights, name='insights'),
]
