from pacientes.models import (
    SI_NO, SI_NO_NA, SEXO, INSTRUCCION, ETNIA, INTERP,
    PROLACT_INTERP, TUMOR_INTERP, KI67_INTERP, TIPO_HISTOLOGICO, KNOSP,
    DIAGNOSTICO_TIPOS,
)

ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('completado', 'Completado')]

SECCIONES = [
    {
        'id': 'generales',
        'label': 'Datos Generales',
        'icon': 'bi-person-fill',
        'vars': [
            {'campo': 'edad_diagnostico',  'label': 'Edad al diagnóstico',    'tipo': 'numerico'},
            {'campo': 'sexo',              'label': 'Sexo',                   'tipo': 'categorico', 'choices': SEXO},
            {'campo': 'primera_cirugia',   'label': 'Primera cirugía',        'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'solo_biopsia',      'label': 'Solo biopsia',           'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'extranjero',        'label': 'Extranjero',             'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'nivel_instruccion', 'label': 'Nivel de instrucción',   'tipo': 'categorico', 'choices': INSTRUCCION},
            {'campo': 'etnia',             'label': 'Etnia',                  'tipo': 'categorico', 'choices': ETNIA},
            {'campo': 'antecedentes_fam',  'label': 'Antec. fam. hipofisarios', 'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'diagnostico',       'label': 'Diagnóstico (combinación)', 'tipo': 'categorico', 'choices': DIAGNOSTICO_TIPOS, 'multivalue': True, 'no_choices_filter': True},
            {'campo': 'estado',            'label': 'Estado del registro',    'tipo': 'categorico', 'choices': ESTADO_CHOICES},
        ],
    },
    {
        'id': 'somatotropo',
        'label': 'Eje Somatotropo',
        'icon': 'bi-activity',
        'vars': [
            {'campo': 'gh',                  'label': 'GH',                 'tipo': 'numerico'},
            {'campo': 'gh_ref_min',          'label': 'GH Ref. Mín',        'tipo': 'numerico'},
            {'campo': 'gh_ref_max',          'label': 'GH Ref. Máx',        'tipo': 'numerico'},
            {'campo': 'gh_interp',           'label': 'GH Interpretación',  'tipo': 'categorico', 'choices': INTERP},
            {'campo': 'igf1',                'label': 'IGF-1',              'tipo': 'numerico'},
            {'campo': 'igf1_ref_min',        'label': 'IGF-1 Ref. Mín',    'tipo': 'numerico'},
            {'campo': 'igf1_ref_max',        'label': 'IGF-1 Ref. Máx',    'tipo': 'numerico'},
            {'campo': 'igf1_interp',         'label': 'IGF-1 Interpretación', 'tipo': 'categorico', 'choices': INTERP},
            {'campo': 'igf1_index_elevado',  'label': 'IGF-1 ÷ ref_max',   'tipo': 'numerico'},
            {'campo': 'acromegalia',         'label': 'Acromegalia',        'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'tto_previo_octretide','label': 'Tto. Octreótide',    'tipo': 'categorico', 'choices': SI_NO},
        ],
    },
    {
        'id': 'gonadotropo',
        'label': 'Eje Gonadotropo',
        'icon': 'bi-activity',
        'vars': [
            {'campo': 'lh',                 'label': 'LH',                      'tipo': 'numerico'},
            {'campo': 'fsh',                'label': 'FSH',                     'tipo': 'numerico'},
            {'campo': 'estradiol',          'label': 'Estradiol',               'tipo': 'numerico'},
            {'campo': 'testosterona',       'label': 'Testosterona',            'tipo': 'numerico'},
            {'campo': 'hipogonadismo_fem',  'label': 'Hipogonadismo Fem.',      'tipo': 'categorico', 'choices': SI_NO_NA},
            {'campo': 'hipogonadismo_masc', 'label': 'Hipogonadismo Masc.',     'tipo': 'categorico', 'choices': SI_NO_NA},
            {'campo': 'amenorrea',          'label': 'Amenorrea',               'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'gonadotropinoma',    'label': 'Gonadotropinoma func.',   'tipo': 'categorico', 'choices': SI_NO},
        ],
    },
    {
        'id': 'tiroideo',
        'label': 'Eje Tiroideo',
        'icon': 'bi-activity',
        'vars': [
            {'campo': 'tsh',                   'label': 'TSH',                    'tipo': 'numerico'},
            {'campo': 't4l',                   'label': 'T4L',                    'tipo': 'numerico'},
            {'campo': 'hipotiroidismo_central', 'label': 'Hipotiroidismo Central', 'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'tirotropinoma',          'label': 'Tirotropinoma',          'tipo': 'categorico', 'choices': SI_NO},
        ],
    },
    {
        'id': 'corticotropo',
        'label': 'Eje Corticotropo',
        'icon': 'bi-activity',
        'vars': [
            {'campo': 'cortisol',  'label': 'Cortisol', 'tipo': 'numerico'},
            {'campo': 'acth',      'label': 'ACTH',     'tipo': 'numerico'},
            {'campo': 'cushing',   'label': 'Cushing',  'tipo': 'categorico', 'choices': SI_NO},
        ],
    },
    {
        'id': 'prolactina',
        'label': 'Prolactina',
        'icon': 'bi-droplet-fill',
        'vars': [
            {'campo': 'prolactina',             'label': 'Prolactina sérica',    'tipo': 'numerico'},
            {'campo': 'prolactina_interp',      'label': 'Prolactina Interp.',   'tipo': 'categorico', 'choices': PROLACT_INTERP},
            {'campo': 'tto_previo_cabergolina', 'label': 'Tto. Cabergolina',    'tipo': 'categorico', 'choices': SI_NO},
        ],
    },
    {
        'id': 'sintomas',
        'label': 'Síntomas / Complicaciones',
        'icon': 'bi-exclamation-triangle-fill',
        'vars': [
            {'campo': 'deficit_vasopresina', 'label': 'Déficit Vasopresina',    'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'apoplejia',           'label': 'Apoplejía hipofisaria',  'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'cefalea',             'label': 'Cefalea',                'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'alt_campo_visual',    'label': 'Alt. campo visual',      'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'convulsiones',        'label': 'Convulsiones',           'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'fistula_lcr',         'label': 'Fístula LCR',            'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'sind_seno_cavernoso', 'label': 'Sínd. seno cavernoso',   'tipo': 'categorico', 'choices': SI_NO},
        ],
    },
    {
        'id': 'tumor',
        'label': 'Tumor',
        'icon': 'bi-circle-fill',
        'vars': [
            {'campo': 'tamano_tumor',       'label': 'Tamaño tumor (mm)',      'tipo': 'numerico'},
            {'campo': 'tamano_tumor_interp','label': 'Clasificación tumor',    'tipo': 'categorico', 'choices': TUMOR_INTERP},
            {'campo': 'invasion_seno_cav',  'label': 'Invasión seno cav.',     'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'knosp',              'label': 'KNOSP',                  'tipo': 'categorico', 'choices': KNOSP},
            {'campo': 'tipo_histologico',   'label': 'Tipo histológico',       'tipo': 'categorico', 'choices': TIPO_HISTOLOGICO},
        ],
    },
    {
        'id': 'histologia',
        'label': 'Histología',
        'icon': 'bi-eyedropper',
        'vars': [
            {'campo': 'reticulina_distorsionada', 'label': 'Reticulina distorsionada', 'tipo': 'categorico', 'choices': SI_NO},
            {'campo': 'ki67',                     'label': 'Ki-67 (%)',                'tipo': 'numerico'},
            {'campo': 'ki67_interp',              'label': 'Ki-67 Interpretación',     'tipo': 'categorico', 'choices': KI67_INTERP},
        ],
    },
    {
        'id': 'diagnostico_individual',
        'label': 'Diagnóstico por tipo',
        'icon': 'bi-check2-square',
        'vars': [
            {
                'campo': 'diag_tipos_resumen',
                'label': 'Diagnóstico por tipo (resumen)',
                'tipo': 'resumen_tipos',
                'source_campo': 'diagnostico',
                'tipos': DIAGNOSTICO_TIPOS,
            },
            {
                'campo': 'diag_clinico',
                'label': 'Diagnóstico Clínico',
                'tipo': 'categorico',
                'choices': SI_NO,
                'source_campo': 'diagnostico',
                'multivalue_extract': 'clinico',
            },
            {
                'campo': 'diag_bioquimico',
                'label': 'Diagnóstico Bioquímico',
                'tipo': 'categorico',
                'choices': SI_NO,
                'source_campo': 'diagnostico',
                'multivalue_extract': 'bioquimico',
            },
            {
                'campo': 'diag_anatomopatologico',
                'label': 'Diagnóstico Anatomopatológico',
                'tipo': 'categorico',
                'choices': SI_NO,
                'source_campo': 'diagnostico',
                'multivalue_extract': 'anatomopatologico',
            },
        ],
    },
]

# Flat index: campo → metadata
CATALOGO = {
    v['campo']: {**v, 'seccion': s['label']}
    for s in SECCIONES
    for v in s['vars']
}
