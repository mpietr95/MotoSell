from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('moje/', views.my_vehicles, name='my_vehicles'),
    path('dodaj/', views.vehicle_create, name='vehicle_create'),
    path('<int:pk>/edytuj/', views.vehicle_edit, name='vehicle_edit'),
    path('<int:pk>/publikuj/', views.vehicle_publish, name='vehicle_publish'),
    path('<int:pk>/usun/', views.vehicle_delete, name='vehicle_delete'),
]
