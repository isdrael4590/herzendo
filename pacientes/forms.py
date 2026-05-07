from django import forms
from .models import Paciente, HORMONAS_IHQ

_num = {'class': 'form-control form-control-sm', 'step': 'any'}
_sel = {'class': 'form-select form-select-sm'}
_txt = {'class': 'form-control form-control-sm'}
_ta  = {'class': 'form-control form-control-sm', 'rows': 2}
_dat = {'class': 'form-control form-control-sm', 'type': 'date'}


def _w(widget_attrs):
    return widget_attrs


class PacienteForm(forms.ModelForm):

    # Campo múltiple para hormonas IHQ — se guarda como CSV en el modelo
    hormonas_ihq = forms.MultipleChoiceField(
        label='Hormonas IHQ',
        choices=HORMONAS_IHQ,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Paciente
        exclude = ['creado', 'actualizado', 'estado']
        widgets = {
            # Generales
            'nombre':              forms.TextInput(attrs=_txt),
            'hcu':                 forms.TextInput(attrs=_txt),
            'fecha_nacimiento':    forms.DateInput(attrs=_dat),
            'edad_diagnostico':    forms.NumberInput(attrs=_num),
            'fecha_procedimiento': forms.DateInput(attrs=_dat),
            'sexo':                forms.Select(attrs=_sel),
            'procedimiento':       forms.TextInput(attrs=_txt),
            'cirujano':            forms.TextInput(attrs=_txt),
            'primera_cirugia':     forms.Select(attrs=_sel),
            'solo_biopsia':        forms.Select(attrs=_sel),
            'provincia_nacimiento':forms.Select(attrs=_sel),
            'extranjero':          forms.Select(attrs=_sel),
            'pais_nacimiento':     forms.TextInput(attrs=_txt),
            'nivel_instruccion':   forms.Select(attrs=_sel),
            'etnia':               forms.Select(attrs=_sel),
            'antecedentes_fam':    forms.Select(attrs=_sel),
            'detalle_sindrome':    forms.Textarea(attrs=_ta),
            # Somatotropo
            'gh':                  forms.NumberInput(attrs=_num),
            'gh_ref_min':          forms.NumberInput(attrs=_num),
            'gh_ref_max':          forms.NumberInput(attrs=_num),
            'gh_interp':           forms.Select(attrs=_sel),
            'igf1':                forms.NumberInput(attrs=_num),
            'igf1_ref_min':        forms.NumberInput(attrs=_num),
            'igf1_ref_max':        forms.NumberInput(attrs=_num),
            'igf1_interp':         forms.Select(attrs=_sel),
            'igf1_index_elevado':  forms.NumberInput(attrs={**_num, 'readonly': True, 'style': 'background:#f8f9fa;'}),
            'acromegalia':         forms.Select(attrs=_sel),
            'tto_previo_octretide':forms.Select(attrs=_sel),
            # Gonadotropo
            'lh':                  forms.NumberInput(attrs=_num),
            'lh_ref_min':          forms.NumberInput(attrs=_num),
            'lh_ref_max':          forms.NumberInput(attrs=_num),
            'lh_interp':           forms.Select(attrs=_sel),
            'fsh':                 forms.NumberInput(attrs=_num),
            'fsh_ref_min':         forms.NumberInput(attrs=_num),
            'fsh_ref_max':         forms.NumberInput(attrs=_num),
            'fsh_interp':          forms.Select(attrs=_sel),
            'estradiol':           forms.NumberInput(attrs=_num),
            'estradiol_ref_min':   forms.NumberInput(attrs=_num),
            'estradiol_ref_max':   forms.NumberInput(attrs=_num),
            'estradiol_interp':    forms.Select(attrs=_sel),
            'testosterona':        forms.NumberInput(attrs=_num),
            'testosterona_ref_min':forms.NumberInput(attrs=_num),
            'testosterona_ref_max':forms.NumberInput(attrs=_num),
            'testosterona_interp': forms.Select(attrs=_sel),
            'hipogonadismo_fem':   forms.Select(attrs=_sel),
            'hipogonadismo_masc':  forms.Select(attrs=_sel),
            'amenorrea':           forms.Select(attrs=_sel),
            'gonadotropinoma':     forms.Select(attrs=_sel),
            # Tiroideo
            'tsh':                 forms.NumberInput(attrs=_num),
            'tsh_ref_min':         forms.NumberInput(attrs=_num),
            'tsh_ref_max':         forms.NumberInput(attrs=_num),
            't4l':                 forms.NumberInput(attrs=_num),
            't4l_ref_min':         forms.NumberInput(attrs=_num),
            't4l_ref_max':         forms.NumberInput(attrs=_num),
            'hipotiroidismo_central': forms.Select(attrs=_sel),
            'tirotropinoma':       forms.Select(attrs=_sel),
            # Corticotropo
            'cortisol':            forms.NumberInput(attrs=_num),
            'cortisol_ref_min':    forms.NumberInput(attrs=_num),
            'cortisol_ref_max':    forms.NumberInput(attrs=_num),
            'cortisol_interp':     forms.Select(attrs=_sel),
            'eje_corticotropo_suf':forms.Select(attrs=_sel),
            'eje_corticotropo_ins':forms.Select(attrs=_sel),
            'acth':                forms.NumberInput(attrs=_num),
            'acth_ref_min':        forms.NumberInput(attrs=_num),
            'acth_ref_max':        forms.NumberInput(attrs=_num),
            'acth_interp':         forms.Select(attrs=_sel),
            'cushing':             forms.Select(attrs=_sel),
            # Prolactina
            'prolactina':          forms.NumberInput(attrs=_num),
            'prolactina_ref_min':  forms.NumberInput(attrs=_num),
            'prolactina_ref_max':  forms.NumberInput(attrs=_num),
            'prolactina_interp':   forms.Select(attrs=_sel),
            'tto_previo_cabergolina': forms.Select(attrs=_sel),
            # Síntomas
            'deficit_vasopresina': forms.Select(attrs=_sel),
            'apoplejia':           forms.Select(attrs=_sel),
            'cefalea':             forms.Select(attrs=_sel),
            'alt_campo_visual':    forms.Select(attrs=_sel),
            'convulsiones':        forms.Select(attrs=_sel),
            'fistula_lcr':         forms.Select(attrs=_sel),
            'sind_seno_cavernoso': forms.Select(attrs=_sel),
            # Tumor
            'tamano_tumor':        forms.NumberInput(attrs=_num),
            'tamano_tumor_interp': forms.Select(attrs=_sel),
            'invasion_seno_cav':   forms.Select(attrs=_sel),
            'knosp':               forms.Select(attrs=_sel),
            'tipo_histologico':    forms.Select(attrs=_sel),
            # Histología
            'reticulina_distorsionada': forms.Select(attrs=_sel),
            'descripcion_ihq':     forms.Textarea(attrs=_ta),
            'ki67':                forms.NumberInput(attrs=_num),
            'ki67_interp':         forms.Select(attrs=_sel),
            'observaciones':       forms.Textarea(attrs={**_ta, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convertir CSV almacenado → lista para el widget de checkboxes
        if self.instance and self.instance.hormonas_ihq:
            self.initial['hormonas_ihq'] = [
                v.strip() for v in self.instance.hormonas_ihq.split(',') if v.strip()
            ]

    def clean_hormonas_ihq(self):
        # Convertir lista seleccionada → CSV para guardar en el modelo
        valores = self.cleaned_data.get('hormonas_ihq') or []
        return ','.join(valores)
