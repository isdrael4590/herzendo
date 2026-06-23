from django.urls import path
from . import views

app_name = 'estadisticas'

urlpatterns = [
    path('',         views.dashboard, name='dashboard'),
    path('analizar/', views.analizar,  name='analizar'),
]
