import json
from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Paciente
from .forms import PacienteForm
from .forms_usuario import UsuarioCrearForm, UsuarioEditarForm


def role_required(*grupos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.groups.filter(name__in=grupos).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapped
    return decorator


@login_required
def lista(request):
    q = request.GET.get('q', '')
    pacientes = Paciente.objects.all()
    if q:
        pacientes = pacientes.filter(
            Q(nombre__icontains=q) |
            Q(hcu__icontains=q) |
            Q(cirujano__icontains=q) |
            Q(procedimiento__icontains=q)
        )
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes, 'q': q})


@role_required('administrador', 'medico')
def crear(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro guardado correctamente.')
            return redirect('lista')
    else:
        initial = {k: v for k, v in request.GET.items() if v}
        form = PacienteForm(initial=initial)
    return render(request, 'pacientes/form.html', {'form': form, 'titulo': 'Nuevo Registro'})


@role_required('administrador', 'medico')
def editar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    form = PacienteForm(request.POST or None, instance=paciente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Registro actualizado correctamente.')
        return redirect('lista')
    return render(request, 'pacientes/form.html', {'form': form, 'titulo': f'Editar — {paciente.nombre}', 'object': paciente})


@role_required('administrador')
def eliminar(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Registro eliminado.')
        return redirect('lista')
    return render(request, 'pacientes/confirmar_eliminar.html', {'paciente': paciente})


@role_required('administrador', 'medico')
def subir_pdf(request):
    return render(request, 'pacientes/subir_pdf.html')


@role_required('administrador', 'medico')
@require_POST
def procesar_pdf(request):
    from .pdf_extractor import extraer_todo

    archivo = request.FILES.get('pdf')
    if not archivo:
        return JsonResponse({'error': 'No se recibió ningún archivo.'}, status=400)
    if not archivo.name.lower().endswith('.pdf'):
        return JsonResponse({'error': 'El archivo debe ser un PDF.'}, status=400)
    if archivo.size > 50 * 1024 * 1024:
        return JsonResponse({'error': 'El archivo no debe superar 50 MB.'}, status=400)

    try:
        texto, campos, paginas, gemini_status = extraer_todo(archivo)
        return JsonResponse({
            'campos': campos,
            'paginas': paginas,
            'gemini_status': gemini_status,
            'texto_crudo': texto[:4000],
            'total_campos': len(campos),
        })
    except Exception as e:
        return JsonResponse({'error': f'No se pudo procesar el PDF: {str(e)}'}, status=500)


@login_required
def imprimir(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    return render(request, 'pacientes/imprimir.html', {'paciente': paciente})


# ── Gestión de usuarios (solo administrador) ──────────────────────────────────

@role_required('administrador')
def usuarios_lista(request):
    usuarios = User.objects.exclude(is_superuser=True).order_by('username')
    return render(request, 'pacientes/usuarios_lista.html', {'usuarios': usuarios})


@role_required('administrador')
def usuario_crear(request):
    form = UsuarioCrearForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        u = User.objects.create_user(
            username=cd['username'],
            password=cd['password1'],
            first_name=cd.get('first_name', ''),
            last_name=cd.get('last_name', ''),
            email=cd.get('email', ''),
        )
        if cd['rol']:
            grupo, _ = Group.objects.get_or_create(name=cd['rol'])
            u.groups.set([grupo])
        messages.success(request, f'Usuario "{u.username}" creado correctamente.')
        return redirect('usuarios_lista')
    return render(request, 'pacientes/usuario_form.html', {
        'form': form, 'titulo': 'Nuevo Usuario', 'es_edicion': False,
    })


@role_required('administrador')
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    rol_actual = usuario.groups.values_list('name', flat=True).first() or ''
    initial = {
        'username': usuario.username,
        'first_name': usuario.first_name,
        'last_name': usuario.last_name,
        'email': usuario.email,
        'rol': rol_actual,
        'is_active': usuario.is_active,
    }
    form = UsuarioEditarForm(request.POST or None, usuario=usuario, initial=initial)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        usuario.username   = cd['username']
        usuario.first_name = cd.get('first_name', '')
        usuario.last_name  = cd.get('last_name', '')
        usuario.email      = cd.get('email', '')
        usuario.is_active  = cd.get('is_active', True)
        if cd.get('password1'):
            usuario.set_password(cd['password1'])
        usuario.save()
        if cd['rol']:
            grupo, _ = Group.objects.get_or_create(name=cd['rol'])
            usuario.groups.set([grupo])
        else:
            usuario.groups.clear()
        messages.success(request, f'Usuario "{usuario.username}" actualizado.')
        return redirect('usuarios_lista')
    return render(request, 'pacientes/usuario_form.html', {
        'form': form, 'titulo': f'Editar — {usuario.username}',
        'es_edicion': True, 'usuario': usuario,
    })


@role_required('administrador')
def usuario_eliminar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario.is_superuser:
        messages.error(request, 'No se puede eliminar a un superusuario.')
        return redirect('usuarios_lista')
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado.')
        return redirect('usuarios_lista')
    return render(request, 'pacientes/usuario_confirmar_eliminar.html', {'usuario': usuario})
