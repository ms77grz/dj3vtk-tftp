from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='equipment_accounting_home'),
    path('about/', views.about, name='equipment_accounting_about'),
]
