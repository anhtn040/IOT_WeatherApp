from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('1/', views.index1, name='home1'),
    path('delete/<city_name>/', views.delete_city, name='delete_city')
]