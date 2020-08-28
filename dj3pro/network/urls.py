from django.urls import path
from .views import olt_list, olt_detail, ont_detail, network

urlpatterns = [
    path('', network, name='network_url'),
    path('gpon/', olt_list, name='olt_list'),
    path('gpon/olt/<str:ip>/<str:model>', olt_detail, name='olt_detail'),
    path('gpon/ont/<str:ip>/<str:oid>/<str:description>', ont_detail, name='ont_detail'),
]
