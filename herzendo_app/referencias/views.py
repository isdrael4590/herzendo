import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from functools import wraps
from .models import ValorReferencia, HORMONA_CHOICES
from .forms import ValorReferenciaForm
from . import excel_importer


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
    hormona_sel = request.GET.get('hormona', '')
    qs = ValorReferencia.objects.all()
    if hormona_sel:
        qs = qs.filter(hormona=hormona_sel)

    # Agrupar por hormona para la vista
    grupos = {}
    for vr in qs:
        grupos.setdefault(vr.get_hormona_display(), []).append(vr)

    return render(request, 'referencias/lista.html', {
        'grupos':       grupos,
        'hormonas':     HORMONA_CHOICES,
        'hormona_sel':  hormona_sel,
    })


@role_required('administrador', 'medico')
def crear(request):
    hormona_inicial = request.GET.get('hormona', '')
    initial = {'hormona': hormona_inicial} if hormona_inicial else {}
    form = ValorReferenciaForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Valor de referencia guardado.')
        return redirect('referencias:lista')
    return render(request, 'referencias/form.html', {'form': form, 'titulo': 'Nuevo valor de referencia'})


@role_required('administrador', 'medico')
def editar(request, pk):
    vr = get_object_or_404(ValorReferencia, pk=pk)
    form = ValorReferenciaForm(request.POST or None, instance=vr)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Valor de referencia actualizado.')
        return redirect('referencias:lista')
    return render(request, 'referencias/form.html', {
        'form': form,
        'titulo': f'Editar — {vr.get_hormona_display()} {vr.version}',
        'object': vr,
    })


@login_required
def api_hormona(request, hormona):
    def _f(v):
        return float(v) if isinstance(v, Decimal) else v

    registros = ValorReferencia.objects.filter(hormona=hormona).order_by('version', 'grupo_clinico')
    data = []
    for vr in registros:
        label = vr.version
        if vr.grupo_clinico:
            label += f' · {vr.grupo_clinico}'
        data.append({
            'label':   label,
            'ref_min': _f(vr.ref_min),
            'ref_max': _f(vr.ref_max),
            'unidad':  vr.unidad,
        })
    return JsonResponse({'grupos': data})


@role_required('administrador', 'medico')
def importar_excel(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        modo    = request.POST.get('modo', 'crear')
        if not archivo:
            messages.error(request, 'Seleccione un archivo Excel.')
            return redirect('referencias:importar_excel')
        if not archivo.name.lower().endswith(('.xlsx', '.xls')):
            messages.error(request, 'Solo se aceptan archivos .xlsx o .xls.')
            return redirect('referencias:importar_excel')
        try:
            resultado = excel_importer.importar_excel(archivo, modo=modo)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('referencias:importar_excel')

        resumen = (
            f"Importación completada: "
            f"{resultado['creados']} creados, "
            f"{resultado['actualizados']} actualizados, "
            f"{resultado['omitidos']} omitidos."
        )
        if resultado['errores']:
            resumen += f" {len(resultado['errores'])} errores."
        messages.success(request, resumen)
        return render(request, 'referencias/importar_excel.html', {
            'resultado': resultado,
        })

    return render(request, 'referencias/importar_excel.html', {})


@role_required('administrador')
def eliminar(request, pk):
    vr = get_object_or_404(ValorReferencia, pk=pk)
    if request.method == 'POST':
        vr.delete()
        messages.success(request, 'Valor de referencia eliminado.')
        return redirect('referencias:lista')
    return render(request, 'referencias/confirmar_eliminar.html', {'vr': vr})
