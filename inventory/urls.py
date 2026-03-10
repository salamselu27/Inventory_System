from django.urls import path
from . import views

urlpatterns = [
    path('add-item/', views.add_item, name='add_item'),
    path('entry-hub/', views.entry_hub, name='entry_hub'),
    path('job-card/', views.create_job_card, name='create_job_card'),
    path('logs/', views.inventory_logs, name='inventory_logs'),
    path('alerts/', views.stock_alerts, name='stock_alerts'),
    path('live-stock/', views.live_stock, name='live_stock'),
]
