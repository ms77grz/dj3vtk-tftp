from django.urls import path
from .views import olt_list, olt_detail, ont_detail, network, show_map

urlpatterns = [
    path('', network, name='network_url'),
    path('gpon/', olt_list, name='olt_list'),
    path('gpon/olt/map/', show_map, name='map_url'),
    path('gpon/olt/<str:ip>/<str:model>', olt_detail, name='olt_detail'),
    path('gpon/ont/<str:ip>/<str:model>/<str:oid>/', ont_detail, name='ont_detail'),
]
