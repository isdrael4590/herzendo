from django.urls import path
from . import views

app_name = 'referencias'

urlpatterns = [
    path('',                       views.lista,       name='lista'),
    path('nuevo/',                 views.crear,       name='crear'),
    path('<int:pk>/editar/',       views.editar,      name='editar'),
    path('<int:pk>/eliminar/',     views.eliminar,    name='eliminar'),
    path('api/<str:hormona>/',     views.api_hormona,    name='api_hormona'),
    path('importar/',              views.importar_excel, name='importar_excel'),
]
