from django.contrib import admin
from .models import ValorReferencia

@admin.register(ValorReferencia)
class ValorReferenciaAdmin(admin.ModelAdmin):
    list_display = ('hormona', 'version', 'unidad', 'ref_min', 'ref_max', 'intervalo_min', 'intervalo_max')
    list_filter  = ('hormona',)
