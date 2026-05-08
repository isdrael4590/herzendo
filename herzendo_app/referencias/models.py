from django.db import models

HORMONA_CHOICES = [
    ('gh',          'GH'),
    ('igf1',        'IGF1'),
    ('lh',          'LH'),
    ('fsh',         'FSH'),
    ('estradiol',   'ESTRADIOL'),
    ('testosterona','Testosterona'),
    ('tsh',         'TSH'),
    ('ft4',         'FT4'),
    ('cortisol',    'Cortisol'),
    ('acth',        'ACTH'),
    ('prolactina',  'PROLACTINA'),
]


class ValorReferencia(models.Model):
    hormona        = models.CharField(max_length=20, choices=HORMONA_CHOICES)
    version        = models.CharField('Versión del inserto', max_length=50)

    # Criterios clínicos
    grupo_clinico  = models.CharField('Grupo / Condición clínica', max_length=100, blank=True,
                        help_text='Ej: Hombres, Mujeres Fase Folicular, Hombres (20-49 años)')
    tipo_muestra   = models.CharField('Tipo de muestra', max_length=100, blank=True,
                        help_text='Ej: Suero y Plasma, Suero')

    # Unidad 1 — Valores Teóricos (Rango Esperado)
    unidad         = models.CharField('Unidad 1', max_length=30, blank=True)
    ref_min        = models.DecimalField('Ref. mín', max_digits=14, decimal_places=4, null=True, blank=True)
    ref_max        = models.DecimalField('Ref. máx', max_digits=14, decimal_places=4, null=True, blank=True)

    # Unidad 2 — para hormonas con doble unidad (ej. Prolactina: µUI/mL y ng/mL)
    unidad2        = models.CharField('Unidad 2', max_length=30, blank=True)
    ref_min2       = models.DecimalField('Ref. mín (unidad 2)', max_digits=14, decimal_places=4, null=True, blank=True)
    ref_max2       = models.DecimalField('Ref. máx (unidad 2)', max_digits=14, decimal_places=4, null=True, blank=True)

    # Intervalo de Medición (Capacidad Técnica)
    intervalo_min  = models.DecimalField('Intervalo mín (técnico)', max_digits=14, decimal_places=4, null=True, blank=True)
    intervalo_max  = models.DecimalField('Intervalo máx (técnico)', max_digits=14, decimal_places=4, null=True, blank=True)

    observaciones  = models.TextField('Observaciones', blank=True)

    class Meta:
        ordering = ['hormona', 'version', 'grupo_clinico']
        unique_together = [('hormona', 'version', 'grupo_clinico')]
        verbose_name = 'Valor de referencia'
        verbose_name_plural = 'Valores de referencia'

    def __str__(self):
        partes = [self.get_hormona_display(), self.version]
        if self.grupo_clinico:
            partes.append(self.grupo_clinico)
        return ' — '.join(partes)
