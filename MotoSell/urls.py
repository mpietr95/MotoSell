from django.urls import path
from . import views

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('moje/', views.MyVehicleListView.as_view(), name='my_vehicles'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('<int:pk>/edytuj/', views.VehicleEditView.as_view(), name='vehicle_edit'),
    path('<int:pk>/publikuj/', views.VehiclePublishView.as_view(), name='vehicle_publish'),
    path('<int:pk>/usun/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('<int:pk>/galeria/', views.VehicleImageUploadView.as_view(), name='vehicle_gallery'),
]
