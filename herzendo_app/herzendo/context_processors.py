def permisos_rol(request):
    if not request.user.is_authenticated:
        return {
            'puede_crear': False,
            'puede_editar': False,
            'puede_eliminar': False,
            'puede_pdf': False,
            'rol_nombre': '',
        }
    grupos = set(request.user.groups.values_list('name', flat=True))
    es_admin = request.user.is_superuser or 'administrador' in grupos
    es_medico = 'medico' in grupos
    puede_stats      = es_admin or request.user.groups.filter(name='estadisticas').exists()
    puede_codificado = es_admin or request.user.groups.filter(name='ver_codificado').exists()
    return {
        'puede_crear':        es_admin or es_medico,
        'puede_editar':       es_admin or es_medico,
        'puede_eliminar':     es_admin,
        'puede_pdf':          es_admin or es_medico,
        'puede_estadisticas': puede_stats,
        'puede_codificado':   puede_codificado,
        'rol_nombre': ('Administrador' if es_admin
                       else 'Médico' if es_medico
                       else 'Visualizador'),
    }
