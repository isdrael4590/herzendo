from django.db import models

SI_NO = [('', '—'), ('si', 'Sí'), ('no', 'No')]
SI_NO_NA = [('', '—'), ('si', 'Sí'), ('no', 'No'), ('na', 'No aplica')]
ETNIA = [
    ('', '—'),
    ('mestizo',         'Mestizo'),
    ('indigena',        'Indígena'),
    ('afroecuatoriano', 'Afroecuatoriano'),
    ('blanco',          'Blanco'),
    ('montubio',        'Montubio'),
    ('otro',            'Otros'),
    ('no_dato',         'No dato'),
]
HORMONAS_IHQ = [
    ('prl',    'PRL+'),
    ('gh',     'GH+'),
    ('acth',   'ACTH+'),
    ('fsh_lh', 'FSH/LH+'),
    ('tsh',    'TSH+'),
]
PROVINCIAS = [
    ('', '—'),
    ('Azuay', 'Azuay'),
    ('Bolívar', 'Bolívar'),
    ('Cañar', 'Cañar'),
    ('Carchi', 'Carchi'),
    ('Chimborazo', 'Chimborazo'),
    ('Cotopaxi', 'Cotopaxi'),
    ('El Oro', 'El Oro'),
    ('Esmeraldas', 'Esmeraldas'),
    ('Galápagos', 'Galápagos'),
    ('Guayas', 'Guayas'),
    ('Imbabura', 'Imbabura'),
    ('Loja', 'Loja'),
    ('Los Ríos', 'Los Ríos'),
    ('Manabí', 'Manabí'),
    ('Morona Santiago', 'Morona Santiago'),
    ('Napo', 'Napo'),
    ('Orellana', 'Orellana'),
    ('Pastaza', 'Pastaza'),
    ('Pichincha', 'Pichincha'),
    ('Santa Elena', 'Santa Elena'),
    ('Santo Domingo de los Tsáchilas', 'Santo Domingo de los Tsáchilas'),
    ('Sucumbíos', 'Sucumbíos'),
    ('Tungurahua', 'Tungurahua'),
    ('Zamora Chinchipe', 'Zamora Chinchipe'),
]
INTERP = [('', '—'), ('normal', 'Normal'), ('elevado', 'Elevado'), ('bajo', 'Bajo'), ('no_det', 'No determinado')]
SEXO = [('', '—'), ('M', 'Masculino'), ('F', 'Femenino')]
INSTRUCCION = [
    ('', '—'),
    ('ninguna', 'Ninguna'),
    ('primaria_completa', 'Primaria Completa'),
    ('primaria_incompleta', 'Primaria Incompleta'),
    ('secundaria_completa', 'Secundaria Completa'),
    ('secundaria_incompleta', 'Secundaria Incompleta'),
    ('superior_completa', 'Superior Completa'),
    ('superior_incompleta', 'Superior Incompleta'),
]
TUMOR_INTERP = [
    ('', '—'),
    ('microadenoma', 'Microadenoma (< 10 mm)'),
    ('macroadenoma', 'Macroadenoma (≥ 10 mm hasta 40 mm)'),
    ('gigante',      'Adenoma gigante (> 40 mm)'),
]
KI67_INTERP = [
    ('', '—'),
    ('muy_bajo', 'Muy bajo (< 1 %)'),
    ('bajo',     'Bajo (1 – 3 %)'),
    ('alto',     'Alto (> 3 %)'),
    ('muy_alto', 'Muy alto (>= 10 %)'),
]
PROLACT_INTERP = [
    ('', '—'),
    ('normal',  'Normal'),
    ('baja',    'Baja'),
    ('elevada', 'Elevada'),
    ('no_dato', 'No dato'),
]
KNOSP = [('', '—'), ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
TIPO_HISTOLOGICO = [
    ('', '—'),
    ('prolactinoma',      'Prolactinoma'),
    ('somatotropinoma',   'Somatotropinoma'),
    ('corticotropinoma',  'Corticotropinoma'),
    ('gonadotropinoma',   'Gonadotropinoma'),
    ('tirotropinoma',     'Tirotropinoma'),
    ('carcinoma',         'Carcinoma hipofisario'),
]


def _d(**kw):
    return dict(null=True, blank=True, max_digits=10, decimal_places=3, **kw)


def _c(choices, **kw):
    return dict(max_length=30, choices=choices, blank=True, **kw)


class Paciente(models.Model):
    # ── Datos Generales ──────────────────────────────────────────────────────
    nombre              = models.CharField(max_length=150)
    hcu                 = models.CharField('HCU', max_length=50, blank=True)
    fecha_nacimiento    = models.DateField('Fecha de nacimiento', null=True, blank=True)
    edad_diagnostico    = models.DecimalField('Edad al diagnóstico', **_d())
    sexo                = models.CharField(max_length=1, choices=SEXO, blank=True)
    fecha_procedimiento = models.DateField('Fecha de procedimiento', null=True, blank=True)
    procedimiento       = models.CharField(max_length=200, blank=True)
    cirujano            = models.CharField(max_length=150, blank=True)
    primera_cirugia     = models.CharField('Primera cirugía', **_c(SI_NO))
    solo_biopsia        = models.CharField(**_c(SI_NO))
    provincia_nacimiento = models.CharField(max_length=50, choices=PROVINCIAS, blank=True)
    extranjero          = models.CharField(**_c(SI_NO))
    pais_nacimiento     = models.CharField('País de nacimiento', max_length=100, blank=True)
    nivel_instruccion   = models.CharField('Nivel de instrucción', **_c(INSTRUCCION))
    etnia               = models.CharField(max_length=20, choices=ETNIA, blank=True)
    antecedentes_fam    = models.CharField('Antecedentes familiares tumores hipofisarios', **_c(SI_NO))
    detalle_sindrome    = models.TextField('Detalle del síndrome', blank=True)

    # ── Eje Somatotropo ───────────────────────────────────────────────────────
    gh                  = models.DecimalField('GH', **_d())
    gh_ref_min          = models.DecimalField('GH ref. mín', **_d())
    gh_ref_max          = models.DecimalField('GH ref. máx', **_d())
    gh_interp           = models.CharField('Interpretación GH', **_c(INTERP))
    igf1                = models.DecimalField('IGF-1', **_d())
    igf1_ref_min        = models.DecimalField('IGF-1 ref. mín', **_d())
    igf1_ref_max        = models.DecimalField('IGF-1 ref. máx', **_d())
    igf1_interp         = models.CharField('Interpretación IGF-1', **_c(INTERP))
    igf1_index_elevado  = models.DecimalField('INDEX IGF-1 (ref_max ÷ IGF-1)', null=True, blank=True, max_digits=10, decimal_places=3)
    acromegalia         = models.CharField(**_c(SI_NO))
    tto_previo_octretide = models.CharField('Tto. previo octreótide', **_c(SI_NO))

    # ── Eje Gonadotropo ───────────────────────────────────────────────────────
    lh                  = models.DecimalField('LH', **_d())
    lh_ref_min          = models.DecimalField('LH ref. mín', **_d())
    lh_ref_max          = models.DecimalField('LH ref. máx', **_d())
    lh_interp           = models.CharField('Interpretación LH', **_c(INTERP))
    fsh                 = models.DecimalField('FSH', **_d())
    fsh_ref_min         = models.DecimalField('FSH ref. mín', **_d())
    fsh_ref_max         = models.DecimalField('FSH ref. máx', **_d())
    fsh_interp          = models.CharField('Interpretación FSH', **_c(INTERP))
    estradiol           = models.DecimalField(**_d())
    estradiol_ref_min   = models.DecimalField('Estradiol ref. mín', **_d())
    estradiol_ref_max   = models.DecimalField('Estradiol ref. máx', **_d())
    estradiol_interp    = models.CharField('Interpretación estradiol', **_c(INTERP))
    testosterona        = models.DecimalField('Testosterona total', **_d())
    testosterona_ref_min = models.DecimalField('Testosterona ref. mín', **_d())
    testosterona_ref_max = models.DecimalField('Testosterona ref. máx', **_d())
    testosterona_interp  = models.CharField('Interpretación testosterona', **_c(INTERP))
    hipogonadismo_fem   = models.CharField('Hipogonadismo femenino', **_c(SI_NO_NA))
    hipogonadismo_masc  = models.CharField('Hipogonadismo masculino', **_c(SI_NO_NA))
    amenorrea           = models.CharField(**_c(SI_NO))
    gonadotropinoma     = models.CharField('Gonadotropinoma funcionante', **_c(SI_NO))

    # ── Eje Tiroideo ──────────────────────────────────────────────────────────
    tsh                 = models.DecimalField('TSH', **_d())
    tsh_ref_min         = models.DecimalField('TSH ref. mín', **_d())
    tsh_ref_max         = models.DecimalField('TSH ref. máx', **_d())
    t4l                 = models.DecimalField('T4L', **_d())
    t4l_ref_min         = models.DecimalField('T4L ref. mín', **_d())
    t4l_ref_max         = models.DecimalField('T4L ref. máx', **_d())
    hipotiroidismo_central = models.CharField('Hipotiroidismo central', **_c(SI_NO))
    tirotropinoma       = models.CharField(**_c(SI_NO))

    # ── Eje Corticotropo ──────────────────────────────────────────────────────
    cortisol            = models.DecimalField(**_d())
    cortisol_ref_min    = models.DecimalField('Cortisol ref. mín', **_d())
    cortisol_ref_max    = models.DecimalField('Cortisol ref. máx', **_d())
    cortisol_interp     = models.CharField('Interpretación cortisol', **_c(INTERP))
    eje_corticotropo_suf = models.CharField('Eje corticotropo suficiente', **_c(SI_NO))
    eje_corticotropo_ins = models.CharField('Eje corticotropo insuficiente', **_c(SI_NO))
    acth                = models.DecimalField('ACTH plasmática', **_d())
    acth_ref_min        = models.DecimalField('ACTH ref. mín', **_d())
    acth_ref_max        = models.DecimalField('ACTH ref. máx', **_d())
    acth_interp         = models.CharField('Interpretación ACTH', **_c(INTERP))
    cushing             = models.CharField('Síndrome de Cushing', **_c(SI_NO))

    # ── Prolactina ────────────────────────────────────────────────────────────
    prolactina          = models.DecimalField('Prolactina sérica', **_d())
    prolactina_ref_min  = models.DecimalField('Prolactina ref. mín', **_d())
    prolactina_ref_max  = models.DecimalField('Prolactina ref. máx', **_d())
    prolactina_interp   = models.CharField('Interpretación prolactina', max_length=30, choices=PROLACT_INTERP, blank=True)
    tto_previo_cabergolina = models.CharField('Tto. previo cabergolina', **_c(SI_NO))

    # ── Síntomas y complicaciones ─────────────────────────────────────────────
    deficit_vasopresina = models.CharField('Déficit arginina vasopresina', **_c(SI_NO))
    apoplejia           = models.CharField('Apoplejía hipofisaria', **_c(SI_NO))
    cefalea             = models.CharField(**_c(SI_NO))
    alt_campo_visual    = models.CharField('Alteración del campo visual', **_c(SI_NO))
    convulsiones        = models.CharField(**_c(SI_NO))
    fistula_lcr         = models.CharField('Fístula de LCR', **_c(SI_NO))
    sind_seno_cavernoso = models.CharField('Síndrome del seno cavernoso', **_c(SI_NO))

    # ── Tumor ─────────────────────────────────────────────────────────────────
    tamano_tumor        = models.DecimalField('Tamaño del tumor (mm)', **_d())
    tamano_tumor_interp = models.CharField('Interpretación tamaño tumor', max_length=30, choices=TUMOR_INTERP, blank=True)
    invasion_seno_cav   = models.CharField('Invasión del seno cavernoso', **_c(SI_NO))
    knosp               = models.CharField('KNOSP', max_length=5, choices=KNOSP, blank=True)
    tipo_histologico    = models.CharField('Tipo histológico del tumor', max_length=30, choices=TIPO_HISTOLOGICO, blank=True)

    # ── Histología ────────────────────────────────────────────────────────────
    reticulina_distorsionada = models.CharField('Fibras de reticulina distorsionadas', **_c(SI_NO))
    hormonas_ihq        = models.CharField('Hormonas IHQ', max_length=100, blank=True,
                            help_text='Valores separados por coma: prl,gh,acth,fsh_lh,tsh')
    descripcion_ihq     = models.TextField('Descripción hormonas IHQ', blank=True)
    ki67                = models.DecimalField('Ki-67 (%)', **_d())
    ki67_interp         = models.CharField('Interpretación Ki-67', max_length=10, choices=KI67_INTERP, blank=True)
    observaciones       = models.TextField(blank=True)

    ESTADO_CHOICES = [('pendiente', 'Pendiente'), ('completado', 'Completado')]
    estado              = models.CharField(max_length=15, choices=ESTADO_CHOICES,
                            default='pendiente', db_index=True)

    creado              = models.DateTimeField(auto_now_add=True)
    actualizado         = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_procedimiento', 'nombre']
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.nombre} — {self.hcu or "sin HCU"}'

    def save(self, *args, **kwargs):
        # Provincia → extranjero y país de nacimiento
        if self.provincia_nacimiento:
            self.extranjero = 'no'
            if not self.pais_nacimiento:
                self.pais_nacimiento = 'Ecuador'
        else:
            if not self.extranjero:
                self.extranjero = 'si'

        # INDEX IGF-1 = igf1_ref_max / igf1
        try:
            if self.igf1 and self.igf1_ref_max and float(self.igf1) != 0:
                from decimal import Decimal, ROUND_HALF_UP
                idx = Decimal(str(self.igf1_ref_max)) / Decimal(str(self.igf1))
                self.igf1_index_elevado = idx.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        except Exception:
            pass

        # Prolactina → interpretación automática
        if self.prolactina is None:
            self.prolactina_interp = 'no_dato'
        elif self.prolactina_ref_min is not None and self.prolactina_ref_max is not None:
            v = float(self.prolactina); vmin = float(self.prolactina_ref_min); vmax = float(self.prolactina_ref_max)
            self.prolactina_interp = 'baja' if v < vmin else ('elevada' if v > vmax else 'normal')

        # LH → interpretación automática
        if self.lh is None:
            self.lh_interp = 'no_det'
        elif self.lh_ref_min is not None and self.lh_ref_max is not None:
            v = float(self.lh); vmin = float(self.lh_ref_min); vmax = float(self.lh_ref_max)
            self.lh_interp = 'bajo' if v < vmin else ('elevado' if v > vmax else 'normal')

        # FSH → interpretación automática
        if self.fsh is None:
            self.fsh_interp = 'no_det'
        elif self.fsh_ref_min is not None and self.fsh_ref_max is not None:
            v = float(self.fsh); vmin = float(self.fsh_ref_min); vmax = float(self.fsh_ref_max)
            self.fsh_interp = 'bajo' if v < vmin else ('elevado' if v > vmax else 'normal')

        # Estradiol → interpretación automática
        if self.estradiol is None:
            self.estradiol_interp = 'no_det'
        elif self.estradiol_ref_min is not None and self.estradiol_ref_max is not None:
            v = float(self.estradiol); vmin = float(self.estradiol_ref_min); vmax = float(self.estradiol_ref_max)
            self.estradiol_interp = 'bajo' if v < vmin else ('elevado' if v > vmax else 'normal')

        # Testosterona → interpretación automática
        if self.testosterona is None:
            self.testosterona_interp = 'no_det'
        elif self.testosterona_ref_min is not None and self.testosterona_ref_max is not None:
            v = float(self.testosterona); vmin = float(self.testosterona_ref_min); vmax = float(self.testosterona_ref_max)
            self.testosterona_interp = 'bajo' if v < vmin else ('elevado' if v > vmax else 'normal')

        # GH → interpretación automática
        if self.gh is None:
            self.gh_interp = 'no_det'
        elif self.gh_ref_min is not None and self.gh_ref_max is not None:
            v = float(self.gh)
            vmin = float(self.gh_ref_min)
            vmax = float(self.gh_ref_max)
            if v < vmin:
                self.gh_interp = 'bajo'
            elif v > vmax:
                self.gh_interp = 'elevado'
            else:
                self.gh_interp = 'normal'

        # IGF-1 → interpretación automática
        if self.igf1 is None:
            self.igf1_interp = 'no_det'
        elif self.igf1_ref_min is not None and self.igf1_ref_max is not None:
            v = float(self.igf1)
            vmin = float(self.igf1_ref_min)
            vmax = float(self.igf1_ref_max)
            if v < vmin:
                self.igf1_interp = 'bajo'
            elif v > vmax:
                self.igf1_interp = 'elevado'
            else:
                self.igf1_interp = 'normal'

        # Cortisol → interpretación automática
        if self.cortisol is None:
            self.cortisol_interp = 'no_det'
        elif self.cortisol_ref_min is not None and self.cortisol_ref_max is not None:
            c = float(self.cortisol)
            vmin = float(self.cortisol_ref_min)
            vmax = float(self.cortisol_ref_max)
            if c < vmin:
                self.cortisol_interp = 'bajo'
            elif c > vmax:
                self.cortisol_interp = 'elevado'
            else:
                self.cortisol_interp = 'normal'

        # ACTH → interpretación automática
        if self.acth is None:
            self.acth_interp = 'no_det'
        elif self.acth_ref_min is not None and self.acth_ref_max is not None:
            a = float(self.acth)
            vmin = float(self.acth_ref_min)
            vmax = float(self.acth_ref_max)
            if a < vmin:
                self.acth_interp = 'bajo'
            elif a > vmax:
                self.acth_interp = 'elevado'
            else:
                self.acth_interp = 'normal'

        # Ki-67 → interpretación automática
        if self.ki67 is not None:
            k = float(self.ki67)
            if   k < 1:   self.ki67_interp = 'muy_bajo'
            elif k <= 3:  self.ki67_interp = 'bajo'
            elif k <= 9: self.ki67_interp = 'alto'
            else:         self.ki67_interp = 'muy_alto'

        # Calcular interpretación del tamaño del tumor automáticamente
        if self.tamano_tumor is not None:
            t = float(self.tamano_tumor)
            if t < 10:
                self.tamano_tumor_interp = 'microadenoma'
            elif t <= 40:
                self.tamano_tumor_interp = 'macroadenoma'
            else:
                self.tamano_tumor_interp = 'gigante'
        super().save(*args, **kwargs)
