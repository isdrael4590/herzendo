from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('nuevo/', views.crear, name='crear'),
    path('editar/<int:pk>/', views.editar, name='editar'),
    path('eliminar/<int:pk>/', views.eliminar, name='eliminar'),
    path('imprimir/<int:pk>/', views.imprimir, name='imprimir'),
    path('subir-pdf/', views.subir_pdf, name='subir_pdf'),
    path('subir-pdf/procesar/', views.procesar_pdf, name='procesar_pdf'),
    # Gestión de personal
    path('personal/', views.usuarios_lista, name='usuarios_lista'),
    path('personal/nuevo/', views.usuario_crear, name='usuario_crear'),
    path('personal/editar/<int:pk>/', views.usuario_editar, name='usuario_editar'),
    path('personal/eliminar/<int:pk>/', views.usuario_eliminar, name='usuario_eliminar'),
]
