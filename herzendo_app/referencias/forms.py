from django import forms
from .models import ValorReferencia


class ValorReferenciaForm(forms.ModelForm):
    class Meta:
        model  = ValorReferencia
        fields = [
            'hormona', 'version',
            'grupo_clinico', 'tipo_muestra',
            'unidad', 'ref_min', 'ref_max',
            'unidad2', 'ref_min2', 'ref_max2',
            'intervalo_min', 'intervalo_max',
            'observaciones',
        ]
        widgets = {
            'hormona':       forms.Select(attrs={'class': 'form-select'}),
            'version':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: V11.0 y V12.0'}),
            'grupo_clinico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Hombres, Mujeres Fase Folicular'}),
            'tipo_muestra':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Suero y Plasma'}),
            'unidad':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: µUI/mL'}),
            'ref_min':       forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'ref_max':       forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'unidad2':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ng/mL'}),
            'ref_min2':      forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'ref_max2':      forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'intervalo_min': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'intervalo_max': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                                   'placeholder': 'Notas u observaciones adicionales...'}),
        }
