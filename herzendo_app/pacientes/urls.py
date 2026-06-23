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
    path('estado/<int:pk>/',   views.cambiar_estado,  name='cambiar_estado'),
    path('exportar/excel/',     views.exportar_excel,  name='exportar_excel'),
    path('exportar/csv/',       views.exportar_csv,    name='exportar_csv'),
    path('importar/csv/',       views.importar_csv,    name='importar_csv'),
    path('importar/plantilla/', views.plantilla_csv,   name='plantilla_csv'),
    path('importar/excel/',     views.importar_excel,  name='importar_excel'),
    # Datos codificados
    path('codificado/',               views.datos_codificados,         name='datos_codificados'),
    path('codificado/excel/',         views.exportar_codificado_excel, name='exportar_codificado_excel'),
    path('codificado/csv/',           views.exportar_codificado_csv,   name='exportar_codificado_csv'),
    # Gestión de personal
    path('personal/', views.usuarios_lista, name='usuarios_lista'),
    path('personal/nuevo/', views.usuario_crear, name='usuario_crear'),
    path('personal/editar/<int:pk>/', views.usuario_editar, name='usuario_editar'),
    path('personal/eliminar/<int:pk>/', views.usuario_eliminar, name='usuario_eliminar'),
]
