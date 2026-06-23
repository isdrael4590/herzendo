from django import forms
from django.contrib.auth.models import User

ROLES = [
    ('', '— Seleccione un rol —'),
    ('administrador', 'Administrador'),
    ('medico', 'Médico'),
    ('visualizador', 'Visualizador'),
]


class UsuarioCrearForm(forms.Form):
    username         = forms.CharField(max_length=150)
    first_name       = forms.CharField(max_length=150, required=False)
    last_name        = forms.CharField(max_length=150, required=False)
    email            = forms.EmailField(required=False)
    rol              = forms.ChoiceField(choices=ROLES)
    ver_codificado   = forms.BooleanField(required=False, label='Acceso a datos codificados')
    ver_estadisticas = forms.BooleanField(required=False, label='Acceso a estadísticas')
    password1        = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2        = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        u = self.cleaned_data['username']
        if User.objects.filter(username=u).exists():
            raise forms.ValidationError('Ese nombre de usuario ya está en uso.')
        return u

    def clean(self):
        cd = super().clean()
        if cd.get('password1') and cd.get('password1') != cd.get('password2'):
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cd


class UsuarioEditarForm(forms.Form):
    username         = forms.CharField(max_length=150)
    first_name       = forms.CharField(max_length=150, required=False)
    last_name        = forms.CharField(max_length=150, required=False)
    email            = forms.EmailField(required=False)
    rol              = forms.ChoiceField(choices=ROLES)
    ver_codificado   = forms.BooleanField(required=False, label='Acceso a datos codificados')
    ver_estadisticas = forms.BooleanField(required=False, label='Acceso a estadísticas')
    is_active        = forms.BooleanField(required=False, initial=True)
    password1        = forms.CharField(widget=forms.PasswordInput, required=False, min_length=8)
    password2        = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def clean_username(self):
        u = self.cleaned_data['username']
        qs = User.objects.filter(username=u)
        if self.usuario:
            qs = qs.exclude(pk=self.usuario.pk)
        if qs.exists():
            raise forms.ValidationError('Ese nombre de usuario ya está en uso.')
        return u

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')
        if p1 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cd
